from django.contrib.gis.db import models

# utilities
from apps.utils.models import BaseModel

# dominios
from apps.catastro import models as models_catastro


class EstadoPredio(models.Model):
    nombre= models.CharField(max_length=10)
    descripcion = models.CharField(max_length=100)

class FuenteAdmon(models.Model):
    estado = models.ForeignKey(EstadoPredio, models.DO_NOTHING)
    predio = models.ForeignKey(models_catastro.LcDcPredio, models.DO_NOTHING, db_column='id_predio')
    derecho_predio = models.ForeignKey(models_catastro.Derecho_predio, models.DO_NOTHING)
    terreno = models.ForeignKey(models_catastro.LcTerreno, models.DO_NOTHING, db_column='id_terreno')
    unidad_construccion = models.ForeignKey(models_catastro.LcUnidadConstruccion, models.DO_NOTHING, db_column='id_construccion')
   
    class Meta:
        managed = False
        db_table = 'historia'