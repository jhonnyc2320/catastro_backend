"""setup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.login.views import (CustomTokenObtainPairView, VerifyAuthView, 
                              LogoutView, VerifyAuthCalidadView, VerifyAuthAnalistaView,
                              VerifyAuthAnalistaEstadoPredioView
                              )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('apps.users.urls')),
    path('catastro/', include('apps.catastro.urls')),
    path('gestion/', include('apps.gestion.urls')),
    path('reportes/', include('apps.reportes.urls')),
    path('dominios/', include('apps.dominios.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/verify/', VerifyAuthView.as_view(), name='verify-auth'),
    path('api/auth/verify_calidad/', VerifyAuthCalidadView.as_view(), name='verify-auth-calidad'),
    path('api/auth/verify_analista/', VerifyAuthAnalistaView.as_view(), name='verify-auth-analista'),
    path('api/auth/verify_analista_predio/', VerifyAuthAnalistaEstadoPredioView.as_view(), name='verify_analista_predio'),
]
