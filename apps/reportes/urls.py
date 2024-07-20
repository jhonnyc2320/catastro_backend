from django.urls import path
from .views import GenerarReportes


urlpatterns = [
    path('generar_reportes/', GenerarReportes.as_view(), name='generar_reportes'),
] 