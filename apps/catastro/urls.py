from django.urls import path
from .views import FindPredioListApiView, DetailPredioListApiView, serve_local_images
from .control_calidad.views import FindPredioListEstadoApiView, CambiarEstado

urlpatterns = [
    path('list_predio/', FindPredioListApiView.as_view(), name='list_predio'),
    path('detail_predio/', DetailPredioListApiView.as_view(), name='detail_predio'),
    path('all_predios/', FindPredioListEstadoApiView.as_view(), name='all_predios'),
    path('update_predio/<int:pk>', CambiarEstado.as_view(), name='update_predio'),

    path('list_images/<int:idpredio>', serve_local_images, name='list_images'),

]