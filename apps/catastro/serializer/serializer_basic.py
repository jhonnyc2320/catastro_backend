from rest_framework import serializers
from apps.catastro.models import LcTerreno, LcUnidadConstruccion, Derecho_predio, Lc_puntaje

class InteresadoPredioSerializer(serializers.ModelSerializer):
    id_interesado = serializers.SerializerMethodField()
    nombre = serializers.SerializerMethodField()
    documento_identidad = serializers.SerializerMethodField()
    tipo_documento = serializers.SerializerMethodField()
    tipo_interesado = serializers.SerializerMethodField()
    primer_nombre = serializers.SerializerMethodField()
    segundo_nombre = serializers.SerializerMethodField()
    primer_apellido = serializers.SerializerMethodField()
    segundo_apellido = serializers.SerializerMethodField()
    razon_social = serializers.SerializerMethodField()
    sexo = serializers.SerializerMethodField()
    etnia = serializers.SerializerMethodField()
    id_predio = serializers.SerializerMethodField()
    telefono_uno = serializers.SerializerMethodField()
    telefono_dos = serializers.SerializerMethodField()
    correo_electronico = serializers.SerializerMethodField()
    
    class Meta:
        model = Derecho_predio
        fields = (
            'id_interesado','id','documento_identidad','tipo_documento','tipo_interesado','nombre', 'fraccion_derecho',
            'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'razon_social',
            'sexo','etnia', 'id_predio', 'telefono_uno', 'telefono_dos', 'correo_electronico'
        )
    
    def get_telefono_uno(self, obj):
        datos = 0
        if obj.interesado:
            predio = obj.interesado
            datos =  predio.telefono_uno
        return datos

    def get_telefono_dos(self, obj):
        datos = 0
        if obj.interesado:
            predio = obj.interesado
            datos =  predio.telefono_dos
        return datos

    def get_correo_electronico(self, obj):
        datos = ''
        if obj.interesado:
            predio = obj.interesado
            datos =  predio.correo_electronico
        return datos

    def get_id_predio(self, obj):
        id = None
        if obj.predio:
            predio = obj.predio
            id =  predio.id_predio
        return id

    def get_id_interesado(self, obj):
        id = None
        if obj.interesado:
            interesado = obj.interesado
            id =  interesado.id
        return id

    def get_primer_nombre(self, obj):
        nombre = None
        if obj.interesado:
            interesado = obj.interesado
            nombre =  interesado.primer_nombre 
        return nombre

    def get_segundo_nombre(self, obj):
        nombre = None
        if obj.interesado:
            interesado = obj.interesado
            nombre =  interesado.segundo_nombre 
        return nombre 

    def get_primer_apellido(self, obj):
        nombre = None
        if obj.interesado:
            interesado = obj.interesado
            nombre =  interesado.primer_apellido 
        return nombre
    
    def get_segundo_apellido(self, obj):
        nombre = None
        if obj.interesado:
            interesado = obj.interesado
            nombre =  interesado.segundo_apellido 
        return nombre
    
    def get_razon_social(self, obj):
        nombre = None
        if obj.interesado:
            interesado = obj.interesado
            nombre =  interesado.razon_social 
        return nombre 
    
    def get_nombre(self,obj):
        nombre = None
        if obj.interesado:
            interesado = obj.interesado
            list_nombres = [
                interesado.primer_nombre,
                interesado.segundo_nombre,
                interesado.primer_apellido,
                interesado.segundo_apellido,
                interesado.razon_social
            ]
            nombre = ' '.join(filter(None, list_nombres))
        return nombre

    def get_documento_identidad(self,obj):
        variable = None
        if obj.interesado:
            interesado = obj.interesado
            variable = interesado.documento_identidad
        return variable

    def get_tipo_documento(self,obj):
        variable = None
        if obj.interesado:
            interesado = obj.interesado
            tipo_documento = interesado.id_tipodoc
            if tipo_documento:
                variable = tipo_documento.des_tipodoc
        return variable

    def get_tipo_interesado(self,obj):
        variable = None
        if obj.interesado:
            interesado = obj.interesado
            tipo_interesado = interesado.id_interesadotipo
            if tipo_interesado:
                variable = tipo_interesado.des_interesadotipo
        return variable
    
    def get_sexo(self,obj):
        variable = None
        if obj.interesado:
            interesado = obj.interesado
            tipo_interesado = interesado.id_genero
            if tipo_interesado:
                variable = tipo_interesado.des_genero
        return variable
    
    def get_etnia(self,obj):
        variable = None
        if obj.interesado:
            interesado = obj.interesado
            tipo_interesado = interesado.id_etnia
            if tipo_interesado:
                variable = tipo_interesado.des_etnia
        return variable

class TerrenosZonasSerializer(serializers.ModelSerializer):
    restriccion_tipo = serializers.SerializerMethodField()

    class Meta:
        model = LcTerreno
        fields = (
            'id_terreno','id_predio','area_total','area_comun', 'restriccion_tipo'
        )

    def get_restriccion_tipo(self, obj):
        id_rest_servi = getattr(obj, 'id_rest_servi', '')
        if id_rest_servi:
            return id_rest_servi.descr_restricciontipo
        else:
            return ''

class CalificacionSerializer(serializers.ModelSerializer):
    codcali = serializers.SerializerMethodField()
    codiestru = serializers.SerializerMethodField()
    codiclas = serializers.SerializerMethodField()

    class Meta:
        model = Lc_puntaje
        fields = (
            'puntaje', 'codcali', 'codiestru', 'codiclas'
        )
    
    def get_codcali(self, obj):
        return obj.codcali.detalle
    
    def get_codiestru(self, obj):
        return obj.codiestru.detalle
    
    def get_codiclas(self, obj):
        return obj.codiclas.detalle

class CaracteristicasUnidadConstruccionSerializer(serializers.ModelSerializer):
    construccion_planta_tipo = serializers.SerializerMethodField()
    construccion_tipo = serializers.SerializerMethodField()
    dominio_construccion_tipo = serializers.SerializerMethodField()
    uso = serializers.SerializerMethodField()
    total_banios = serializers.SerializerMethodField()
    puntaje = serializers.SerializerMethodField()
    area_construida = serializers.SerializerMethodField()
    construccion_planta_tipo = serializers.SerializerMethodField()
    construccion_tipo = serializers.SerializerMethodField()
    dominio_construccion_tipo = serializers.SerializerMethodField()
    uso = serializers.SerializerMethodField()
    identificador = serializers.SerializerMethodField()
    unidad_construccion_tipo = serializers.SerializerMethodField()
    anexo_tipo = serializers.SerializerMethodField()
    calificacion = serializers.SerializerMethodField()
    estado_unidad = serializers.SerializerMethodField()
    
    class Meta:
        model = LcUnidadConstruccion
        fields = (
            'id_construccion','identificador','planta_ubicacion','total_habitaciones','total_banios', 'total_locales','total_pisos','anio_construccion',
            'area_construida', 'puntaje','construccion_planta_tipo','construccion_tipo','dominio_construccion_tipo', 'uso',
            'numero_mezanines', 'numero_sotanos', 'unidad_construccion_tipo', 'anexo_tipo','area_construida_comun', 'id_predio', 'calificacion', 'estado_unidad'
        )

    def get_identificador(self, obj):
        return obj.id_unidad
    
    def get_area_construida(self, obj):
        return str(obj.area_construida)

    def get_construccion_tipo(self, obj):
        return getattr(obj.id_constipo,'des_consttipo', '')

    def get_dominio_construccion_tipo(self, obj):
        return getattr(obj.dominio_construccion_tipo,'dispname', '')
    
    def get_total_banios(self, obj):
        return obj.total_banos
    
    def get_puntaje(self, obj):
        return obj.total_puntaje
    
    def get_calificacion(self,obj):
        instance_calificaion = Lc_puntaje.objects.filter(id_unidad=obj)
        if instance_calificaion.exists():
            return CalificacionSerializer(instance_calificaion, many =True).data
        else:
            return []
    
    def get_construccion_planta_tipo(self, obj):
        return getattr(obj.id_constplantatipo, 'des_constplantatipo', '')
    
    def get_dominio_construccion_tipo(self, obj):
        return getattr(obj.id_domconstipo, 'des_domconsttipo', '')
    
    def get_uso(self, obj):
        return getattr(obj.id_usocons, 'des_usocons', '')
    
    def get_unidad_construccion_tipo(self, obj):
        return getattr(obj.id_undconstipo, 'des_undconsttipo', '')
    
    def get_estado_unidad(self, obj):
        return obj.retirado.desc_estado

    def get_anexo_tipo(self, obj):
        instance_unidad = LcUnidadConstruccion.objects.get(id_construccion=obj.id_construccion)
        # Verificar si la relación id_anexotipo existe
        if instance_unidad.id_anexotipo_id is not None:  # Usar id_anexotipo_id para verificar la existencia de la relación
            id_anexotipo = instance_unidad.id_anexotipo
            codigo =  f'{id_anexotipo.calificacion}-{id_anexotipo.des_anexotipo}'
        else:
            codigo = ''
        # instance_anexo_tipo = obj.id_anexotipo
        # if instance_anexo_tipo:
        #     return f'{instance_anexo_tipo.calificacion}-{instance_anexo_tipo.des_anexotipo}'
        # else:
        return codigo