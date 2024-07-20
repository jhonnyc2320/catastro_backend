from django.contrib.gis.db import models

# utilities
from apps.utils.models import BaseModel

# dominios
from apps.dominios import models as models_dominios

# USER
from apps.users.models import User
from django.utils import timezone


class Municipio(models.Model):
    id_muni = models.CharField(primary_key=True, max_length=50)
    nom_muni = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'municipio'


class AlfaConexion(models.Model):
    id_predio = models.OneToOneField('LcDcPredio', models.DO_NOTHING, db_column='id_predio')
    npn = models.CharField(max_length=30)
    conexion = models.CharField(max_length=30)
    
    class Meta:
        managed = False
        db_table = 'alfa_conexion'



class FuenteAdmon(models.Model):
    id = models.BigIntegerField(unique=True, primary_key=True)
    id_registro = models.BigIntegerField(unique=True)
    id_fuente = models.ForeignKey(models_dominios.LcFuenteadministrativatipo, models.DO_NOTHING, db_column='id_fuente')
    id_ente_emisor = models.ForeignKey(models_dominios.EnteEmisor, models.DO_NOTHING, db_column='id_ente_emisor')
    ente_emisor_fuente = models.CharField(max_length=30, blank=True, null=True)
    fuente_emisor_ciudad = models.ForeignKey('Municipio', models.DO_NOTHING, db_column='fuente_emisor_ciudad')
    numero_fuente = models.BigIntegerField(blank=True, null=True)
    fecha_documento_fuente = models.CharField(max_length=30, blank=True, null=True)
    estado_disponibilidad = models.ForeignKey(models_dominios.ColEstadodisponibilidadtipo, models.DO_NOTHING, db_column='estado_disponibilidad')
    fraccion_derecho = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valor = models.BigIntegerField(blank=True, null=True)
    id_adquisicion = models.ForeignKey(models_dominios.Adquisicion, models.DO_NOTHING, db_column='id_adquisicion')
    id_derechotipo = models.ForeignKey(models_dominios.LcDerechotipo, models.DO_NOTHING, db_column='id_derechotipo')
    numero_matricula = models.BigIntegerField(blank=True, null=True)
    fecha_matricula = models.CharField(max_length=30, blank=True, null=True)
    area_registral = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fuente_admon'

class Interesado(models.Model):
    documento_identidad = models.CharField(max_length=30)
    secuencial = models.BigIntegerField()
    id_interesadotipo = models.ForeignKey(models_dominios.LcInteresadotipo, models.DO_NOTHING, db_column='id_interesadotipo')
    id_tipodoc = models.ForeignKey(models_dominios.LcInteresadodocumentotipo, models.DO_NOTHING, db_column='id_tipodoc')
    id_etnia = models.ForeignKey(models_dominios.LcGrupoetnicotipo, models.DO_NOTHING, db_column='id_etnia')
    id_genero = models.ForeignKey(models_dominios.LcSexotipo, models.DO_NOTHING, db_column='id_genero')
    primer_nombre = models.CharField(max_length=50)
    segundo_nombre = models.CharField(max_length=50, blank=True, null=True)
    primer_apellido = models.CharField(max_length=50)
    segundo_apellido = models.CharField(max_length=50, blank=True, null=True)
    razon_social = models.CharField(max_length=50, blank=True, null=True)
    telefono_uno = models.BigIntegerField(blank=True, null=True)
    telefono_dos = models.BigIntegerField(blank=True, null=True)
    direccion_predio = models.CharField(max_length=50, blank=True, null=True)
    direccion_notificacion = models.CharField(max_length=50, blank=True, null=True)
    correo_electronico = models.CharField(max_length=50, blank=True, null=True)
    autoriza_notificacion_correo = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'interesado'
        unique_together = (('documento_identidad', 'secuencial'),)

class ContactoVisita(models.Model):
    autoriza_notificaciones = models.CharField(max_length=50, blank=True, null=True)
    celular = models.CharField(max_length=50, blank=True, null=True)
    domi_notificacion = models.CharField(max_length=50, blank=True, null=True)
    id_predio = models.OneToOneField('LcDcPredio', models.DO_NOTHING, db_column='id_predio')
    id_tipodoc = models.ForeignKey(models_dominios.LcInteresadodocumentotipo, models.DO_NOTHING, db_column='id_tipodoc', null=True)
    num_doc_atendio = models.CharField(max_length=30, blank=True, null=True)
    primer_nombre = models.CharField(max_length=50, blank=True, null=True)
    segundo_nombre = models.CharField(max_length=50, blank=True, null=True)
    primer_apellido = models.CharField(max_length=50, blank=True, null=True)
    segundo_apellido = models.CharField(max_length=50, blank=True, null=True)
    relacion_predio = models.CharField(max_length=50, blank=True, null=True)
    correo_electronico = models.CharField(max_length=50, blank=True, null=True)
    

class LcDatosadicionaleslevcat(models.Model):
    id = models.BigIntegerField(primary_key=True)
    id_predio = models.OneToOneField('LcDcPredio', models.DO_NOTHING, db_column='id_predio')
    id_resultado = models.ForeignKey(models_dominios.LcResultadovisitatipo, models.DO_NOTHING, db_column='id_resultado')
    id_novedad_est = models.ForeignKey('LcEstructuranovedadnumeropre', models.DO_NOTHING, db_column='id_novedad_est')
    area_registral_m2 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    observaciones = models.CharField(max_length=150, blank=True, null=True)
    fecha_visita_predial = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lc_datosadicionaleslevcat'


class EstadoPredio(models.Model):
    nombre= models.CharField(max_length=10)
    descripcion = models.CharField(max_length=100)

class LcDcPredio(models.Model):
    id_predio = models.BigIntegerField(unique=True, primary_key=True)
    pre_retirado = models.ForeignKey('SdeEstado', models.DO_NOTHING, db_column='pre_retirado')
    id_prediotipo = models.ForeignKey(models_dominios.LcPrediotipo, models.DO_NOTHING, db_column='id_prediotipo')
    id_condprediotipo = models.ForeignKey(models_dominios.LcCondicionprediotipo, models.DO_NOTHING, db_column='id_condprediotipo')
    id_clasesuelo = models.ForeignKey(models_dominios.LcClasesuelotipo, models.DO_NOTHING, db_column='id_clasesuelo')
    id_destecono = models.ForeignKey(models_dominios.LcDestinacioneconomicatipo, models.DO_NOTHING, db_column='id_destecono')
    id_tipo_predio = models.ForeignKey('SdeTipoPredio', models.DO_NOTHING, db_column='id_tipo_predio')
    id_operacion = models.BigIntegerField()
    npn = models.CharField(max_length=30)
    direccion_predio = models.CharField(max_length=100, blank=True, null=True)
    direccion_notificacion = models.CharField(max_length=100, blank=True, null=True)
    porc_participa = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    pre_inscrip_catas = models.CharField(max_length=30, blank=True, null=True)
    observacion = models.CharField(max_length=150, blank=True, null=True)
    estado_predio = models.ForeignKey(EstadoPredio, models.DO_NOTHING)
    id_predio_maestra = models.BigIntegerField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)  # Nuevo campo de tipo DateTimeField  # Nuevo campo de tipo DateField
    orip = models.IntegerField(blank=True, null=True)
    matricula = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lc_dc_predio'

class Asignacion(BaseModel):
    analista = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asignaciones_como_analista')
    coordinador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asignaciones_como_coordinador', null=True)
    predio = models.ForeignKey(LcDcPredio, on_delete=models.CASCADE, db_column='id_predio')
    semana = models.IntegerField(null=True)


    class Meta:
        managed = True
        db_table = 'asignacion'
    
    def __str__(self):
        return f'Asignación de {self.predio} a {self.analista} (Coordinador: {self.coordinador})'

class Trazabilidad(BaseModel):
    analista = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trazabilidad_analista')
    coordinador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trazabilidad_coordinador')
    predio = models.ForeignKey(LcDcPredio, on_delete=models.CASCADE, db_column='id_predio')
    estado_trazabilidad = models.ForeignKey(EstadoPredio, models.DO_NOTHING)
    observacion = models.TextField(null=True)


class Derecho_predio(BaseModel):
    fraccion_derecho = models.FloatField(null=True)
    interesado = models.ForeignKey(Interesado, on_delete=models.CASCADE)
    predio = models.ForeignKey(LcDcPredio, on_delete=models.CASCADE, db_column='id_predio')
    fuente_administrativa = models.ForeignKey(FuenteAdmon, on_delete=models.CASCADE, null=True, db_column='id_registro')
    comienzo_vida_util = models.DateField(null=True)
    fin_vida_util = models.DateField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'derecho_predio'

class FuentePredio(models.Model):
    predio = models.ForeignKey(LcDcPredio, on_delete=models.CASCADE, db_column='id_predio')
    fuente_administrativa = models.ForeignKey(FuenteAdmon, on_delete=models.CASCADE, null=True, db_column='id_registro')
    
class LcDcTitulo(models.Model):
    id_predio = models.OneToOneField(LcDcPredio, models.DO_NOTHING, db_column='id_predio', primary_key=True)
    id_operacion = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'lc_dc_titulo'
        unique_together = (('id_predio', 'id_operacion'),)


class LcEstructuranovedadnumeropre(models.Model):
    id_novedad_est = models.CharField(primary_key=True, max_length=50)
    descri_novedad_est = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lc_estructuranovedadnumeropre'

class LcTerreno(models.Model):
    id_terreno = models.BigIntegerField(primary_key=True)
    id_operacion = models.BigIntegerField()
    id_predio = models.ForeignKey(LcDcPredio, models.DO_NOTHING, db_column='id_predio')
    area_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    area_comun = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pre_retirado = models.ForeignKey('SdeEstado', models.DO_NOTHING, db_column='pre_retirado')
    id_rest_servi = models.ForeignKey(models_dominios.LcRestricciontipo, models.DO_NOTHING, db_column='id_rest_servi')

    class Meta:
        managed = False
        db_table = 'lc_terreno'
        # unique_together = (('id_terreno', 'id_operacion'), ('id_terreno', 'id_operacion'),)


class LcTipologiatipo(models.Model):
    id_tipologia = models.IntegerField(primary_key=True)
    des_tipologia = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lc_tipologiatipo'


class LcUnidadConstruccion(models.Model):
    id_construccion = models.BigIntegerField(primary_key=True)
    id_calificartipo = models.ForeignKey(models_dominios.LcCalificartipo, models.DO_NOTHING, db_column='id_calificartipo')
    id_predio = models.ForeignKey(LcDcPredio, models.DO_NOTHING, db_column='id_predio')
    identificador = models.BigIntegerField()
    id_constipo = models.ForeignKey(models_dominios.LcConstrucciontipo, models.DO_NOTHING, db_column='id_constipo')
    id_undconstipo = models.ForeignKey(models_dominios.LcUnidadconstrucciontipo, models.DO_NOTHING, db_column='id_undconstipo')
    id_domconstipo = models.ForeignKey(models_dominios.LcDominioconstrucciontipo, models.DO_NOTHING, db_column='id_domconstipo')
    id_unidad = models.CharField(max_length=50)
    id_usocons = models.ForeignKey(models_dominios.LcUsoconstipo, models.DO_NOTHING, db_column='id_usocons')
    area_construida = models.DecimalField(max_digits=10, decimal_places=2)
    area_construida_comun = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    anio_construccion = models.IntegerField(blank=True, null=True)
    total_locales = models.IntegerField(blank=True, null=True)
    total_banos = models.IntegerField()
    total_pisos = models.IntegerField(blank=True, null=True)
    total_habitaciones = models.IntegerField(blank=True, null=True)
    id_constplantatipo = models.ForeignKey(models_dominios.LcConstruccionplantatipo, models.DO_NOTHING, db_column='id_constplantatipo')
    planta_ubicacion = models.IntegerField(blank=True, null=True)
    numero_sotanos = models.IntegerField(blank=True, null=True)
    numero_mezanines = models.IntegerField(blank=True, null=True)
    numero_semisotanos = models.IntegerField(blank=True, null=True)
    altura = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_puntaje = models.IntegerField()
    retirado = models.ForeignKey('SdeEstado', models.DO_NOTHING, db_column='retirado')
    id_anexotipo = models.ForeignKey(models_dominios.LcAnexotipo, models.DO_NOTHING, db_column='id_anexotipo')
    observaciones = models.CharField(max_length=50, blank=True, null=True)
    id_tipologia = models.ForeignKey(LcTipologiatipo, models.DO_NOTHING, db_column='id_tipologia')
    destino_h = models.CharField(max_length=50, blank=True, null=True)
    puntaje_anexo = models.IntegerField(null=True)
    id_construccion_maestra = models.IntegerField(null=True)

    class Meta:
        managed = False
        db_table = 'lc_unidad_construccion'

class Cat_clase_clase(models.Model):
    detalle = models.TextField()

class Cat_calificacion(models.Model):
    detalle = models.TextField()

class Cat_estructura(models.Model):
    codcali = models.ForeignKey(Cat_calificacion, models.DO_NOTHING)
    codiestr = models.IntegerField(default=0)
    detalle = models.TextField()

class Cat_clase(models.Model):
    codcali = models.ForeignKey(Cat_calificacion, models.DO_NOTHING)
    codiestr = models.ForeignKey(Cat_estructura, models.DO_NOTHING)
    codiclas = models.IntegerField(default=0)
    clase_clase = models.ForeignKey(Cat_clase_clase, models.DO_NOTHING, default=1)
    detalle = models.TextField()
    puntaje = models.IntegerField(default=0)

class Lc_puntaje(models.Model):
    id_predio = models.ForeignKey(LcDcPredio, models.DO_NOTHING, db_column='id_predio')
    id_unidad = models.ForeignKey(LcUnidadConstruccion, models.DO_NOTHING, null=True)
    codcali = models.ForeignKey(Cat_calificacion, models.DO_NOTHING)
    codiestru = models.ForeignKey(Cat_estructura, models.DO_NOTHING)
    codiclas = models.ForeignKey(Cat_clase, models.DO_NOTHING)
    puntaje = models.CharField(max_length=4)

class LcNovedadfmi(models.Model):
    id_novedad_fmi = models.CharField(primary_key=True, max_length=50)
    descri_novedad_fmi = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'lc_novedadfmi'

class Unidad_puntaje(models.Model):
    unidad = models.ForeignKey(LcUnidadConstruccion, models.DO_NOTHING, null=True)
    puntaje = models.JSONField()


class Npn(models.Model):
    id_predio = models.ForeignKey(LcDcPredio, models.DO_NOTHING, db_column='id_predio', related_name='npns')
    provipre = models.CharField(max_length=50, blank=True, null=True)
    depapred = models.CharField(max_length=50)
    munipred = models.CharField(max_length=50)
    tipo_avaluo = models.CharField(max_length=50)
    comuna_id = models.CharField(max_length=50)
    barrio_id = models.CharField(max_length=50)
    manzana_id = models.CharField(max_length=50)
    terreno_id = models.CharField(max_length=50)
    condpred = models.CharField(max_length=50)
    edifpred = models.CharField(max_length=50)
    pisopred = models.CharField(max_length=50)
    predio_id = models.CharField(max_length=50)
    lado_manzana = models.CharField(max_length=50)
    estado = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'npn'


class SdeCatGeneral(models.Model):
    id_predio = models.OneToOneField(LcDcPredio, models.DO_NOTHING, db_column='id_predio', primary_key=True)
    id_operacion = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sde_cat_general'


class SdeEstado(models.Model):
    id_estado = models.IntegerField(primary_key=True)
    desc_estado = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'sde_estado'


class SdeTipoPredio(models.Model):
    id_tipo_predio = models.CharField(primary_key=True, max_length=50)
    desc_tipo_predio = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'sde_tipo_predio'


class Zhg(models.Model):
    id_zhg = models.IntegerField(primary_key=True)
    desc_zhg = models.CharField(max_length=50, blank=True, null=True)
    vigencia_zhg = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'zhg'

class Historia(models.Model):
    estado = models.ForeignKey(EstadoPredio, models.DO_NOTHING)
    predio = models.ForeignKey(LcDcPredio, models.DO_NOTHING, db_column='id_predio')
    derecho_predio = models.ForeignKey(Derecho_predio, models.DO_NOTHING)
    terreno = models.ForeignKey(LcTerreno, models.DO_NOTHING, db_column='id_terreno')
    unidad_construccion = models.ForeignKey(LcUnidadConstruccion, models.DO_NOTHING, db_column='id_construccion')
   