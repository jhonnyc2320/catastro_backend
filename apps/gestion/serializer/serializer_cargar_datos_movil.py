from rest_framework import serializers

from apps.users.models import User

from apps.catastro.models import (
        LcDcPredio as Predio, EstadoPredio, SdeTipoPredio, SdeEstado, 
        LcTerreno, LcUnidadConstruccion, LcDatosadicionaleslevcat, FuenteAdmon, Municipio, Derecho_predio, Interesado,
        FuentePredio, ContactoVisita, Asignacion, Npn, Unidad_puntaje, Lc_puntaje, Cat_calificacion, Cat_estructura, Cat_clase, Cat_clase_clase
    )
from apps.dominios.models import (
        LcPrediotipo, LcCondicionprediotipo, LcClasesuelotipo, 
        LcDestinacioneconomicatipo, LcRestricciontipo,
        LcConstruccionplantatipo, LcConstrucciontipo, LcDominioconstrucciontipo,LcUsoconstipo, LcUnidadconstrucciontipo,
        LcResultadovisitatipo, LcFuenteadministrativatipo, Adquisicion, EnteEmisor, ColEstadodisponibilidadtipo, LcDerechotipo,
        LcInteresadotipo, LcInteresadodocumentotipo, LcSexotipo, LcGrupoetnicotipo
    )

from django.db import transaction

from django.db.models import Max
from django.utils import timezone

class CargarDatosMovilSerializer(serializers.Serializer):
    data = serializers.ListField()

    def validate(self, value):
        return value

    def get_max_id(self, model, field):
        last_id = model.objects.aggregate(Max(field))[f'{field}__max']
        next_id = (last_id or 0) + 1
        return next_id

    def create_predio(self, data):
        # Obtener el último id_terreno y calcular el próximo id
        return Predio.objects.create(**data)
    
    def get_instance(self, Model, field_name, value):
        # Obtener la instancia del modelo utilizando el campo y el valor proporcionados
        try:
            instance = Model.objects.get(**{field_name: value})
        except Exception as e:
            print(str(e))
            instance = None
        return instance
    
    def verificar_propietario(self, interesado):

        # Asume que 'interesado' es tu diccionario de entrada
        campos_interesado = ['primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'razon_social']
        # Transforma los campos vacíos en None
        interesado_procesado = {k: (v if v else None) for k, v in interesado.items() if k in campos_interesado}
        
        instance_interesado = Interesado.objects.filter(
            primer_nombre = interesado_procesado.get('primer_nombre'),
            segundo_nombre= interesado_procesado.get('segundo_nombre'),
            primer_apellido = interesado_procesado.get('primer_apellido'),
            segundo_apellido= interesado_procesado.get('segundo_apellido'),
            razon_social = interesado_procesado.get('razon_social'),
            documento_identidad = interesado.get('documento_identidad'),
            id_tipodoc__id_tipodoc = interesado.get('id_tipodoc'),
            id_interesadotipo__id_interesadotipo = interesado.get('id_interesadotipo')
        )
        
        if not instance_interesado.exists():
            return None, False
        
        return instance_interesado.first(), True

    def create(self, valid_data):
        
        list_predios = valid_data.get('data')
        
        predios_no_cargados_list = []
        predios_no_cargados = {
            'predios':[],
            'message':'predios no cargados.',
            'motivo':'',
        }
        estado = 0
        with transaction.atomic():
            # try:
                
                for json_predio in list_predios:

                    id_predio = json_predio.get('id_predio')
                    predio = json_predio.get('predio')
                    fecha_ingreso = json_predio.get('fecha_ingreso')
                    nom_usu = json_predio.get('nom_usu').upper()
                    instance_usuario = self.get_instance(User, 'email', nom_usu)
                    new_predio = json_predio.get('new_predio')
                    id_predio_nuevo = self.get_max_id(Predio, 'id_predio')

                    #OBJETOS
                    terreno = json_predio.get('lcTerreno')
                    unidadades = json_predio.get('construcciones')
                    datos_adicionales = json_predio.get('datos_adicionales')
                    contacto_visita = json_predio.get('contactoVisita')
                    fuente_administrativa = json_predio.get('fuente_administrativa')
                    npn = json_predio.get('npn')
                    insteresados_predios = json_predio.get('InteresadosPredios')
                    
                    if not predio:
                        predios_no_cargados.get('predios').append(id_predio)
                        predios_no_cargados['motivo'] = 'No tienen diligenciado la pestaña predio.'
                        predios_no_cargados_list.append(predios_no_cargados)
                        continue
                        #raise serializers.ValidationError(f'El id {id_predio} no tienen diligenciada la informadio de predio')
                    
                    # if Predio.objects.filter(id_predio_maestra = id_predio, estado_predio__in = [2,3,4,5,6,7,8]).exists():
                    #     predios_no_cargados.get('predios').append(id_predio)
                    #     predios_no_cargados['motivo'] = 'Los predios ya estan en el aplicativo'
                    #     predios_no_cargados_list.append(predios_no_cargados)
                    #     continue
                    
                    id_prediotipo = 0 if predio.get('id_predio_tipo', None) == 'Por favor seleccione:' else predio.get('id_predio_tipo', None)
                    id_condprediotipo =  predio.get('id_condprediotipo')
                    id_clasesuelo = predio.get('id_clasesuelo')
                    id_destecono =  28 if predio.get('id_desteecono', None) == 'Por favor seleccione:' else predio.get('id_desteecono', None) 
                    id_tipo_predio =predio.get('id_tipo_predio')
                    direccion_notificacion = predio.get('direccion_notificacion')
                    direccion_predio = predio.get('direccion_predio')
                    numero_predial_nacional = predio.get('numero_predial_nacional')
                    porc_participa = predio.get('porcentaje_participacion')
                    pre_inscrip_catas = predio.get('pre_inscrip_catas')
                    observacion = predio.get('observacion')
                    pre_retirado = predio.get('pre_retirado')
                    estado_predio = 2

                    # OBTENER LAS INSTANCIAS 
                    instance_predio_tipo = LcPrediotipo.objects.get(id_prediotipo = id_prediotipo)
                    instance_condicionpredio = LcCondicionprediotipo.objects.get(id_condprediotipo = id_condprediotipo)
                    instance_clasesuelo = LcClasesuelotipo.objects.get(id_clasesuelo = id_clasesuelo)
                    instance_destecono = LcDestinacioneconomicatipo.objects.get(id_destecono = id_destecono)
                    instance_tipo_predio = SdeTipoPredio.objects.get(id_tipo_predio = id_tipo_predio)
                    instance_estadopredio = EstadoPredio.objects.get(id = estado_predio)
                    instance_preretirado = SdeEstado.objects.get(id_estado = pre_retirado)

                    dict_json_predio = {
                        "id_predio": id_predio_nuevo,
                        "id_predio_maestra": id_predio_nuevo if new_predio else id_predio,
                        "id_prediotipo":instance_predio_tipo,
                        'id_condprediotipo':instance_condicionpredio,
                        "id_clasesuelo": instance_clasesuelo,
                        "id_destecono": instance_destecono,
                        "id_tipo_predio": instance_tipo_predio,
                        "npn":numero_predial_nacional,
                        "estado_predio":instance_estadopredio,
                        "direccion_notificacion":direccion_notificacion,
                        "direccion_predio":direccion_predio,
                        "porc_participa":porc_participa,
                        "pre_inscrip_catas":pre_inscrip_catas,
                        "observacion":observacion,
                        "pre_retirado":instance_preretirado,
                        "created_at":timezone.now(),
                        "updated_at":timezone.now(),
                    }

                    # SE CREA EL PREDIO
                    instance_predio = self.create_predio(dict_json_predio)

                    if instance_usuario:
                        Asignacion.objects.create(analista = instance_usuario, predio = instance_predio)
                    
                    
                    # -------------------  INORPORAR TERRENOS -------------------
                    if terreno:

                        # Obtener el último id_terreno y calcular el próximo id
                        id_terreno = self.get_max_id(LcTerreno, 'id_terreno')
                        area_total = terreno.get('area_total')
                        area_comun = terreno.get('area_comun')
                        restriccion_tipo = terreno.get('id_rest_servi')
                        
                        # Obtener instancias de relaciones foráneas
                        instance_SDEstado = self.get_instance(SdeEstado, 'id_estado', 1)
                        instance_restriccion_tipo = self.get_instance(LcRestricciontipo, 'id_restricciontipo', restriccion_tipo)
                        
                        dict_terreno = {
                            'id_predio': instance_predio,
                            'id_terreno': id_terreno,
                            'id_operacion': 1,
                            'area_total': area_total,
                            'area_comun': area_comun,
                            'pre_retirado': instance_SDEstado,
                            'id_rest_servi': instance_restriccion_tipo
                        }

                        LcTerreno.objects.create(**dict_terreno)
                    
                    # -------------------  INORPORAR CONSTRUCCIONES -------------------
                    if unidadades:
                        for construcciones in unidadades:
                            id_construccion = self.get_max_id(LcUnidadConstruccion, 'id_construccion')
                            altura =construcciones.get('altura', 0.0)
                            ano_constru = construcciones.get('anio_construccion')
                            area_comun = construcciones.get('area_comun')
                            area_construida = construcciones.get('area_construida')
                            area_total = construcciones.get('area_total')
                            banos = construcciones.get('banos')
                            desti_econo = construcciones.get('desti_econo')
                            esta_constru = construcciones.get('esta_constru')
                            estado = construcciones.get('estado')
                            habitaciones = construcciones.get('habitaciones')
                            id_tipologia = construcciones.get('id_tipologia')
                            identificador = construcciones.get('identificador')
                            iid = construcciones.get('iid')
                            locales = construcciones.get('locales')
                            mezanines = construcciones.get('mezanines')
                            observacion = construcciones.get('observacion')
                            pisos = construcciones.get('pisos')
                            planta_ubicacion = construcciones.get('planta_ubica')
                            puntaje = construcciones.get('puntaje')
                            semisotanos = construcciones.get('semisotanos')
                            sotanos = construcciones.get('sotanos')
                            construccion_tipo = construcciones.get('tipconst')
                            construccion_planta_tipo = construcciones.get('tipo_planta')
                            anexo_tipo = construcciones.get('tipoanexo')
                            dominio_tipo = construcciones.get('tipodominio')
                            unidad_construccion_tipo = construcciones.get('tipunconst')
                            unidad = construcciones.get('unidad')
                            puntajes = construcciones.get('puntajes')
                            
                            # Obtener instancias de relaciones foráneas
                            #instance_anexo_tipo = self.get_instance(LcAnexotipo, 'des_anexotipo', anexo_tipo)
                            instance_construccion_planta_tipo = self.get_instance(LcConstruccionplantatipo, 'id_constplantatipo', construccion_planta_tipo)
                            instance_construccion_tipo = self.get_instance(LcConstrucciontipo, 'id_constipo', construccion_tipo)
                            instance_dominio_construccion_tipo = self.get_instance(LcDominioconstrucciontipo, 'id_domconstipo', dominio_tipo)
                            instance_unidad_construccion_tipo = self.get_instance(LcUnidadconstrucciontipo, 'id_undconstipo', unidad_construccion_tipo)
                            instance_uso = self.get_instance(LcUsoconstipo, 'id_usocons', desti_econo)
                            instance_SDEstado = self.get_instance(SdeEstado, 'id_estado', 1)

                            dict_unidad = {
                                'id_construccion': id_construccion,
                                'id_predio': instance_predio,
                                'identificador': id_construccion,
                                'id_constipo': instance_construccion_tipo,
                                'id_undconstipo': instance_unidad_construccion_tipo,
                                'id_domconstipo': instance_dominio_construccion_tipo,
                                'id_unidad': unidad,
                                'id_usocons': instance_uso,
                                'area_construida': area_construida,
                                'area_construida_comun': area_comun,
                                'anio_construccion': ano_constru,
                                'total_locales': locales,
                                'total_banos': banos,
                                'total_pisos': pisos,
                                'total_habitaciones': habitaciones,
                                'id_constplantatipo': instance_construccion_planta_tipo,
                                'numero_sotanos': sotanos,
                                'numero_mezanines': mezanines,
                                'total_puntaje': puntaje,
                                'numero_semisotanos':semisotanos,
                                'planta_ubicacion': planta_ubicacion,
                                'retirado': instance_SDEstado,
                                'altura':altura,
                                'puntaje_anexo':anexo_tipo,
                                'id_construccion_maestra': identificador,
                                #'id_anexotipo': instance_anexo_tipo,
                            }
                            instance_unidad = LcUnidadConstruccion.objects.create(**dict_unidad)
                            if puntajes:
                                for clasificacion in puntajes:
                                   
                                    clasclas = clasificacion.get('clasclas')
                                    codcali = clasificacion.get('codcali')
                                    codestr = clasificacion.get('codestr')
                                    codiclas = clasificacion.get('codiclas')
                                    id_predio = instance_predio
                                    puntaje = clasificacion.get('puntaje')
                                    id_unidad = instance_unidad
                                    identificador_puntaje = clasificacion.get('identificador_puntaje')

                                    # OBTENER INSTANCIAS
                                    # try:
                                    instance_codcali = self.get_instance(Cat_calificacion, 'id', codcali)
                                    codi_estructura = Cat_estructura.objects.get(codiestr=codestr, codcali = instance_codcali)
                                    
                                    instance_clase = Cat_clase.objects.get(
                                        codcali=codcali, codiestr__codiestr=codestr, 
                                        codiclas=codiclas, clase_clase = clasclas
                                    ) 

                                    dic_calificacion = {
                                        "puntaje":puntaje,
                                        "codcali":instance_codcali,
                                        "codiclas":instance_clase,
                                        "codiestru":codi_estructura,
                                        "id_predio":instance_predio,
                                        "id_unidad":id_unidad
                                    }
                                    Lc_puntaje.objects.create(**dic_calificacion)
                                    Unidad_puntaje.objects.create(unidad = instance_unidad, puntaje = clasificacion)
                                    # except Exception as e:
                                    #     print(f"Error: {e}")
                                    #     Unidad_puntaje.objects.create(unidad = instance_unidad, puntaje = clasificacion)

                        
                    if datos_adicionales:
                        id_resulvis = datos_adicionales.get('id_resulvis')
                        otroResul = datos_adicionales.get('otroResul')
                        instance_resultado_visita = self.get_instance(LcResultadovisitatipo, 'id_resultado', id_resulvis)
                        
                        dict_datos_adicionales = {
                            'id':self.get_max_id(LcDatosadicionaleslevcat, 'id'),
                            'id_predio' : instance_predio,
                            'id_resultado': instance_resultado_visita,
                            'observaciones': otroResul,
                        }
                        LcDatosadicionaleslevcat.objects.create(**dict_datos_adicionales)
                    
                    instance_fuente_admon = None
                    if fuente_administrativa:
                        print(fuente_administrativa.get('id_registro'), 'id_registro')
                        area_registral = fuente_administrativa.get('area_registral')
                        ente_emisor_fuente = fuente_administrativa.get('ente_emisor_fuente')
                        estado_disponibilidad =fuente_administrativa.get('estado_disponibilidad')
                        fecha_documento_fuente = fuente_administrativa.get('fecha_documento_fuente')
                        fecha_matricula =fuente_administrativa.get('fecha_matricula')
                        fraccion_derecho = fuente_administrativa.get('fraccion_derecho')
                        fuente_emisor_ciudad =fuente_administrativa.get('fuente_emisor_ciudad')
                        id_adquisicion = fuente_administrativa.get('id_adquisicion') if fuente_administrativa.get('id_adquisicion') else 8
                        id_derecho_tipo = fuente_administrativa.get('id_derecho_tipo')
                        id_ente_emisor = fuente_administrativa.get('id_ente_emisor')
                        id_fuente = fuente_administrativa.get('id_fuente')
                        id_predio = instance_predio
                        numero_fuente = fuente_administrativa.get('numero_fuente')
                        numero_matricula = fuente_administrativa.get('numero_matricula')
                        valor = fuente_administrativa.get('valor')
                        id_registro_fuente = fuente_administrativa.get('id_registro')

                        # Obtener instancias de relaciones foráneas
                        instance_fuente_administrativa_tipo = self.get_instance(LcFuenteadministrativatipo, 'id_fuente', id_fuente)
                        insrtance_adquisicion = self.get_instance(Adquisicion, 'id_adquisicion', id_adquisicion)
                        instance_ente_emisor = self.get_instance(EnteEmisor, 'id_ente_emisor', id_ente_emisor)
                        instance_coldisponibilidad_tipo = self.get_instance(ColEstadodisponibilidadtipo, 'id_estadodispo', estado_disponibilidad)
                        instance_derecho_tipo = self.get_instance(LcDerechotipo, 'id_derechotipo', id_derecho_tipo)
                        instance_municipio = self.get_instance(Municipio, 'id_muni', 76001)

                        dict_fuente = {
                            'id': self.get_max_id(FuenteAdmon, 'id_registro'),
                            'id_registro': self.get_max_id(FuenteAdmon, 'id_registro'),
                            'id_fuente': instance_fuente_administrativa_tipo,
                            'id_ente_emisor': instance_ente_emisor,
                            'ente_emisor_fuente': ente_emisor_fuente,
                            'fuente_emisor_ciudad': instance_municipio,
                            'numero_fuente': numero_fuente,
                            'fecha_documento_fuente': fecha_documento_fuente,
                            'estado_disponibilidad': instance_coldisponibilidad_tipo,
                            'fraccion_derecho': fraccion_derecho,
                            'valor': valor,
                            'id_adquisicion': insrtance_adquisicion,
                            'id_derechotipo': instance_derecho_tipo,
                            'numero_matricula': numero_matricula,
                            'fecha_matricula': fecha_matricula,
                            'area_registral': area_registral,
                        }
                        instance_fuente_admon = FuenteAdmon.objects.create(**dict_fuente)
                        FuentePredio.objects.create(fuente_administrativa = instance_fuente_admon, predio = instance_predio)

                    if insteresados_predios:
                        
                        for insteresado_predio in insteresados_predios:

                            autoriza_notificacion_correo = insteresado_predio.get('autoriza_notificacion_correo')
                            correo_electronico = insteresado_predio.get('correo_electronico')
                            estado = insteresado_predio.get('estado')
                            id_estado =insteresado_predio.get('id_estado')
                            id_interesado = insteresado_predio.get('id_interesado')
                            id_interesados_predio = insteresado_predio.get('id_interesados_predio')
                            id_predio = insteresado_predio.get('id_predio')
                            porcentaje_participacion = insteresado_predio.get('porcentaje_participacion')
                            primer_nombre = insteresado_predio.get('primer_nombre')
                            primer_apellido = insteresado_predio.get('primer_apellido')
                            segundo_nombre = insteresado_predio.get('segundo_nombre')
                            segundo_apellido = insteresado_predio.get('segundo_apellido')
                            razon_social = insteresado_predio.get('razon_social')
                            telefono_dos = insteresado_predio.get('telefono_dos')
                            telefono_uno = insteresado_predio.get('telefono_uno')
                            documento_identidad =insteresado_predio.get('documento_identidad') #
                            id_tipodoc = insteresado_predio.get('id_tipodoc') #
                            id_genero = insteresado_predio.get('id_genero') #
                            id_interesadotipo = insteresado_predio.get('id_interesadotipo') #
                            id_etnia = insteresado_predio.get('id_etnia') #
                            id_registro = insteresado_predio.get('id_registro') #

                            # Obtener instancias de relaciones foráneas
                            instance_tipo_documento = self.get_instance(LcInteresadodocumentotipo, 'id_tipodoc', id_tipodoc)
                            instance_genero = self.get_instance(LcSexotipo, 'id_genero', id_genero)
                            instance_tipo_interesado = self.get_instance(LcInteresadotipo, 'id_interesadotipo', id_interesadotipo)
                            instance_etnia = self.get_instance(LcGrupoetnicotipo, 'id_etnia', id_etnia)

                            instance_interesado, verificado = self.verificar_propietario(insteresado_predio)

                            if not verificado:
                                dict_interesado = {
                                    'id': self.get_max_id(Interesado, 'id'),
                                    'documento_identidad': documento_identidad,
                                    'id_interesadotipo': instance_tipo_interesado,
                                    'id_tipodoc': instance_tipo_documento,
                                    'id_etnia': instance_etnia,
                                    'id_genero': instance_genero,
                                    'primer_nombre': primer_nombre,
                                    'segundo_nombre': segundo_nombre,
                                    'primer_apellido': primer_apellido,
                                    'segundo_apellido': segundo_apellido,
                                    'razon_social': razon_social,
                                    'telefono_uno': telefono_uno,
                                    'telefono_dos': telefono_dos,
                                    'direccion_predio': fecha_matricula,
                                    'direccion_notificacion': area_registral,
                                    'correo_electronico': correo_electronico,
                                    'autoriza_notificacion_correo': autoriza_notificacion_correo,
                                }
                                instance_interesado = Interesado.objects.create(**dict_interesado)
                            
                            dict_interesado_predio = {
                                'id': self.get_max_id(Derecho_predio, 'id'),
                                'fraccion_derecho': porcentaje_participacion,
                                'interesado': instance_interesado, 
                                'predio': instance_predio,
                                'fuente_administrativa': instance_fuente_admon if id_registro_fuente == id_registro else None
                            }

                            Derecho_predio.objects.create(**dict_interesado_predio)
                    
                    if contacto_visita:
                        autoriza_notificaciones = contacto_visita.get('autoriza_notificaciones')
                        celular = contacto_visita.get('celular')
                        correo_electronico = contacto_visita.get('correo_electronico')
                        domi_notificacion = contacto_visita.get('domi_notificacion')
                        estado = contacto_visita.get('estado')
                        id_predio = contacto_visita.get('id_predio')
                        id_tipodoc = contacto_visita.get('id_tipodoc')
                        num_doc_atendio = contacto_visita.get('num_doc_atendio')
                        primer_apellido = contacto_visita.get('primer_apellido')
                        primer_nombre = contacto_visita.get('primer_nombre')
                        relacion_predio = contacto_visita.get('relacion_predio')
                        segundo_apellido = contacto_visita.get('segundo_apellido')
                        segundo_nombre = contacto_visita.get('segundo_nombre')

                        instance_tipo_documento = self.get_instance(LcInteresadodocumentotipo, 'des_tipodoc', id_tipodoc)

                        dic_contacto = {
                            'autoriza_notificaciones':autoriza_notificaciones,
                            'celular':celular,
                            'domi_notificacion':domi_notificacion,
                            'correo_electronico':correo_electronico,
                            'id_predio':instance_predio,
                            'id_tipodoc':instance_tipo_documento,
                            'num_doc_atendio':num_doc_atendio,
                            'primer_apellido':primer_apellido,
                            'primer_nombre':primer_nombre,
                            'relacion_predio':relacion_predio,
                            'segundo_apellido':segundo_apellido,
                            'segundo_nombre':segundo_nombre,
                        }

                        ContactoVisita.objects.create(**dic_contacto)

                    if npn:
                        depa = npn.get('Depa')
                        muni = npn.get('Muni')
                        barrio = npn.get('barrio')
                        comuna = npn.get('comuna')
                        condi = npn.get('condi')
                        edifio = npn.get('edifio')
                        estado = npn.get('estado')
                        manzana = npn.get('manzana')
                        piso = npn.get('piso')
                        predio = npn.get('predio')
                        terreno = npn.get('terreno')
                        zona = npn.get('zona')

                        dic_npn = {
                            'id_predio':instance_predio,
                            'depapred': depa,
                            'munipred':muni,
                            'tipo_avaluo':zona,
                            'comuna_id':comuna,
                            'barrio_id':barrio,
                            'manzana_id':manzana,
                            'terreno_id':terreno,
                            'condpred':condi,
                            'edifpred':edifio,
                            'pisopred':piso,
                            'predio_id':predio,
                            'estado':estado,
                            'id': self.get_max_id(Interesado, 'id'),
                        }

                        Npn.objects.create(**dic_npn)
                    
                    predios_no_cargados.get('predios').append(id_predio)
                    predios_no_cargados['message'] = 'Predios cargados exitosamente'
                    predios_no_cargados_list.append(predios_no_cargados)

                # SE CREA LA ASIGNACION
                message_final = "La carga se realizo con novedades" if predios_no_cargados else 'Carga exitosa de todos los predios'
                return {"message": message_final, 'otros':predios_no_cargados}