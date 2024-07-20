# from apps.espacial.models import Terreno_zonas, Unidad_construccion
from apps.catastro.models import Historia as Tramite_catastral_historico, Derecho_predio, LcUnidadConstruccion, LcDcPredio, LcTerreno, Asignacion, Trazabilidad, LcDatosadicionaleslevcat, ContactoVisita, Npn
from rest_framework import serializers
from django.db.models import QuerySet

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

# IMPORT CUSTOM SERIALIZER
from .serializer_basic import (
    InteresadoPredioSerializer, TerrenosZonasSerializer, CaracteristicasUnidadConstruccionSerializer
)

import datetime

class FindPredioListSerializer(serializers.ModelSerializer):

    departamento = serializers.SerializerMethodField()
    destino = serializers.SerializerMethodField()
    estado = serializers.SerializerMethodField()
    municipio = serializers.SerializerMethodField()
    matricula = serializers.SerializerMethodField()
    direccion = serializers.SerializerMethodField()
    numero_predial = serializers.SerializerMethodField()
    vigencia = serializers.SerializerMethodField()
    area_terreno = serializers.SerializerMethodField()
    analista = serializers.SerializerMethodField()
    coordinador = serializers.SerializerMethodField()
    fecha = serializers.SerializerMethodField()
    observacion = serializers.SerializerMethodField()
    area_construida = serializers.SerializerMethodField()
    resultado_visita = serializers.SerializerMethodField()
    semana =serializers.SerializerMethodField()
    fecha_trazabilidad = serializers.SerializerMethodField()
    comuna = serializers.SerializerMethodField()
    

    class Meta:
        model = LcDcPredio
        fields = (
            'id_predio','npn','comuna','semana','direccion', 'numero_predial', 'vigencia',  'departamento',
            'destino', 'area_terreno', 'estado','fecha_trazabilidad','analista', 'coordinador', 'fecha','municipio', 'matricula', 'observacion',
            'area_construida', 'resultado_visita'
        )
        

    def get_departamento(self, obj):
       return 'Valle'
    
    def get_area_terreno(self, obj):
        try:
            instance_terreno = LcTerreno.objects.get(id_predio = obj)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return None
        return instance_terreno.area_total
    
    def get_area_construida(self, obj):
        try:
            instance_terreno = LcUnidadConstruccion.objects.get(id_predio = obj)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return None
        return instance_terreno.area_construida
    
    def get_direccion(self, obj):
        return getattr(obj, 'direccion_predio', '')

    def get_vigencia(self, obj):
        return '2025'

    def get_numero_predial(self, obj):
        return ''

    def get_destino(self, obj):
        variable = None
        if obj.id_destecono:
            variable = obj.id_destecono.desc_destecno
        return variable
    
    def get_analista(self, obj):
        try:
            instance_Asignacion = Asignacion.objects.get(predio = obj)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return None
        
        return instance_Asignacion.analista.username
    
    def get_coordinador(self, obj):
        try:
            instance_Asignacion = Asignacion.objects.get(predio = obj)
            if instance_Asignacion.coordinador:
                return instance_Asignacion.coordinador.username
            else:
                return None
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return None
    
    def get_fecha(sefl, obj):
        try:
            instance_Asignacion = Asignacion.objects.get(predio = obj)
            return instance_Asignacion.modified.strftime('%Y-%m-%d')
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return None
    
    def get_matricula(self, obj):
        return ''
    
    def get_resultado_visita(self, obj):
        instance_datos_levantamiento = LcDatosadicionaleslevcat.objects.filter(id_predio = obj.id_predio)
        if instance_datos_levantamiento.exists():
            instance_levantamiento = instance_datos_levantamiento.first().id_resultado
        return getattr(instance_levantamiento,'descri_resultado','')

    def get_estado(self, obj):
        variable = None
        if obj.estado_predio:
            variable = obj.estado_predio.nombre
        return variable
    
    def get_observacion(self, obj):
        estado = obj.estado_predio.id
        instance_trazabilidad = Trazabilidad.objects.filter(predio = obj, estado_trazabilidad__id = estado).order_by('-id')
        if instance_trazabilidad.exists():
            if instance_trazabilidad.first().observacion:
                return instance_trazabilidad.first().observacion
        return ''
    
    def get_municipio(self, obj):
        return 'Cali'
    
    def get_semana(self, obj):
        instance_asignacion = Asignacion.objects.filter(predio=obj)
        if instance_asignacion.exists():
            return instance_asignacion.first().semana
        return 0

    def get_fecha_trazabilidad(self, obj):
        instance_trazabilidad = Trazabilidad.objects.filter(predio=obj, estado_trazabilidad__id = obj.estado_predio.id).order_by('-id')
        if instance_trazabilidad.exists():
            timestamp = instance_trazabilidad.first().modified
            # Formatear el datetime solo a la fecha en formato YYYY-MM-DD
            date_str = timestamp.strftime("%Y-%m-%d")
            print(date_str,'deberia estar entrando aqui')
        else:
            timestamp = obj.updated_at
            date_str = timestamp.strftime("%Y-%m-%d")
            print(date_str,'Porque esta aqui')
        return date_str

    def get_departamento(self, obj):
        return 'VALLE'
    
    def get_comuna(self, obj):
        instance_npn = Npn.objects.filter(id_predio=obj)
        if instance_npn.exists():
            return instance_npn.first().comuna_id
        return ''

class DetailPredioSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    departamento = serializers.SerializerMethodField()
    destino = serializers.SerializerMethodField()
    estado = serializers.SerializerMethodField()
    municipio = serializers.SerializerMethodField()
    interesados = serializers.SerializerMethodField()
    matricula = serializers.SerializerMethodField()
    terrenos =  serializers.SerializerMethodField()
    unidades =  serializers.SerializerMethodField()
    direccion = serializers.SerializerMethodField()
    vigencia = serializers.SerializerMethodField()
    resultado_visita = serializers.SerializerMethodField()
    contacto_visita = serializers.SerializerMethodField()
    direccion_notificacion =serializers.SerializerMethodField()
    semana =serializers.SerializerMethodField()
    fecha_trazabilidad = serializers.SerializerMethodField()
    comuna = serializers.SerializerMethodField()
    
    class Meta:
        model = LcDcPredio
        fields = (
            'id','npn','comuna','direccion','direccion_notificacion', 'matricula', 'semana','vigencia','fecha_trazabilidad', 'estado', 'departamento', 'id_predio_maestra',
            'destino', 'estado', 'municipio', 'interesados', 'terrenos', 'unidades', 'resultado_visita', 'contacto_visita'
        )
    
    def get_related_objects_serializer_data(self, obj, related_path: str, model: QuerySet, serializer_class, field_query, value_list):
        """
        Método genérico para obtener datos serializados de objetos relacionados.

        Args:
        - obj: El objeto desde el cual se inicia la relación.
        - related_path: Cadena que especifica el camino a través de los modelos relacionados hasta el objetivo.
        - model: Modelo de Django del objeto objetivo.
        - serializer_class: Clase del serializer usado para serializar los objetos del modelo.

        Returns:
        - Datos serializados de los objetos relacionados.
        """
        related_ids = Tramite_catastral_historico.objects.filter(
            predio=obj,
            **{f'{related_path}__isnull': False}
        ).values_list(f'{value_list}', flat=True)

        query_fiedl = {
            field_query:related_ids
        }

        related_objects = model.objects.filter(**query_fiedl)
        serializer = serializer_class(related_objects, many=True)
        return serializer.data
    
    def get_resultado_visita(self, obj):
        instance_datosadicionales = LcDatosadicionaleslevcat.objects.filter(id_predio = obj.id_predio)
        if instance_datosadicionales.exists():
            return {
                'resultado_visita': instance_datosadicionales.first().id_resultado.descri_resultado,
                'observacion': instance_datosadicionales.first().observaciones
            }
        else:
            return {}

    def get_id(self, obj):
        return getattr(obj, 'id_predio', '')
    
    def get_semana(self, obj):
        instance_asignacion = Asignacion.objects.filter(predio=obj)
        if instance_asignacion.exists():
            return instance_asignacion.first().semana
        return 0

    def get_fecha_trazabilidad(self, obj):
        instance_trazabilidad = Trazabilidad.objects.filter(predio=obj, estado_trazabilidad__id = obj.estado_predio.id).order_by('-id')
        if instance_trazabilidad.exists():
            timestamp = instance_trazabilidad.first().modified
            # Formatear el datetime solo a la fecha en formato YYYY-MM-DD
            date_str = timestamp.strftime("%Y-%m-%d")
        else:
            timestamp = obj.updated_at
            date_str = timestamp.strftime("%Y-%m-%d")
        return date_str

    def get_departamento(self, obj):
        return 'VALLE'
    
    def get_comuna(self, obj):
        instance_npn = Npn.objects.filter(id_predio=obj)
        if instance_npn.exists():
            return instance_npn.first().comuna_id
        return ''

    def get_vigencia(self, obj):
        estado_predio = getattr(obj, 'estado_predio.id', None)
        if estado_predio == 2:
            return '2025'
        else:
            return '2024'

    def get_direccion(self, obj):
        return getattr(obj, 'direccion_predio', '')
    
    def get_direccion_notificacion(self, obj):
        return getattr(obj, 'direccion_notificacion', '')

    def get_destino(self, obj):
        variable = None
        if obj.id_destecono:
            variable = obj.id_destecono.desc_destecno
        return variable
    
    def get_matricula(self, obj):
        variable = ''
        # if obj.matricula:
        #     variable = f'{obj.matricula.orip.codigo}-{obj.matricula.numero_matricula}'
        return obj.matricula

    def get_estado(self, obj):
        variable = None
        if obj.estado_predio:
            variable = obj.estado_predio.nombre
        return variable
    
    def get_municipio(self, obj):
        return 'CALI'

    def get_interesados(self,obj):
        instance_derecho_predio = Derecho_predio.objects.filter(predio = obj)
        serializer = InteresadoPredioSerializer(instance_derecho_predio, many=True)
        return serializer.data

    def get_terrenos(self, obj):
        related_objects = LcTerreno.objects.filter(id_predio = obj)
        serializer = TerrenosZonasSerializer(related_objects, many=True)
        return serializer.data
    
    def get_unidades(self, obj):
        related_objects = LcUnidadConstruccion.objects.filter(id_predio = obj)
        serializer = CaracteristicasUnidadConstruccionSerializer(related_objects, many=True)
        return serializer.data
    
    def get_contacto_visita(self, obj):
        instance_contacto_visita = ContactoVisita.objects.filter(id_predio=obj.id_predio)
        if instance_contacto_visita.exists():
            return {
                'documento': instance_contacto_visita.first().num_doc_atendio,
                'primer_nombre': instance_contacto_visita.first().primer_nombre,
                'segundo_nombre': instance_contacto_visita.first().segundo_nombre,
                'primer_apellido': instance_contacto_visita.first().primer_apellido,
                'segundo_apellido': instance_contacto_visita.first().segundo_apellido,
                'celular': instance_contacto_visita.first().celular,
                'correo_electronico': instance_contacto_visita.first().correo_electronico,
                'relacion_predio': instance_contacto_visita.first().relacion_predio,
            }
        else:
            return {}
    