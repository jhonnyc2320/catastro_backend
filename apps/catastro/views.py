from rest_framework import response, generics, serializers
from apps.catastro.serializer.serializer import FindPredioListSerializer, DetailPredioSerializer
import re
from django.db.models import F, Value, Q, CharField
from django.db.models.functions import Concat, Lower, Replace

#MODELS
from apps.catastro.models import LcDcPredio as Predio, Interesado 

#PAGINATION
from apps.utils.pagination.ClassPagination import ListPrediosPagination

# PERMISSIONS
from ..utils.permission.permission import IsConsultaAmindUser
from ..utils.middleware.CookiesJWTAuthentication import CookieJWTAuthentication


class FindPredioListApiView(generics.ListAPIView):
    serializer_class = FindPredioListSerializer
    pagination_class = ListPrediosPagination
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsConsultaAmindUser]

    def buscar_persona(self, nombre_completo):
        palabras = nombre_completo.split()  # Divide el nombre completo en palabras
        q_objects = Q()  # Inicializa un Q object vacío para acumular condiciones de búsqueda
        # Genera condiciones de búsqueda para cada palabra en todas las posiciones de nombre/apellido
        for palabra in palabras:
            q_objects |= Q(derecho_predio__interesado__primer_nombre__istartswith=palabra) | Q(derecho_predio__interesado__segundo_nombre__istartswith=palabra) | \
                        Q(derecho_predio__interesado__primer_apellido__istartswith=palabra) | Q(derecho_predio__interesado__segundo_apellido__istartswith=palabra)
        
        resultados = Predio.objects.filter(q_objects).distinct()
        return resultados
    
    def buscar_interesado(self, nombre_completo):

        texto_sin_espacios = re.sub(r"\s+", "", nombre_completo)
        # Queryset that annotates a new field 'full_name' by concatenating the desired fields
        interesados = Interesado.objects.annotate(
            full_name=Lower(Concat(
                F('primer_nombre'), Value(''),  # Value('') adds no separator between names
                F('segundo_nombre'), Value(''),
                F('primer_apellido'),Value(''),
                F('segundo_apellido'),Value(''),
                F('razon_social'),
                output_field=CharField(),
            ))
        ).annotate(
            # Remove spaces from the concatenated field for comparison
            full_name_no_spaces=Replace('full_name', Value(' '), Value(''))
        ).filter(
            full_name_no_spaces__startswith=texto_sin_espacios
        )

        return interesados

    def get_queryset(self):
        parametro = self.request.query_params.get('parametro','')
        valor = self.request.query_params.get('valor','')

        if not parametro or not valor:
            return Predio.objects.none()

        if parametro == 'npn': 
            # queryset = Predio.objects.filter(npn__startswith = valor, estado__in=(1,2,4)).order_by('npn')
            queryset = Predio.objects.filter(npn__startswith = valor).order_by('npn')

        elif parametro == 'matricula':
            try:
                orip, matricula_numero = valor.split("-")
                queryset = Predio.objects.filter(matricula__orip=orip, matricula__numero_matricula=matricula_numero, estado__in=(1,2,4))
            except ValueError:
                # Si el valor no se puede dividir correctamente, retorna un QuerySet vacío
                return Predio.objects.none()
        elif parametro == 'documento_identidad':
            queryset = Predio.objects.filter(derecho_predio__interesado__documento_identidad__startswith=valor, estado__id__in=(1,2,4))
        elif parametro == 'nombres':
            try:
                interesado_ids = self.buscar_interesado(valor)
                queryset = Predio.objects.filter(derecho_predio__interesado__id__in=interesado_ids).distinct()
            except ValueError:
                # Si el valor no se puede dividir correctamente, retorna un QuerySet vacío
                return Predio.objects.none()

        else:
            return Predio.objects.none()
        
        return queryset.order_by('npn') if queryset.exists() else Predio.objects.none()
    

class DetailPredioListApiView(generics.ListAPIView):
    serializer_class = DetailPredioSerializer
    queryset = Predio.objects.all()[:10]
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsConsultaAmindUser]

    def list(self, request):
        id_predio = request.query_params.get('id_predio')
        instance_predio = Predio.objects.filter(id_predio=id_predio)
        if instance_predio.exists() == False:
            raise serializers.ValidationError('No existe informacion para el predio') 
        serializer = self.serializer_class(instance_predio.first())
        return response.Response(serializer.data)


import os
from django.http import JsonResponse

def serve_local_images(request,idpredio):
    path_carpeta = r'C:\Users\User\webservices\PERSONAL_APIRESTMySQL_Python_v2 (1)2024\app\uploads\4361'  # Ruta base a la carpeta de imágenes
    # Convertir idpredio a cadena (str) para asegurar que sea un texto
    idpredio_str = str(idpredio)
    
    # Utilizar os.path.join para concatenar de manera segura las partes de la ruta
    images_folder = os.path.join(path_carpeta, idpredio_str)
    
    # Normalizar la ruta resultante para asegurar que sea válida en Windows
    images_folder = path_carpeta
    print(images_folder)
    try:
        # Obtener la lista de archivos (imágenes) en la carpeta
        images_list = [f for f in os.listdir(images_folder) if os.path.isfile(os.path.join(images_folder, f))]
        return JsonResponse({'images': images_list})
    except FileNotFoundError:
        return JsonResponse({'error': 'Carpeta no encontrada'}, status=404)