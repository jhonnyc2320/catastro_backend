from rest_framework import serializers
import zipfile
import csv
from collections import defaultdict
import openpyxl
import xlrd
from rest_framework import generics
from apps.catastro.models import Asignacion, LcDcPredio as Predio, LcTerreno, SdeEstado, LcDatosadicionaleslevcat
from apps.dominios.models import LcRestricciontipo
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datetime import datetime

from django.db import transaction

import pandas as pd
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from datetime import datetime
import os
from io import BytesIO

def generate_excel(data):
    # Convertir los datos a un DataFrame de pandas
    df = pd.DataFrame(data)

    # Crear un buffer en memoria
    buffer = BytesIO()

    # Guardar el DataFrame en el buffer
    df.to_excel(buffer, index=False, engine='openpyxl')
    
    # Definir el nombre del archivo
    filename = f"reporte_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    filepath = os.path.join('reportes', filename)
    
    # Guardar el contenido del buffer en el almacenamiento de Django
    buffer.seek(0)
    file = ContentFile(buffer.read())
    default_storage.save(filepath, file)
    
    return filename

class AsignacionSerializer(serializers.ModelSerializer):

    id_predio_maestra = serializers.SerializerMethodField()
    npn = serializers.SerializerMethodField()
    comuna = serializers.SerializerMethodField()
    analista = serializers.SerializerMethodField()
    coordinador = serializers.SerializerMethodField()
    resultado_visita = serializers.SerializerMethodField()
    observaciones = serializers.SerializerMethodField()
    fecha_visita = serializers.SerializerMethodField()
    resultado_efectivo = serializers.SerializerMethodField()
    fecha_reporte = serializers.SerializerMethodField()

    class Meta:
        model = Asignacion
        fields = (
            'id_predio_maestra', 'npn','comuna','analista','coordinador','resultado_visita','observaciones',
            'fecha_visita', 'resultado_efectivo', 'fecha_reporte', 'semana'
        )

    def get_id_predio_maestra(self, obj):
        return getattr(obj.predio,'id_predio_maestra',None)
    
    def get_npn(self, obj):
        return getattr(obj.predio,'npn','')
    
    def get_comuna(self, obj):
        npn = self.get_npn(obj)
        if npn:
            return npn[9:11]
        return ''
    
    def get_analista(self, obj):
        return getattr(obj.analista,'first_name','')
    
    def get_coordinador(self, obj):
        coordinador = getattr(obj,'coordinador',None)
        if coordinador:
            return getattr(coordinador,'first_name',None)
        return ''
    
    def get_resultado_visita(self, obj):
        instance_datos_adicionales = LcDatosadicionaleslevcat.objects.filter(id_predio = obj.predio)
        if instance_datos_adicionales.exists():
            return getattr(instance_datos_adicionales.first().id_resultado,'descri_resultado','')
        else:
            return ''
    
    def get_observaciones(self, obj):
        instance_datos_adicionales = LcDatosadicionaleslevcat.objects.filter(id_predio = obj.predio)
        if instance_datos_adicionales.exists():
            return getattr(instance_datos_adicionales.first(),'observaciones','')
        else:
            return ''
    
    def get_fecha_visita(self, obj):
        instance_predio = obj.predio
        return instance_predio.created_at.strftime('%Y-%m-%d')
    
    def get_resultado_efectivo(self, obj):
        if self.get_resultado_visita(obj) == 'Exitoso':
            return 'Efectivo'
        else:
            return 'No efectivo'
    
    def get_fecha_reporte(self, obj):
        return datetime.now().strftime("%Y-%m-%d")
    
    

class ReporteSerializer(serializers.Serializer):
    reporte = serializers.IntegerField()

    def validate(self, value):
        return value

    def create(self, validated_data):
        data = validated_data.get('reporte')
        
        if data == 1:
            instance_asignacion = Asignacion.objects.all().select_related('predio', 'analista', 'coordinador','predio__lcdatosadicionaleslevcat')
            serializer = AsignacionSerializer(instance_asignacion, many=True)
            reporte_data = serializer.data

            # Generar el archivo Excel
            filename = generate_excel(reporte_data)
            file_url = default_storage.url(filename)
            
            return {'file_url': filename}

        return data
