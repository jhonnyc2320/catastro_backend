from django.contrib.gis.db import models 

# Create your models here.

# MODELOS [CARTOGRAFICOS]
class Adquisicion(models.Model):
    id_adquisicion = models.CharField(unique=True, max_length=30, primary_key=True)
    des_adquisicion = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'adquisicion'

class EnteEmisor(models.Model):
    id_ente_emisor = models.IntegerField(unique=True, primary_key=True)
    des_ente_emisor = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'ente_emisor'

class EstadoInteresado(models.Model):
    id_estinter = models.CharField(unique=True, max_length=30, primary_key=True)
    des_estinter = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estado_interesado'

class ColEstadodisponibilidadtipo(models.Model):
    id_estadodispo = models.IntegerField(unique=True, primary_key=True)
    des_estadodispo = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'col_estadodisponibilidadtipo'

class LcAnexotipo(models.Model):
    id_anexotipo = models.IntegerField(unique=True, primary_key=True)
    des_anexotipo = models.CharField(max_length=30)
    codigo = models.CharField(max_length=3)
    calificacion = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'lc_anexotipo'

class LcCalificartipo(models.Model):
    id_calificartipo = models.IntegerField(unique=True, primary_key=True)
    des_calificartipo = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'lc_calificartipo'
    

class LcClasecalificaciontipo(models.Model):
    id_clacaltipo = models.AutoField(primary_key=True)
    des_clacaltipo = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'lc_clasecalificaciontipo'


class LcClasesuelotipo(models.Model):
    id_clasesuelo = models.CharField(primary_key=True, max_length=30)
    desc_clasesuelo = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'lc_clasesuelotipo'


class LcCondicionprediotipo(models.Model):
    id_condprediotipo = models.CharField(primary_key=True, max_length=30)
    desc_condprediotipo = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'lc_condicionprediotipo'


class LcConstruccionplantatipo(models.Model):
    id_constplantatipo = models.IntegerField(primary_key=True)
    des_constplantatipo = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'lc_construccionplantatipo'


class LcConstrucciontipo(models.Model):
    id_constipo = models.IntegerField(primary_key=True)
    des_consttipo = models.CharField(max_length=30)
    
    class Meta:
        managed = False
        db_table = 'lc_construcciontipo'

class LcDerechotipo(models.Model):
    id_derechotipo = models.IntegerField(primary_key=True)
    des_derechotipo = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'lc_derechotipo'


class LcDestinacioneconomicatipo(models.Model):
    id_destecono = models.CharField(primary_key=True, max_length=30)
    desc_destecno = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lc_destinacioneconomicatipo'


class LcDominioconstrucciontipo(models.Model):
    id_domconstipo = models.CharField(primary_key=True, max_length=30)
    des_domconsttipo = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'lc_dominioconstrucciontipo'

class LcEstadoconservaciontipo(models.Model):
    id_estadoconser = models.IntegerField(primary_key=True)
    des_estadoconser = models.CharField(max_length=30)
    valor = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lc_estadoconservaciontipo'

class LcFuenteadministrativatipo(models.Model):
    id_fuente = models.IntegerField(primary_key=True)
    des_fuente = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'lc_fuenteadministrativatipo'


class LcGrupoetnicotipo(models.Model):
    id_etnia = models.IntegerField(primary_key=True)
    des_etnia = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lc_grupoetnicotipo'


class LcInteresadodocumentotipo(models.Model):
    id_tipodoc = models.CharField(primary_key=True, max_length=30)
    des_tipodoc = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'lc_interesadodocumentotipo'

class LcInteresadotipo(models.Model):
    id_interesadotipo = models.IntegerField(primary_key=True)
    des_interesadotipo = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'lc_interesadotipo'

class CategoriaObjeto(models.Model):
    id_categobject = models.IntegerField(unique=True)
    id_clacaltipo = models.ForeignKey('LcClasecalificaciontipo', models.DO_NOTHING, db_column='id_clacaltipo')
    des_categobject = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'categoria_objeto'

class LcObjetoconstrucciontipo(models.Model):
    id_objeto = models.IntegerField(primary_key=True)
    id_categobject = models.ForeignKey(CategoriaObjeto, models.DO_NOTHING, db_column='id_categobject')
    id_objetocons = models.IntegerField()
    des_objetocons = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'lc_objetoconstrucciontipo'

class LcPrediotipo(models.Model):
    id_prediotipo = models.CharField(primary_key=True, max_length=30)
    desc_prediotipo = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'lc_prediotipo'


class LcRestricciontipo(models.Model):
    id_restricciontipo = models.IntegerField(primary_key=True)
    descr_restricciontipo = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'lc_restricciontipo'


class LcResultadovisitatipo(models.Model):
    id_resultado = models.CharField(primary_key=True, max_length=30)
    descri_resultado = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'lc_resultadovisitatipo'

class LcSexotipo(models.Model):
    id_genero = models.IntegerField(primary_key=True)
    des_genero = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'lc_sexotipo'

class LcTipologiatipo(models.Model):
    id_tipologia = models.IntegerField(primary_key=True)
    des_tipologia = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lc_tipologiatipo'


class LcUnidadconstrucciontipo(models.Model):
    id_undconstipo = models.IntegerField(primary_key=True)
    des_undconsttipo = models.CharField(max_length=30)
    tipo_cons = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'lc_unidadconstrucciontipo'


class LcUsoconstipo(models.Model):
    id_usocons = models.IntegerField(primary_key=True)
    des_usocons = models.CharField(max_length=30)
    codigo = models.CharField(max_length=3)
    tipo_unidad = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'lc_usoconstipo'