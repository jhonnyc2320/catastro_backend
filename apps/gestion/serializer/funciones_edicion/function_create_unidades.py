from apps.catastro.models import LcUnidadConstruccion, SdeEstado, Lc_puntaje, Cat_clase, Cat_calificacion, Cat_estructura
from apps.dominios.models import (
    LcUnidadconstrucciontipo, LcAnexotipo, LcDominioconstrucciontipo, LcConstruccionplantatipo,
    LcConstrucciontipo, LcUsoconstipo
)
from django.db.models import Max
from apps.catastro.serializer.serializer_basic import CaracteristicasUnidadConstruccionSerializer
from django.db.models import Sum


def get_instance_SDEstado():
    instance = SdeEstado.objects.get(id_estado = 1)
    return instance

def get_instance(Model, field_name, value):
    # Obtener la instancia del modelo utilizando el campo y el valor proporcionados
    instance = Model.objects.get(**{field_name: value})
    return instance

def handle_calificacion(value, clase_clase_detalle, codiestru_id, dict_calificacion, cod_cali):
    if value:
        partes = value.split('-', 1)
        if len(partes) == 2:
            
            puntaje = partes[0].strip()
            detalle = partes[1].strip()
            instance_codiclas = Cat_calificacion.objects.get(id=cod_cali)
            instance_cat_estru = Cat_estructura.objects.get(id=codiestru_id)
            #instance_clase = Cat_clase.objects.filter(detalle=detalle, puntaje=puntaje, codiestr=instance_cat_estru.id ,clase_clase__detalle=clase_clase_detalle.des_undconsttipo).first()
            instance_clase = Cat_clase.objects.filter(detalle=detalle, codiestr=instance_cat_estru.id ,clase_clase__detalle=clase_clase_detalle.des_undconsttipo).first()
            print(detalle, 'detalle')
            print(clase_clase_detalle.des_undconsttipo, 'clase_clase')
            print(cod_cali, 'codiclas')
            print(codiestru_id, 'codiestru')
            dict_calificacion.update({
                'puntaje': puntaje,
                'codcali': instance_codiclas,
                'codiclas': instance_clase,
                'codiestru': instance_cat_estru,
            })
            Lc_puntaje.objects.create(**dict_calificacion)
    else:
        puntaje = None
        detalle = None

def create_editar_unidad(data, instance_predio):
    # try:
        terreno = data.get('unidad', {})
        id_construccion = terreno.get('id', 0)
        unidad = terreno.get('unidad', 0)
        area_comun = terreno.get('area_comun')
        area_total = terreno.get('area_total')
        puntaje = terreno.get('puntaje') if terreno.get('construccion_tipo') == 'CONVENCIONAL' else 0
        anio_construccion = terreno.get('anio_construccion')
        banio = terreno.get('banio')
        locales = terreno.get('locales')
        habitaciones = terreno.get('habitaciones')
        mezanines = terreno.get('mezanines')
        sotanos = terreno.get('sotanos')
        pisos = terreno.get('pisos')
        planta_ubicacion = terreno.get('planta_ubicacion')
        unidad_construccion_tipo = terreno.get('unidad_construccion_tipo')
        anexo_tipo = terreno.get('anexo_tipo')
        dominio_tipo = terreno.get('dominio_tipo')
        construccion_tipo = terreno.get('construccion_tipo')
        construccion_planta_tipo = terreno.get('construccion_planta_tipo')
        estado_unidad = terreno.get('estado_unidad')
        uso = terreno.get('uso')
        complemento_industrial = terreno.get('complemento_industrial')
        isCheckedComplemento=terreno.get('isCheckedComplemento')

        if estado_unidad == 'RETIRADO':
            instance_sde_estado = get_instance(SdeEstado, 'desc_estado', estado_unidad)
            instance_unidad = LcUnidadConstruccion.objects.filter(id_construccion=id_construccion).first()
            instance_unidad.retirado = instance_sde_estado
            instance_unidad.save()
            message = 'Unidad retirada con exito'
        else:
            # Verificar si la cadena no está vacía
            if anexo_tipo and construccion_tipo == 'NO_CONVENCIONAL' :
                # Separar la cadena por el carácter '-'
                if '-' in anexo_tipo:
                    calificacion, descripcion = anexo_tipo.split('-', 1)
                    
                    # Buscar la instancia en la base de datos
                    instance_anexo_tipo = LcAnexotipo.objects.filter(des_anexotipo=descripcion, calificacion=calificacion).first()
                    
                    # Si no existe, crear una nueva instancia
                    if not instance_anexo_tipo:
                        instance_anexo_tipo = None
                else:
                    instance_anexo_tipo = None
            else:
                instance_anexo_tipo = None
            
            # Obtener instancias de relaciones foráneas
            
            instance_sde_estado = get_instance(SdeEstado, 'desc_estado', estado_unidad)
            instance_construccion_planta_tipo = get_instance(LcConstruccionplantatipo, 'des_constplantatipo', construccion_planta_tipo)
            instance_construccion_tipo = get_instance(LcConstrucciontipo, 'des_consttipo', construccion_tipo)
            instance_dominio_construccion_tipo = get_instance(LcDominioconstrucciontipo, 'des_domconsttipo', dominio_tipo)
            instance_unidad_construccion_tipo = get_instance(LcUnidadconstrucciontipo, 'des_undconsttipo', unidad_construccion_tipo)
            instance_uso = get_instance(LcUsoconstipo, 'des_usocons', uso)
            
            # instance_retirado = get_instance_SDEstado()
            
            dict_terreno = {
                'id_predio': instance_predio,
                'identificador': id_construccion,
                'id_constipo': instance_construccion_tipo,
                'id_undconstipo': instance_unidad_construccion_tipo,
                'id_domconstipo': instance_dominio_construccion_tipo,
                'id_unidad': unidad,
                'id_usocons': instance_uso,
                'area_construida': area_total,
                'area_construida_comun': area_comun,
                'anio_construccion': anio_construccion,
                'total_locales': locales,
                'total_banos': banio,
                'total_pisos': pisos,
                'total_habitaciones': habitaciones,
                'id_constplantatipo': instance_construccion_planta_tipo,
                'numero_sotanos': sotanos,
                'numero_mezanines': mezanines,
                'total_puntaje': puntaje,
                'planta_ubicacion': planta_ubicacion,
                'retirado': instance_sde_estado,
                'id_anexotipo': instance_anexo_tipo,
            }

            dict_calificacion = {
                'puntaje':None,
                'codcali':None,
                'codiclas':None,
                'codiestru':None,
                'id_predio':None,
                'id_unidad':None
            }

            message = ''
            
            instance_unidad = None
            if id_construccion == 0:
                # Obtener el último id_terreno y calcular el próximo id
                last_id = LcUnidadConstruccion.objects.aggregate(Max('id_construccion'))['id_construccion__max']
                next_id = (last_id or 0) + 1
                dict_terreno.update({'id_construccion': next_id})
                
                # Crear un nuevo terreno
                instance_unidad = LcUnidadConstruccion.objects.create(**dict_terreno)
                dict_calificacion['id_unidad'] = instance_unidad
                message = 'Unidad creada con exito'
            else:
                # Actualizar el terreno existente
                instance_unidad = LcUnidadConstruccion.objects.filter(id_construccion=id_construccion)
                dict_calificacion['id_unidad'] = instance_unidad.first()
                instance_unidad.update(**dict_terreno)
                instance_unidad = instance_unidad.first()
                message = 'Terreno editado con éxito'
            
            dict_calificacion['id_predio'] = instance_predio
            # instance_codiclas = None
            # if estructuraCubierta:
            #     partes = estructuraCubierta.split('-', 1)  # El segundo parámetro limita la cantidad de splits
            #     if len(partes) == 2:
            #         puntaje = partes[0].strip()  # Elimina espacios innecesarios
            #         detalle = partes[1].strip()
            #         instance_codiclas = Cat_calificacion.objects.get(id=1)
            #         instance_clase = Cat_clase.objects.get(detalle=detalle, puntaje=puntaje, clase_clase__detalle = instance_unidad_construccion_tipo.des_undconsttipo )
            #         instance_cat_estru = Cat_estructura.objects.get(id=3) 

            #         dict_calificacion['puntaje'] = puntaje
            #         dict_calificacion['codcali'] = instance_codiclas
            #         dict_calificacion['codiclas'] = instance_clase
            #         dict_calificacion['codiestru'] = instance_cat_estru
            #         dict_calificacion['id_predio'] = instance_predio
            #         Lc_puntaje.objects.create(**dict_calificacion)

            # else:
            #     puntaje = None
            #     detalle = None
        
            result = Lc_puntaje.objects.filter(id_predio=instance_predio, id_unidad=dict_calificacion['id_unidad'])
            result.delete()

            if construccion_tipo == 'CONVENCIONAL':
            
                estructuraCubierta = terreno.get('estructuraCubierta', [None])
                estructuraCubierta = estructuraCubierta[0] if isinstance(estructuraCubierta, list) and len(estructuraCubierta) > 0 else estructuraCubierta
                handle_calificacion(estructuraCubierta, instance_unidad_construccion_tipo, 3, dict_calificacion,1)

                estructuraMuros = terreno.get('estructuraMuros', [None])
                estructuraMuros = estructuraMuros[0] if isinstance(estructuraMuros, list) and len(estructuraMuros) > 0 else estructuraMuros
                handle_calificacion(estructuraMuros, instance_unidad_construccion_tipo, 2, dict_calificacion,1)

                estructuraArmazon = terreno.get('estructuraArmazon', [None])
                estructuraArmazon = estructuraArmazon[0] if isinstance(estructuraArmazon, list) and len(estructuraArmazon) > 0 else estructuraArmazon
                handle_calificacion(estructuraArmazon, instance_unidad_construccion_tipo, 1, dict_calificacion,1)

                estructuraConservacion = terreno.get('estructuraConservacion', [None])
                estructuraConservacion = estructuraConservacion[0] if isinstance(estructuraConservacion, list) and len(estructuraConservacion) > 0 else estructuraConservacion
                handle_calificacion(estructuraConservacion, instance_unidad_construccion_tipo, 4, dict_calificacion,1)

                acabadosPrincipalesFachada = terreno.get('acabadosPrincipalesFachada', [None])
                acabadosPrincipalesFachada = acabadosPrincipalesFachada[0] if isinstance(acabadosPrincipalesFachada, list) and len(acabadosPrincipalesFachada) > 0 else acabadosPrincipalesFachada
                handle_calificacion(acabadosPrincipalesFachada, instance_unidad_construccion_tipo, 5, dict_calificacion,2)

                acabadosPrincipalesCubrimientoMuros = terreno.get('acabadosPrincipalesCubrimientoMuros', [None])
                acabadosPrincipalesCubrimientoMuros = acabadosPrincipalesCubrimientoMuros[0] if isinstance(acabadosPrincipalesCubrimientoMuros, list) and len(acabadosPrincipalesCubrimientoMuros) > 0 else acabadosPrincipalesCubrimientoMuros
                handle_calificacion(acabadosPrincipalesCubrimientoMuros, instance_unidad_construccion_tipo, 6, dict_calificacion,2)

                acabadosPrincipalesPisos = terreno.get('acabadosPrincipalesPisos', [None])
                acabadosPrincipalesPisos = acabadosPrincipalesPisos[0] if isinstance(acabadosPrincipalesPisos, list) and len(acabadosPrincipalesPisos) > 0 else acabadosPrincipalesPisos
                handle_calificacion(acabadosPrincipalesPisos, instance_unidad_construccion_tipo, 7, dict_calificacion,2)

                acabadosPrincipalesConservacion = terreno.get('acabadosPrincipalesConservacion', [None])
                acabadosPrincipalesConservacion = acabadosPrincipalesConservacion[0] if isinstance(acabadosPrincipalesConservacion, list) and len(acabadosPrincipalesConservacion) > 0 else acabadosPrincipalesConservacion
                handle_calificacion(acabadosPrincipalesConservacion, instance_unidad_construccion_tipo, 8, dict_calificacion,2)
                
                banioMobiliario = terreno.get('banioMobiliario', [None])
                banioMobiliario = banioMobiliario[0] if isinstance(banioMobiliario, list) and len(banioMobiliario) > 0 else banioMobiliario
                handle_calificacion(banioMobiliario, instance_unidad_construccion_tipo, 11, dict_calificacion,3)

                if unidad_construccion_tipo == 'RESIDENCIAL':

                    banioTamanio = terreno.get('banioTamanio', [None])
                    banioTamanio = banioTamanio[0] if isinstance(banioTamanio, list) and len(banioTamanio) > 0 else banioTamanio
                    handle_calificacion(banioTamanio, instance_unidad_construccion_tipo, 9, dict_calificacion,3)

                    banioEnchapes = terreno.get('banioEnchapes', [None])
                    banioEnchapes = banioEnchapes[0] if isinstance(banioEnchapes, list) and len(banioEnchapes) > 0 else banioEnchapes
                    handle_calificacion(banioEnchapes, instance_unidad_construccion_tipo, 10, dict_calificacion,3)

                    banioConservacion = terreno.get('banioConservacion', [None])
                    banioConservacion = banioConservacion[0] if isinstance(banioConservacion, list) and len(banioConservacion) > 0 else banioConservacion
                    handle_calificacion(banioConservacion, instance_unidad_construccion_tipo, 12, dict_calificacion,3)
                
                cocinaMobiliario = terreno.get('cocinaMobiliario', [None])
                cocinaMobiliario = cocinaMobiliario[0] if isinstance(cocinaMobiliario, list) and len(cocinaMobiliario) > 0 else cocinaMobiliario
                handle_calificacion(cocinaMobiliario, instance_unidad_construccion_tipo, 15, dict_calificacion,4)
                
                if unidad_construccion_tipo == 'RESIDENCIAL':
                
                    cocinaTamanio = terreno.get('cocinaTamanio', [None])
                    cocinaTamanio = cocinaTamanio[0] if isinstance(cocinaTamanio, list) and len(cocinaTamanio) > 0 else cocinaTamanio
                    handle_calificacion(cocinaTamanio, instance_unidad_construccion_tipo, 13, dict_calificacion,4)

                    cocinaEnchapes = terreno.get('cocinaEnchapes', [None])
                    cocinaEnchapes = cocinaEnchapes[0] if isinstance(cocinaEnchapes, list) and len(cocinaEnchapes) > 0 else cocinaEnchapes
                    handle_calificacion(cocinaEnchapes, instance_unidad_construccion_tipo, 14, dict_calificacion,4)
                    
                    cocinaConservacion = terreno.get('cocinaConservacion', [None])
                    cocinaConservacion = cocinaConservacion[0] if isinstance(cocinaConservacion, list) and len(cocinaConservacion) > 0 else cocinaConservacion
                    handle_calificacion(cocinaConservacion, instance_unidad_construccion_tipo, 16, dict_calificacion,4)

                if unidad_construccion_tipo == 'INDUSTRIAL':
                    if terreno.get('complemento_industrial', [None]) != '0-Sin calificar':
                        complementoIdustrial = terreno.get('complemento_industrial', [None])
                        complementoIdustrial = complementoIdustrial[0] if isinstance(complementoIdustrial, list) and len(complementoIdustrial) > 0 else complementoIdustrial
                        handle_calificacion(complementoIdustrial, instance_unidad_construccion_tipo, 17, dict_calificacion,5)

                # Inicialización de la variable para la suma del puntaje
                suma_puntaje = 0
                # Realización de la consulta
                resultado = Lc_puntaje.objects.filter(id_unidad=instance_unidad)
                # Iteración sobre el queryset para sumar los puntajes
                for registro in resultado:
                    if registro.puntaje:
                        suma_puntaje += int(registro.puntaje)
                    else:
                        suma_puntaje += 0
                instance_unidad.total_puntaje = suma_puntaje
                instance_unidad.save()
            
        instance_terreno = LcUnidadConstruccion.objects.filter(id_predio=instance_predio)
        serializer_data = CaracteristicasUnidadConstruccionSerializer(instance_terreno, many = True).data
        return {'data': serializer_data, 'message': message}

    # except Exception as e:
    #     # Manejo de errores
    #     message = f'Error al crear o editar el terreno: {str(e)}'
    #     return {'data': None, 'message': message}
    
