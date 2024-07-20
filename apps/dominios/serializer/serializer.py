from rest_framework import serializers
from apps.dominios.models import (
    LcRestricciontipo, LcInteresadodocumentotipo, LcInteresadotipo, LcSexotipo, LcGrupoetnicotipo,
    LcDominioconstrucciontipo, LcAnexotipo, LcUsoconstipo, LcConstrucciontipo, LcUnidadconstrucciontipo, LcConstruccionplantatipo,
    LcDestinacioneconomicatipo, LcResultadovisitatipo
    )
from apps.catastro.models import (
    Cat_clase, SdeEstado
)

class RestriccionTipoSerializer(serializers.ModelSerializer):
    restriccion_tipo = serializers.SerializerMethodField()
    class Meta:
        model = LcRestricciontipo
        fields = ('id_restricciontipo','restriccion_tipo',)

    def get_restriccion_tipo(self, obj):
        return obj.descr_restricciontipo
    
# SERIALIZER INTERESADOS

class DestinacionTipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LcDestinacioneconomicatipo
        fields = '__all__'

class ResultadoVisitaTipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LcResultadovisitatipo
        fields = '__all__'

class InteresadoDocumentoTipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LcInteresadodocumentotipo
        fields = '__all__'

class InteresadoTipoSerializer(serializers.ModelSerializer):

    class Meta:
        model = LcInteresadotipo
        fields = '__all__'

class SexoTipoSerializer(serializers.ModelSerializer):

    class Meta:
        model = LcSexotipo
        fields = '__all__'

class GrupoEtnicoTipoSerializer(serializers.ModelSerializer):

    class Meta:
        model = LcGrupoetnicotipo
        fields = '__all__'

# SERIALIZER UNIDADES

class LcDominioconstrucciontipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LcDominioconstrucciontipo
        fields = ('id_domconstipo', 'des_domconsttipo')

class LcAnexotipoSerializer(serializers.ModelSerializer):
    calificacion_anexo = serializers.SerializerMethodField()
    class Meta:
        model = LcAnexotipo
        fields = ('id_anexotipo', 'des_anexotipo', 'codigo','calificacion', 'calificacion_anexo')
    
    def get_calificacion_anexo(self, obj):
        return f'{obj.calificacion}-{obj.des_anexotipo}'

class LcUsoconstipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LcUsoconstipo
        fields = ('id_usocons', 'des_usocons')

class LcConstrucciontipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LcConstrucciontipo
        fields = ('id_constipo', 'des_consttipo')

class LcUnidadconstrucciontipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LcUnidadconstrucciontipo
        fields = ('id_undconstipo', 'des_undconsttipo')

class LcConstruccionplantatipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LcConstruccionplantatipo
        fields = ('id_constplantatipo', 'des_constplantatipo')

class LcConstruccionCalificacionSerializer(serializers.ModelSerializer):
    codcali = serializers.SerializerMethodField()
    codiestr = serializers.SerializerMethodField()
    detalle = serializers.SerializerMethodField()

    class Meta:
        model = Cat_clase
        fields = ('puntaje', 'codcali', 'codiestr', 'detalle')
    
    def get_codcali(self, obj):
        return obj.codcali.detalle
    
    def get_codiestr(self, obj):
        return obj.codiestr.detalle
    
    def get_detalle(self, obj):
        return obj.detalle.strip()

class SDEestadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SdeEstado
        fields = '__all__'
    
    