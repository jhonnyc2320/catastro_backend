# myapp/urls.py

from django.urls import path
from .views import (
    RestriccionTipoListView, InteresadoDocumentoTipoListView, InteresadoTipoListView,
    SexoTipoListView, GrupoEtnicoTipoListView, UnidadConstruccionDominiosListView, UnidadConstruccionCalificacionDominiosListView,
    DestinacionEconomicaTipoListView, ResultadoVisitaTipoListView, SDEestadoListView
)

urlpatterns = [
    
    #URL TERRENOS
    path('restriccion_tipo/', RestriccionTipoListView.as_view(), name='restriccion_tipo'),

    # URL INTERESADOS
    path('interesado_documento/', InteresadoDocumentoTipoListView.as_view(), name='interesado_documento'),
    path('interesado_tipo/', InteresadoTipoListView.as_view(), name='interesado_tipo'),
    path('sexo_tipo/', SexoTipoListView.as_view(), name='sexo_tipo'),
    path('grupo_etnico/', GrupoEtnicoTipoListView.as_view(), name='grupo_etnico'),
    path('destinos/', DestinacionEconomicaTipoListView.as_view(), name='destinos'),
    path('resultado_visita/', ResultadoVisitaTipoListView.as_view(), name='resultado_visita'),
    path('sde_estado/', SDEestadoListView.as_view(), name='sde_estado'),
    path('unidad_dominios/', UnidadConstruccionDominiosListView.as_view(), name='unidad_dominios'),
    path('unidad_dominios_calificacion/', UnidadConstruccionCalificacionDominiosListView.as_view(), name='unidad_dominios_calificacion'),

]