from django.urls import path
from .views import ZipUploadView, ReadExcelAsignacionView, EditarCrearAPIView
from .views_create_predio import CargueDatosMovilListCreateView, FileCargueDatosMovilListCreateView

urlpatterns = [
    path('cargar_datos/', ZipUploadView.as_view(), name='cargar_datos'),
    path('asignacion/', ReadExcelAsignacionView.as_view(), name='asignacion'),

    # CARGAR DATOS DESDE LA APLICACION MOVIL
    path('cargar_datos_movil/', CargueDatosMovilListCreateView.as_view(), name='cargar_datos_movil'),
    path('upload-json/', FileCargueDatosMovilListCreateView.as_view(), name='upload-json'),

    # URL PARA LA EDICION Y CREACION DE DATOS
    path('editar_crear_predio/', EditarCrearAPIView.as_view(), name='editar_crear_predio'),
]