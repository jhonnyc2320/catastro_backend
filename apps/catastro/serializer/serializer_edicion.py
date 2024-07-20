from rest_framework import serializers
from apps.catastro.models import Trazabilidad

class TrazabilidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trazabilidad
        fields = ['analista', 'coordinador', 'predio', 'estado_trazabilidad', 'observacion']

    def create(self, validated_data):
        return Trazabilidad.objects.create(**validated_data)