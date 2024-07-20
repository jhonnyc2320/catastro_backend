from rest_framework import generics, status, response
from rest_framework.response import Response
from .serializers import ReporteSerializer
from collections import defaultdict
from django.conf import settings
from django.http import HttpResponse
import os

# PERMISSIONS
from ..utils.permission.permission import IsControlAmindUser
from ..utils.middleware.CookiesJWTAuthentication import CookieJWTAuthentication

class GenerarReportes(generics.ListAPIView):
    serializer_class = ReporteSerializer
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsControlAmindUser]

    def list(self, request, *args, **kwargs):
        reporte = request.query_params.get('reporte')
        serializer = self.serializer_class(data = {'reporte':reporte})
        if serializer.is_valid():
            filename = serializer.save().get('file_url')
            file_url = os.path.join(settings.MEDIA_ROOT,'reportes', filename)
            if os.path.exists(file_url):
                with open(file_url, 'rb') as excel:
                    response = HttpResponse(excel.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                    response['Content-Disposition'] = f'attachment; filename={filename}'
                    return response
            return Response({'error': 'File does not exist'}, status=status.HTTP_404_NOT_FOUND)
        return response.Response(serializer.errors)