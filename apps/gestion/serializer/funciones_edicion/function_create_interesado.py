from apps.catastro.models import LcTerreno, SdeEstado, Derecho_predio, Interesado
from apps.dominios.models import LcSexotipo, LcInteresadodocumentotipo, LcInteresadotipo, LcGrupoetnicotipo
from django.db.models import Max
from apps.catastro.serializer.serializer_basic import TerrenosZonasSerializer, InteresadoPredioSerializer
from django.utils import timezone

def get_instance_SDEstado():
    instance = SdeEstado.objects.get(id_estado = 1)
    return instance

def get_instance(Model, field_name, value):
    # Obtener la instancia del modelo utilizando el campo y el valor proporcionados
    instance = Model.objects.get(**{field_name: value})
    return instance

def capitalizar_campos_interesado(interesado):
        campos_a_capitalizar = [
            'primer_nombre', 
            'segundo_nombre', 
            'primer_apellido', 
            'segundo_apellido', 
            'razon_social'
        ]
        for campo in campos_a_capitalizar:
            valor = interesado.get(campo, "").strip()
            if valor:
                interesado[campo] = valor.upper()
            else:
                interesado[campo] = None
        return interesado

def verificar_propietario(interesado, id_interesado):

        # Asume que 'interesado' es tu diccionario de entrada
        campos_interesado = ['primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'razon_social']
        # Transforma los campos vacíos en None
        interesado_procesado = {k: (v if v else None) for k, v in interesado.items() if k in campos_interesado}
        
        instance_interesado = Interesado.objects.filter(
            primer_nombre = interesado_procesado.get('primer_nombre'),
            segundo_nombre= interesado_procesado.get('segundo_nombre'),
            primer_apellido = interesado_procesado.get('primer_apellido'),
            segundo_apellido= interesado_procesado.get('segundo_apellido'),
            razon_social = interesado_procesado.get('razon_social'),
            documento_identidad = interesado.get('documento_identidad'),
            id_tipodoc__des_tipodoc = interesado.get('tipo_documento'),
            id_interesadotipo__des_interesadotipo = interesado.get('interesado_tipo')
        )
        
        if not instance_interesado.exists():
            return None, False
        
        return instance_interesado.first(), True

def create_editar_interesado(data, instance_predio):
    # try:
        data_entidada = data.get('interesado', {})
        capitalizar_campos_interesado(data_entidada)
        id_entidad = data_entidada.get('id', 0)
        id_interesado = data_entidada.get('id_interesado', 0)
        documento_identidad = data_entidada.get('documento_identidad')
        interesado_tipo = data_entidada.get('interesado_tipo')
        tipo_documento = data_entidada.get('tipo_documento')
        primer_nombre = data_entidada.get('primer_nombre')
        segundo_nombre = data_entidada.get('segundo_nombre')
        primer_apellido = data_entidada.get('primer_apellido')
        segundo_apellido = data_entidada.get('segundo_apellido')
        razon_social = data_entidada.get('razon_social')
        sexo = data_entidada.get('sexo')
        etnia = data_entidada.get('etnia')
        porcentaje_participacion = data_entidada.get('porcentaje_participacion')
        telefono_uno = data_entidada.get('telefono_uno')
        telefono_dos = data_entidada.get('telefono_dos')
        correo_electronico = data_entidada.get('correo_electronico')
        
        # Ejemplos de cómo llamar a la función genérica
        instance_sexotipo = get_instance(LcSexotipo, 'des_genero', sexo)
        instance_documentotipo = get_instance(LcInteresadodocumentotipo, 'des_tipodoc', tipo_documento)
        instance_interesadotipo = get_instance(LcInteresadotipo, 'des_interesadotipo', interesado_tipo)
        instance_grupoetnicotipo = get_instance(LcGrupoetnicotipo, 'des_etnia', etnia)
        
        dict_interesado = {
            'documento_identidad': documento_identidad,
            'id_tipodoc': instance_documentotipo,
            'primer_nombre': primer_nombre,
            'segundo_nombre': segundo_nombre,
            'primer_apellido': primer_apellido,
            'segundo_apellido': segundo_apellido,
            'razon_social': razon_social,
            'id_genero': instance_sexotipo,
            'id_etnia': instance_grupoetnicotipo,
            'id_interesadotipo': instance_interesadotipo,
            'telefono_uno': telefono_uno,
            'telefono_dos': telefono_dos,
            'correo_electronico': correo_electronico,
        }

        dict_derecho_predio={
            'predio': instance_predio,
            'fraccion_derecho': porcentaje_participacion,
            'interesado': None
        }

        message = ''
        if id_entidad == 0:
            instance_interesado, verificado = verificar_propietario(data_entidada, id_interesado)

            if not verificado:
                instance_interesado_nuevo = Interesado.objects.create(**dict_interesado)
                dict_derecho_predio.update({'interesado': instance_interesado_nuevo, 'fraccion_derecho':porcentaje_participacion})
                Derecho_predio.objects.create(**dict_derecho_predio)

                # # Eliminar terrenos asociados al predio
                # LcTerreno.objects.filter(id_predio=instance_predio).delete()

                # # Obtener el último id_terreno y calcular el próximo id
                # last_id = LcTerreno.objects.aggregate(Max('id_terreno'))['id_terreno__max']
                # next_id = (last_id or 0) + 1
                # dict_interesado.update({'id_terreno': next_id})
            
            else:
                dict_derecho_predio.update({'interesado': instance_interesado, 'fraccion_derecho':porcentaje_participacion})
                Derecho_predio.objects.create(**dict_derecho_predio)

            list_instance_derecho_predio = Derecho_predio.objects.filter(predio = instance_predio)
            serializer_data = InteresadoPredioSerializer(list_instance_derecho_predio, many=True).data
            return {'data': serializer_data, 'message': message} 

        else:
            # Actualizar el interesado existente
            instance_derecho_predio = Derecho_predio.objects.get(id=id_entidad)
            instance_derecho_predio.fraccion_derecho = porcentaje_participacion
            instance_derecho_predio.save()
            id_interesado = instance_derecho_predio.interesado.id
            Interesado.objects.filter(id = id_interesado).update(**dict_interesado)
            message = 'Interesado actualizado con éxito'
            instance_interesados = Derecho_predio.objects.filter(predio=instance_predio)
            serializer_data = InteresadoPredioSerializer(instance_interesados, many=True).data
            return {'data': serializer_data, 'message': message}

    # except Exception as e:
    #     # Manejo de errores
    #     message = f'Error al crear o editar el interesado: {str(e)}'
    #     print(message,'ssss')
    #     return {'data': None, 'message': message}
    
