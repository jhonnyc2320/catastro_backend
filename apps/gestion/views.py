from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers, generics
from .serializer.construccion_json import ZipFileSerializer, ReadExcelAsignacion, CargueDatosSerializer # Asegúrate de que el path a los serializers esté correcto
from.serializer.serializer_edicion import EditarCrearPredioSerializer
from collections import defaultdict

from apps.catastro.models import Asignacion, LcDcPredio as Predio
from apps.users.models import User, Rol_predio
from django.utils import timezone

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

# PERMISSIONS
from ..utils.permission.permission import IsConsultaAmindUser
from ..utils.middleware.CookiesJWTAuthentication import CookieJWTAuthentication


class ZipUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ZipFileSerializer(data=request.FILES)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditarCrearAPIView(APIView):
    serializer_class = EditarCrearPredioSerializer
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsConsultaAmindUser]

    def post(self, request, *args, **kwargs):
        data = {'data':request.data}
        user = request.user
        # Serializa manualmente los atributos del usuario
        user_data = {
            'user':{
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        }
        data.get('data').update(user_data)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer_data = serializer.save()
            return Response(serializer_data, status=status.HTTP_200_OK)
        return Response(serializer.errors)

class ReadExcelAsignacionView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ReadExcelAsignacion(data=request.data)
        if serializer.is_valid():
            excel_json = serializer.data
            list_npn = [ data.get('npn') for data in excel_json.get('data') ]

            instance_predios = Predio.objects.filter(npn__in=list_npn).values_list('npn', 'estado_predio')

            estado_predios = defaultdict(set)
            for npn, estado_predio in instance_predios:
                estado_predios[npn].add(estado_predio)
            
            predios_errores = []
            predios_validos = []
            for npn, estados in estado_predios.items():
                if estados == {1, 2}:
                    predios_validos.append(npn)
                else:
                    predios_errores.append(npn)
            
            # Iterar sobre los predios válidos y actualizar la tabla Asignacion
            for valid_npn in predios_validos:
                
                # Obtener el coordinador del JSON del Excel para el npn actual
                coordinador = next((item['coordinador'] for item in excel_json.get('data') if item['npn'] == valid_npn), None)

                try:
                    instance_user = User.objects.get(email = coordinador, is_verified = True)
                except ObjectDoesNotExist:
                    raise serializers.ValidationError(f"El usuario con el correo {coordinador} no existe o no está verificado.")
                except MultipleObjectsReturned:
                    raise serializers.ValidationError(f"Hay múltiples usuarios con el correo {coordinador}.")
                
                #   verificar que el usuario tenga rol coordinador
                try:
                    instance_rol_predio = Rol_predio.objects.get(user = instance_user, rol__name = 'Control_calidad')
                except ObjectDoesNotExist:
                    raise serializers.ValidationError(f"El usuario con el correo {coordinador} no tiene un rol de Control_calidad asignado.")
                except MultipleObjectsReturned:
                    raise serializers.ValidationError(f"Hay múltiples usuarios con el correo {coordinador} y el rol Control_calidad.")
                
                if coordinador:
                    try:
                        # Obtener el id_predio del npn actual
                        id_predio = Predio.objects.get(npn=valid_npn, estado_predio = 2).id_predio

                        # Actualizar la entrada en la tabla Asignacion
                        Asignacion.objects.filter(predio=id_predio).update(
                            coordinador_id=instance_user,
                            modified=timezone.now()
                        )
                    except Predio.DoesNotExist:
                        predios_errores.append(valid_npn)  # Si el predio no existe, agregar a predios_errores

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)