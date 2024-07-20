from rest_framework import serializers
import zipfile
import csv
from collections import defaultdict
import openpyxl
import xlrd
from rest_framework import generics
from apps.catastro.models import Asignacion, LcDcPredio as Predio, LcTerreno, SdeEstado
from apps.dominios.models import LcRestricciontipo
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from decimal import Decimal, InvalidOperation
from django.db.models import Max
from .funciones_edicion import function_create_terreno, function_create_interesado, function_create_unidades, funtion_create_general
from django.db import transaction

class EditarCrearPredioSerializer(serializers.Serializer):
    data = serializers.JSONField()

    def validate(self, value):
        return value
    
    def get_instance_predio(self, id_predio):
        try:
            return Predio.objects.get(id_predio=id_predio)
        except Predio.DoesNotExist:
            return None
    

    def create(self, validated_data):
        data = validated_data.get('data')
        id_predio = data.get('id_predio')
        entidad = validated_data.get('data').get('entidad')
        # Obtener la instancia de predio
        instance_predio = self.get_instance_predio(id_predio)
        if not instance_predio:
            raise serializers.ValidationError('Predio no encontrado')

        response = {}
        with transaction.atomic():
            if entidad == 'terreno':
                response = function_create_terreno.create_editar_terreno(data, instance_predio)
            elif entidad == 'interesado':
                response = function_create_interesado.create_editar_interesado(data, instance_predio)
            elif entidad == 'unidad':
                response = function_create_unidades.create_editar_unidad(data, instance_predio)
            elif entidad == 'general':
                response = funtion_create_general.create_editar_general(data, instance_predio)
            else:
                print('No se ha suministrado nada')

        return response
