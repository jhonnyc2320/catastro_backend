# myapp/views.py

from rest_framework import generics, serializers, response
from apps.dominios.models import (
    LcRestricciontipo, LcInteresadodocumentotipo, LcInteresadotipo, LcSexotipo, LcGrupoetnicotipo,
    LcDominioconstrucciontipo, LcAnexotipo, LcUsoconstipo, LcConstrucciontipo, LcUnidadconstrucciontipo, LcConstruccionplantatipo,
    LcDestinacioneconomicatipo, LcResultadovisitatipo
)

from apps.catastro.models import Cat_clase, Cat_clase_clase, SdeEstado

from .serializer.serializer import (
    RestriccionTipoSerializer, InteresadoDocumentoTipoSerializer, InteresadoTipoSerializer,
    SexoTipoSerializer,GrupoEtnicoTipoSerializer, LcAnexotipoSerializer, LcConstruccionplantatipoSerializer,
    LcConstrucciontipoSerializer, LcDominioconstrucciontipoSerializer, LcUnidadconstrucciontipoSerializer, 
    LcUsoconstipoSerializer, LcConstruccionCalificacionSerializer, DestinacionTipoSerializer, ResultadoVisitaTipoSerializer,
    SDEestadoSerializer
)

class RestriccionTipoListView(generics.ListAPIView):
    queryset = LcRestricciontipo.objects.all()
    serializer_class = RestriccionTipoSerializer

class DestinacionEconomicaTipoListView(generics.ListAPIView):
    queryset = LcDestinacioneconomicatipo.objects.all()
    serializer_class = DestinacionTipoSerializer

class ResultadoVisitaTipoListView(generics.ListAPIView):
    queryset = LcResultadovisitatipo.objects.all()
    serializer_class = ResultadoVisitaTipoSerializer
# VISTAS INTERESADOS

class InteresadoDocumentoTipoListView(generics.ListAPIView):
    queryset = LcInteresadodocumentotipo.objects.all()
    serializer_class = InteresadoDocumentoTipoSerializer

class InteresadoTipoListView(generics.ListAPIView):
    queryset = LcInteresadotipo.objects.all()
    serializer_class = InteresadoTipoSerializer

class SexoTipoListView(generics.ListAPIView):
    queryset = LcSexotipo.objects.all()
    serializer_class = SexoTipoSerializer

class GrupoEtnicoTipoListView(generics.ListAPIView):
    queryset = LcGrupoetnicotipo.objects.all()
    serializer_class = GrupoEtnicoTipoSerializer

# VISTAS UNIDADES

class UnidadConstruccionDominiosListView(generics.ListAPIView):
    queryset = LcInteresadodocumentotipo.objects.all()
    serializer_class = InteresadoDocumentoTipoSerializer

    def list(self, request, *args, **kwargs):

        tipo_unidad = request.query_params.get('tipo_unidad')
        tipo_construccion = request.query_params.get('tipo_construccion')
        tipo_anexo = request.query_params.get('tipo_anexo')

        #QUERIES
        lcAnexotipo =  LcAnexotipo.objects.filter(des_anexotipo = tipo_anexo) if tipo_anexo else LcAnexotipo.objects.all()
        lcDominioconstrucciontipo =  LcDominioconstrucciontipo.objects.all()
        lcUsoconstipo = LcUsoconstipo.objects.filter(tipo_unidad = tipo_unidad) if tipo_unidad else LcUsoconstipo.objects.all()
        lcConstrucciontipo =  LcConstrucciontipo.objects.all()
        lcUnidadconstrucciontipo =  LcUnidadconstrucciontipo.objects.filter(tipo_cons=tipo_construccion) if tipo_construccion else LcUnidadconstrucciontipo.objects.all()
        lcConstruccionplantatipo =  LcConstruccionplantatipo.objects.all()

        #SERIAILZER
        lcAnexotipoSerializer = LcAnexotipoSerializer(lcAnexotipo, many=True)
        lcConstruccionplantatipoSerializer= LcConstruccionplantatipoSerializer(lcConstruccionplantatipo, many=True)
        lcConstrucciontipoSerializer= LcConstrucciontipoSerializer(lcConstrucciontipo, many=True)
        lcDominioconstrucciontipoSerializer= LcDominioconstrucciontipoSerializer(lcDominioconstrucciontipo, many=True)
        lcUnidadconstrucciontipoSerializer= LcUnidadconstrucciontipoSerializer(lcUnidadconstrucciontipo, many=True)
        lcUsoconstipoSerializer= LcUsoconstipoSerializer(lcUsoconstipo, many=True)

        #DICCIONARIO
        dict_data = {
            'anexo_tipo': lcAnexotipoSerializer.data,
            'construccion_planta_tipo': lcConstruccionplantatipoSerializer.data,
            'construccion_tipo':lcConstrucciontipoSerializer.data,
            'dominio_construccion':lcDominioconstrucciontipoSerializer.data,
            'unidad_construccion':lcUnidadconstrucciontipoSerializer.data,
            'uso':lcUsoconstipoSerializer.data,
        }

        return response.Response(dict_data)

class UnidadConstruccionCalificacionDominiosListView(generics.ListAPIView):
    queryset = LcInteresadodocumentotipo.objects.all()
    serializer_class = InteresadoDocumentoTipoSerializer

    def list(self, request, *args, **kwargs):
        
        cat_clas_detalle = request.query_params.get('cat_clas_detalle')

        #QUERIES
        lcCalificacion = Cat_clase.objects.filter(clase_clase__detalle = cat_clas_detalle) if cat_clas_detalle else Cat_clase.objects.all()

        #SERIAILZER
        lcCalificacionSerializer= LcConstruccionCalificacionSerializer(lcCalificacion, many=True)

        #DICCIONARIO
        dict_data = {
            'calificacion': lcCalificacionSerializer.data
        }

        return response.Response(dict_data)


class SDEestadoListView(generics.ListAPIView):
    queryset = SdeEstado.objects.all()
    serializer_class = SDEestadoSerializer