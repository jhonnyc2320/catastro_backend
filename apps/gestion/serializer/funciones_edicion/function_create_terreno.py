from apps.catastro.models import LcTerreno, SdeEstado
from apps.dominios.models import LcRestricciontipo
from django.db.models import Max
from apps.catastro.serializer.serializer_basic import TerrenosZonasSerializer

def get_instance_SDEstado():
    instance = SdeEstado.objects.get(id_estado = 1)
    return instance

def get_instance_restriccion_tipo(restriccion_tipo):
    instance = LcRestricciontipo.objects.get(descr_restricciontipo = restriccion_tipo)
    return instance

def create_editar_terreno(data, instance_predio):
    try:
        terreno = data.get('terreno', {})
        id_terreno = terreno.get('id', 0)
        area_total = terreno.get('area_total')
        area_comun = terreno.get('area_comun')
        restriccion_tipo = terreno.get('restriccion_tipo')
        # Obtener instancias de relaciones foráneas
        instance_SDEstado = get_instance_SDEstado()
        instance_restriccion_tipo = get_instance_restriccion_tipo(restriccion_tipo)
        
        dict_terreno = {
            'id_predio': instance_predio,
            'id_operacion': 1,
            'area_total': area_total,
            'area_comun': area_comun,
            'pre_retirado': instance_SDEstado,
            'id_rest_servi': instance_restriccion_tipo
        }

        message = ''
        if id_terreno == 0:
            
            # Eliminar terrenos asociados al predio
            LcTerreno.objects.filter(id_predio=instance_predio).delete()

            # Obtener el último id_terreno y calcular el próximo id
            last_id = LcTerreno.objects.aggregate(Max('id_terreno'))['id_terreno__max']
            next_id = (last_id or 0) + 1
            dict_terreno.update({'id_terreno': next_id})
            
            # Crear un nuevo terreno
            nuevo_terreno = LcTerreno.objects.create(**dict_terreno)
            serializer_data = TerrenosZonasSerializer(nuevo_terreno).data
            return {'data': serializer_data, 'message': 'Terreno creado con éxito'}

        else:
            # Actualizar el terreno existente
            LcTerreno.objects.filter(id_terreno=id_terreno).update(**dict_terreno)
            message = 'Terreno editado con éxito'
            instance_terreno = LcTerreno.objects.get(id_terreno=id_terreno)
            serializer_data = TerrenosZonasSerializer(instance_terreno).data
            return {'data': serializer_data, 'message': message}

    except Exception as e:
        # Manejo de errores
        message = f'Error al crear o editar el terreno: {str(e)}'
        return {'data': None, 'message': message}
    
