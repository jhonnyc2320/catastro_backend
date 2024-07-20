from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers, generics
from .serializer.construccion_json import ZipFileSerializer, ReadExcelAsignacion, CargueDatosSerializer # Asegúrate de que el path a los serializers esté correcto
from .serializer.serializer_cargar_datos_movil import CargarDatosMovilSerializer

from apps.users.models import User
import json

from apps.catastro.models import (
        LcDcPredio as Predio, EstadoPredio, SdeTipoPredio, SdeEstado, 
        LcTerreno, LcUnidadConstruccion, LcDatosadicionaleslevcat, FuenteAdmon, Municipio, Derecho_predio, Interesado,
        FuentePredio, ContactoVisita, Asignacion, Npn, Unidad_puntaje
    )
from apps.dominios.models import (
        LcPrediotipo, LcCondicionprediotipo, LcClasesuelotipo, 
        LcDestinacioneconomicatipo, LcRestricciontipo,
        LcConstruccionplantatipo, LcConstrucciontipo, LcDominioconstrucciontipo,LcUsoconstipo, LcUnidadconstrucciontipo,
        LcResultadovisitatipo, LcFuenteadministrativatipo, Adquisicion, EnteEmisor, ColEstadodisponibilidadtipo, LcDerechotipo,
        LcInteresadotipo, LcInteresadodocumentotipo, LcSexotipo, LcGrupoetnicotipo
    )

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import transaction

from django.db.models import Max
from django.utils import timezone

class CargueDatosMovilListCreateView(generics.ListCreateAPIView):
    queryset = Predio.objects.all()
    serializer_class = CargarDatosMovilSerializer

    def create(self, request, *args, **kwargs):
        
        data = request.data
        serializer = self.serializer_class(data = {'data':data})
        if serializer.is_valid():
            data = serializer.save()
            return Response(data)
        else:
            return Response(serializer.errors)

class FileCargueDatosMovilListCreateView(generics.ListCreateAPIView):
    queryset = Predio.objects.all()
    serializer_class = CargarDatosMovilSerializer

    def create(self, request, *args, **kwargs):
        
        # Obtener el archivo de la solicitud
        json_file = request.data.get('file')
        if not json_file:
            return Response({'error': 'No se suministrado algun archivo'}, status=400)
        
        # Leer y decodificar el contenido del archivo JSON
        file_data = json_file.read().decode('utf-8')
        data = json.loads(file_data)

        # Verificar que data es un array de objetos
        if not isinstance(data, list):
            return Response({'error': 'El json es invalido, se espera una lista'}, status=400)

        serializer = self.serializer_class(data = {'data':data})

        if serializer.is_valid():
            data_message = serializer.save()
            return Response(data_message)
        else:
            return Response(serializer.errors)    
