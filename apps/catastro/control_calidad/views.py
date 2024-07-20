from rest_framework import generics
from apps.catastro.serializer.serializer import FindPredioListSerializer
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.db.models import Q

from apps.catastro.serializer.serializer_edicion import Trazabilidad
from apps.catastro.models import Trazabilidad, Asignacion
from apps.users.models import Rol_predio

#MODELS
from apps.catastro.models import LcDcPredio as Predio, EstadoPredio, Asignacion

#PAGINATION
from apps.utils.pagination.ClassPagination import ListPrediosPagination

# PERMISSIONS
from ...utils.permission.permission import IsConsultaAmindUser, IsAnalistaControlAmindUser
from ...utils.middleware.CookiesJWTAuthentication import CookieJWTAuthentication

class FindPredioListEstadoApiView(generics.ListAPIView):
    serializer_class = FindPredioListSerializer
    pagination_class = ListPrediosPagination
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsConsultaAmindUser]
    
    def get_queryset(self):
        estado = self.request.query_params.get('estado_predio')
        npn_idpredio = self.request.query_params.get('npn_idpredio', None)
        user = self.request.user  # Obtener el usuario

        # Inicializar el diccionario con el estado
        dict_query = {
            'estado_predio': None,
        }
        
        # Condicional para agregar la clave adecuada
        if npn_idpredio:
            
            if len(npn_idpredio) == 30:
                dict_query['npn'] = npn_idpredio
            else:
                dict_query['id_predio_maestra'] = npn_idpredio

        if estado:
            instance_rol_predio = Rol_predio.objects.filter(user = user).values_list('rol__name', flat=True)
            
            list_predios_id = []
            
            if 'Admin' in instance_rol_predio:
                list_predios_id = Asignacion.objects.all().values_list('predio__id_predio', flat=True)
            
            elif 'Analista' in instance_rol_predio and 'Control_calidad' in instance_rol_predio:
                
                # Filtrar predios asignados al usuario como analista o coordinador
                list_predios_id = Asignacion.objects.filter(
                    Q(analista=user) | Q(coordinador=user)
                ).values_list('predio__id', flat=True)
            
            elif 'Control_calidad' in instance_rol_predio:
                list_predios_id = Asignacion.objects.filter(coordinador = user).values_list('predio__id_predio', flat=True)
            
            elif 'Analista' in instance_rol_predio:
                list_predios_id = Asignacion.objects.filter(analista = user).values_list('predio__id_predio', flat=True)
                
            else:
                return Predio.objects.none()
            
            dict_query['id_predio__in'] = list_predios_id

            try:
                instance_estadopredio = EstadoPredio.objects.get(nombre=estado)
                dict_query['estado_predio'] = instance_estadopredio
                return Predio.objects.filter(**dict_query)
            except MultipleObjectsReturned:
                return Predio.objects.none()
            except ObjectDoesNotExist:
                return Predio.objects.none()
        return Predio.objects.all()

class CambiarEstado(generics.UpdateAPIView):
    queryset = Predio.objects.all()
    serializer_class = FindPredioListSerializer
    pagination_class = ListPrediosPagination
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAnalistaControlAmindUser]

    def partial_update(self, request, *args, **kwargs):
        predio_id = kwargs.get('pk')
        nuevo_estado_nombre = request.data.get('estado')
        observacion = request.data.get('observacion')
        
        predio = None
        try:
            predio = Predio.objects.get(pk=predio_id)
        except Predio.DoesNotExist:
            raise NotFound('Predio no encontrado')
        
        instance_asignacion = None
        try:
            instance_asignacion = Asignacion.objects.get(predio=predio_id, coordinador__isnull = False)
        except Asignacion.DoesNotExist:
            raise serializers.ValidationError(f'El predio {predio.npn} debe tener un coordinador.')

        try:
            nuevo_estado = EstadoPredio.objects.get(nombre=nuevo_estado_nombre)
        except EstadoPredio.DoesNotExist:
            return Response({'error': 'Estado no encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        
        instance_trazabilidad = Trazabilidad.objects.filter(predio = predio).order_by('-id')
        if instance_trazabilidad.exists():
            instance_trazabilidad_first = instance_trazabilidad.first()
            if nuevo_estado.id == instance_trazabilidad_first.estado_trazabilidad.id:
                raise serializers.ValidationError(f'El predio {predio.npn} esta en este estado.') 
        
        data_trazabilidad = {
            'predio':predio,
            'analista':instance_asignacion.analista,
            'coordinador': instance_asignacion.coordinador,
            'estado_trazabilidad': nuevo_estado,
            'observacion': observacion if observacion else None
        }
        Trazabilidad.objects.create(**data_trazabilidad)

        predio.estado_predio = nuevo_estado
        predio.save()

        return Response('Predio actualizado con exito')

