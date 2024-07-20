from apps.catastro.models import LcDcPredio, SdeEstado, LcDatosadicionaleslevcat
from apps.dominios.models import LcResultadovisitatipo, LcDestinacioneconomicatipo
from django.db.models import Max
from apps.catastro.serializer.serializer import DetailPredioSerializer

def get_instance_SDEstado():
    instance = SdeEstado.objects.get(id_estado = 1)
    return instance

def get_instance(Model, field_name, value):
    # Obtener la instancia del modelo utilizando el campo y el valor proporcionados
    instance = Model.objects.get(**{field_name: value})
    return instance

def create_editar_general(data, instance_predio):
    try:
        general = data.get('general', {})
        matricula = general.get('matricula',0)
        direccion = general.get('direccion','')
        direccion_notificacion = general.get('direccionNotificacion','')
        resultado_visita = general.get('selectResultadoVisita')
        destinos = general.get('selectDestinos')
        observacion = general.get('observacion')

        
        # Obtener instancias de relaciones foráneas
        instance_resultado_visita = get_instance(LcResultadovisitatipo,'descri_resultado', resultado_visita)
        instance_destino = get_instance(LcDestinacioneconomicatipo,'desc_destecno', destinos)

        instance_predio.matricula = matricula
        instance_predio.direccion_predio = direccion
        instance_predio.direccion_notificacion = direccion_notificacion
        instance_predio.id_destecono = instance_destino
        instance_predio.save()

        instance_LcDatosadicionaleslevcat = LcDatosadicionaleslevcat.objects.get(id_predio=instance_predio)
        instance_LcDatosadicionaleslevcat.id_resultado = instance_resultado_visita
        instance_LcDatosadicionaleslevcat.observaciones = observacion
        instance_LcDatosadicionaleslevcat.save()

        serializer_data = DetailPredioSerializer(instance_predio).data
        return {'data': serializer_data, 'message': 'Generales editados con exito'}

    except Exception as e:
        # Manejo de errores
        message = f'Error al crear o editar los generales: {str(e)}'
        return {'data': None, 'message': message}
    
