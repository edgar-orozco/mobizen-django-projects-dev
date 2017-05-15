# -*- coding: utf-8 -*- 
import requests
import base64
import math
from verifica import slackbot
from verifica import models


def request_cotizacion(idAuto, cp, paquete, plazo, inicioVigencia, codColonia, idCliente='557', valorFactura='',
                       placa=None, serie=None, deviceToken=None, telefono=None, nombre=None, email=None,
                       descripcion=None):
    if not telefono:
        telefono = '55555555'
    if not email:
        email = 'noreply@mobizen.com.mx'
    if not nombre:
        nombre = 'ND'

    ## API Key Dev
    # apikey = 'af508bca-6438-5acc-b358-e9f9f903c861'
    # url = 'http://api.interesse.com.mx/api/autos/cotizaciones'
    ## API Key Prod
    apikey = '41b317e3-741b-5bae-97b2-5b19a9e8e26d '
    url = 'http://api.interesse.com.mx/api/autos/cotizaciones'

    ### Parametros obligatorios
    ###
    id_auto = idAuto
    ### Plazo viene como Mensual, Trimestral, Semestral o Anual
    ### Sin embargo, este dato se ha omitido en todas las cotizaciones ya que solo se autorizo pago anual
    id_forma_pago = plazo
    codigo_postal = cp
    udi = None
    email_usuario = email
    numero_telefono = telefono
    nombre_usuario = nombre
    #     apellido_paterno_usuario = paterno
    #     apellido_materno_usuario = materno

    fecha_inicio_vigencia = inicioVigencia
    id_paquete = paquete
    ### Parametros opcionales
    ###
    id_subgrupo = None
    id_aseguradora = None
    valor_factura = None
    id_uso = None
    id_tipo = None
    edad_conductor = None
    id_moneda = None
    coberturas = None
    adaptaciones_especiales = None
    equipo_especial = None
    ### Plazo viene como Mensual, Trimestral, Semestral o Anual
    ### El ws de Interesse pide numero de meses >= 12, por lo que por ahora sera omitido
    plazo_multianual = 12
    headers = {'content-type': 'application/json', 'apikey': apikey}
    payload = {
        'id_auto': id_auto,
        'id_forma_pago': id_forma_pago,
        'codigo_postal': codigo_postal,
        'udi': udi,
        'email_usuario': email_usuario,
        'numero_telefono': numero_telefono,
        'nombre_usuario': nombre_usuario,
        'apellido_paterno_usuario': 'ND',
        'apellido_materno_usuario': 'ND',
        'fecha_inicio_vigencia': fecha_inicio_vigencia,
        'id_paquete': id_paquete,
        'id_subgrupo': id_subgrupo,
        'id_aseguradora': id_aseguradora,
        'valor_factura': valor_factura,
        'id_uso': id_uso,
        'id_tipo': id_tipo,
        'edad_conductor': edad_conductor,
        'id_moneda': id_moneda,
        'coberturas': coberturas,
        'adaptaciones_especiales': adaptaciones_especiales,
        'equipo_especial': equipo_especial,
        'plazo_multianual': plazo_multianual,
    }
    comparacion = models.Comparacion()
    if deviceToken:
        comparacion.client = models.Client.objects.get(deviceToken=deviceToken)
    comparacion.paquete = models.Paquete.objects.get(valor_interesse=paquete)
    comparacion.plazo = models.Plazo.objects.get(valor_interesse=plazo)
    comparacion.fecha = inicioVigencia
    if not placa:
        comparacion.coche_registrado = False
    comparacion.id_auto = idAuto
    comparacion.codigo_colonia = codColonia
    comparacion.codigo_postal = cp
    if telefono:
        comparacion.telefono = telefono
    if nombre:
        comparacion.nombre = nombre
    if email:
        comparacion.email = email
    if descripcion:
        comparacion.descripcion = descripcion
    try:
        r = requests.post(url, data=payload, headers=headers, timeout=29.00)
    except requests.exceptions.Timeout:
        slackbot.send_message(message='Cotizacion: Timeout, idAuto: ' + idAuto, channel='#cotizaciones')
        comparacion.timeout = True
        comparacion.elapsed = r.elapsed.total_seconds()
        comparacion.save()
    comparacion.elapsed = r.elapsed.total_seconds()
    if r.status_code == 200:
        slackbot.send_message(message='Nueva Cotizacion, idAuto: ' + idAuto, channel='#cotizaciones')
        r.encoding = 'utf-8'
        content = r.json()
        try:
            content = r.json()
        except:
            content = None
            comparacion.error_message = 'JSON inválido'
            comparacion.save()
            slackbot.send_message(message='Fallo cotizacion: Error JSON, idAuto: ' + idAuto, channel='#cotizaciones')
            return [{'status': 'No JSON object could be decoded'}]
        if content:
            cotizaciones = []
            emision_url = 'https://autos.interesse.com.mx/autos/app/cliente/mobizen/data/'
            data = content.get('data')
            json_cotizaciones = data.get('cotizaciones')
            for key, json_aseguradora in json_cotizaciones.iteritems():
                if 'aseguradora' in json_aseguradora:
                    id_aseguradora = int(key)
                    parseado = parse_cotizacion(json_aseguradora, id_aseguradora)
                    if parseado:
                        ## Agregamos este valor aqui para no pasar los parametros al parser
                        encode_string = 'ida=' + idAuto + '&cp=' + cp + '&idp=' + paquete + '&idf=' + plazo + '&fiv=' + inicioVigencia + '&idas=' + id_aseguradora
                        if placa is not None:
                            encode_string += '&plc=' + placa
                        if serie is not None:
                            encode_string += '&ser=' + serie
                        encoded_emision_string = base64.b64encode(encode_string)
                        parseado['emision'] = [{'url': emision_url + encoded_emision_string}]
                        cotizaciones.append(parseado)
            costos = []
            comparacion.save()
            for cot in cotizaciones:
                costo = models.Costo()
                if 'costoTotal' in cot:
                    costo.costo = cot['costoTotal']
                aseguradora, created = models.Aseguradora.objects.get_or_create(name__icontains=cot['aseguradora'])
                costo.aseguradora = aseguradora
                costo.save()
                costos.append(costo)
            comparacion.costos = costos
            comparacion.save()
            return {'seguros': cotizaciones}
        else:
            comparacion.error_message = 'Error desconocido'
            comparacion.save()
            slackbot.send_message(message='Fallo cotizacion: Error Server, idAuto: ' + idAuto, channel='#cotizaciones')
            return [{'status': 'Error desconocido'}]
    else:
        comparacion.error_message = 'Error en Servidor'
        comparacion.save()
        slackbot.send_message(message='Fallo cotizacion: Error Server, idAuto: ' + idAuto, channel='#cotizaciones')
        return [{'status': r.status_code}]


def parse_cotizacion(aseguradora, id_aseguradora):
    try:
        compania = aseguradora.get('aseguradora')
        depositoBancario = False
        if id_aseguradora == 22:
            depositoBancario = True
        seguro = {'aseguradora': compania, 'hasMeses': False, 'depositoBancario': depositoBancario}

        resumen = aseguradora.get('resumen_coberturas_asegurado')

        # coberturas
        coberturas = aseguradora.get('coberturas')
        seguro_coberturas = {}

        # inicializa valores
        danosMateriales = False
        sumaDanosMateriales = 0
        deducibleDanosMateriales = 0
        roboTotal = False
        sumaRoboTotal = 0
        deducibleRoboTotal = 0
        danosTerceros = False
        sumaDanosTerceros = 0
        deducibleDanos = 0
        gastosMedicos = False
        sumaGastosMedicos = 0
        deducibleGastosMedicos = 0

        asistenciaVial = resumen.get('asistencia_vial')
        asistenciaLegal = resumen.get('asistencia_legal')

        if 'danos_materiales' in resumen:
            sumaDanosMateriales = resumen.get('danos_materiales')
            deducibleDanosMateriales = resumen.get('deducible_danos_materiales')
            danosMateriales = sumaDanosMateriales != 0
        if 'robo_total' in resumen:
            sumaRoboTotal = resumen.get('robo_total')
            deducibleRoboTotal = resumen.get('deducible_robo_total')
            roboTotal = sumaRoboTotal != 0
        if 'danos_terceros' in resumen:
            sumaDanosTerceros = resumen.get('danos_terceros')
            deducibleDanos = resumen.get('deducible_danos_terceros')
            danosTerceros = sumaDanosMateriales != 0
        if 'gastos_medicos' in resumen:
            sumaGastosMedicos = resumen.get('gastos_medicos')
            deducibleGastosMedicos = resumen.get('deducible_gastos_medicos')
            gastosMedicos = sumaGastosMedicos != 0
        # Esto era en caso de que fuera necesario obtener cada cobertura de manera individual
        #
        #     for key, cob in coberturas.iteritems():
        #         cobertura = cob.get('id_cobertura')
        #         if cobertura == 1:
        #             # Daños Mat
        #             danosMateriales = True
        #             sumaDanosMateriales = cob.get('suma_asegurada')
        #             # viene como 0.05 o 0.1 etc
        #             deducibleDanosMateriales = cob.get('deducible')
        #         if cobertura == 2:
        #             # Robo Total
        #             roboTotal = True
        #             sumaRoboTotal = cob.get('suma_asegurada')
        #             deducibleRoboTotal = cob.get('deducible')
        #         if cobertura == 3 or cobertura == 473:
        #             # Danos Terceros
        #             danosTerceros = True
        #             sumaDanosTerceros += cob.get('suma_asegurada')
        #             deducibleDanos = cob.get('deducible')
        #         if cobertura == 4:
        #             # Gastos Medicos
        #             gastosMedicos = True
        #             sumaGastosMedicos = cob.get('suma_asegurada')
        #             deducibleGastosMedicos = cob.get('deducible')
        #         if cobertura == 116:
        #             # Asistencia Vial
        #             asistenciaVial = True
        #         if cobertura == 78:
        #             # Asistcia Legal
        #             asistenciaLegal = True
        #     # Guarda todos los valores en el diccionario
        seguro_coberturas['danosMateriales'] = danosMateriales
        seguro_coberturas['danosMatDesc'] = {'sumaAsegurada': 'VALOR COMERCIAL',
                                             'deducible': str(deducibleDanosMateriales)}
        seguro_coberturas['roboTotal'] = roboTotal
        seguro_coberturas['roboTotalDesc'] = {'sumaAsegurada': 'VALOR COMERCIAL', 'deducible': str(deducibleRoboTotal)}
        seguro_coberturas['danosTerceros'] = danosTerceros
        seguro_coberturas['danosTercerosDesc'] = {'sumaAsegurada': str(sumaDanosTerceros),
                                                  'deducible': str(deducibleDanos)}
        seguro_coberturas['gastosMedicos'] = gastosMedicos
        seguro_coberturas['gastosMedicosDesc'] = {'sumaAsegurada': str(sumaGastosMedicos),
                                                  'deducible': str(deducibleGastosMedicos)}
        seguro_coberturas['asistenciaVial'] = asistenciaVial
        seguro_coberturas['asistenciaLegal'] = asistenciaLegal
        seguro['cobertura'] = seguro_coberturas

        # costos
        costos = aseguradora.get('costos')
        ptotal = costos.get('prima_total')
        seguro['costoTotal'] = int(math.ceil(float(ptotal)))

        #     recibos = aba_root.find('INCISOS//RECIBOS').getchildren()
        pagos = []
        #     for recibo in recibos:
        #         num = recibo.find('NUM').text
        #         total = int(math.ceil(float(recibo.find('PTOTAL').text)))
        #         pagos += [{'num' : num, 'total' : total}]
        pagos += [{'num': 1, 'total': ptotal}]
        seguro['pagos'] = pagos
        print seguro
        return seguro
    except:
        return None


def test_cotizacion(inicioVigencia, idAuto='1', cp='06700', paquete='1', plazo='1'):
    ## API Key Dev
    apikey = '41b317e3-741b-5bae-97b2-5b19a9e8e26d'
    url = 'http://api.interesse.com.mx/api/autos/cotizaciones'

    idCliente = '557'
    ### Parametros obligatorios
    ###http://api.interesse.com.mx/api/autos/cotizaciones?
    # id_auto=14623
    # id_subgrupo=557
    # id_paquete=1
    # id_forma_pago=1
    # codigo_postal=03300
    # udi
    # email_usuario=jhuerta88@gmail.com
    # nombre_usuario=jorge
    # apellido_paterno_usuario=huerta
    # apellido_materno_usuario=l
    id_subgrupo = idCliente
    id_auto = idAuto
    ### Plazo viene como Mensual, Trimestral, Semestral o Anual
    ### Sin embargo, este dato se ha omitido en todas las cotizaciones ya que solo se autorizo pago anual
    id_forma_pago = plazo
    codigo_postal = cp
    udi = None
    email_usuario = 'carlos.chacon@gmail.com'
    numero_telefono = '5512345678'
    nombre_usuario = 'Carlos'
    apellido_paterno_usuario = 'TEST'
    apellido_materno_usuario = 'TEST'

    fecha_inicio_vigencia = inicioVigencia
    id_paquete = paquete
    ### Parametros opcionales
    ###
    id_aseguradora = None
    valor_factura = None
    id_uso = None
    id_tipo = None
    edad_conductor = None
    id_moneda = None
    coberturas = None
    adaptaciones_especiales = None
    equipo_especial = None
    ### Plazo viene como Mensual, Trimestral, Semestral o Anual
    ### El ws de Interesse pide numero de meses >= 12, por lo que por ahora sera omitido
    plazo_multianual = 12
    headers = {'content-type': 'application/json', 'apikey': apikey}
    payload = {
        'id_auto': id_auto,
        'id_forma_pago': id_forma_pago,
        'codigo_postal': codigo_postal,
        'udi': udi,
        'email_usuario': email_usuario,
        'numero_telefono': numero_telefono,
        'nombre_usuario': nombre_usuario,
        'apellido_paterno_usuario': 'ND',
        'apellido_materno_usuario': 'ND',
        'fecha_inicio_vigencia': fecha_inicio_vigencia,
        'id_paquete': id_paquete,
        'id_subgrupo': id_subgrupo,
        'id_aseguradora': id_aseguradora,
        'valor_factura': valor_factura,
        'id_uso': id_uso,
        'id_tipo': id_tipo,
        'edad_conductor': edad_conductor,
        'id_moneda': id_moneda,
        'coberturas': coberturas,
        'adaptaciones_especiales': adaptaciones_especiales,
        'equipo_especial': equipo_especial,
        'plazo_multianual': plazo_multianual,
    }
    try:
        r = requests.get(url, params=payload, headers=headers, timeout=59.00)
    except requests.exceptions.Timeout:
        print 'error'
        return r
    if r.status_code == 200:
        r.encoding = 'utf-8'
        content = r.json()
        try:
            content = r.json()
        except:
            content = None
            return [{'status': 'No JSON object could be decoded'}]
        if content:
            cotizaciones = []
            emision_url = 'https://autos.interesse.com.mx/autos/app/cliente/mobizen/data/'
            data = content.get('data')
            json_cotizaciones = data.get('cotizaciones')
            for key, json_aseguradora in json_cotizaciones["1"].iteritems():
                if 'aseguradora' in json_aseguradora:
                    id_aseguradora = int(key)
                    parseado = parse_cotizacion(json_aseguradora, id_aseguradora)
                    if parseado:
                        ## Agregamos este valor aqui para no pasar los parametros al parser
                        encode_string = 'ida=' + str(idAuto) + '&cp=' + cp + '&idp=' + str(paquete) + '&idf=' + str(
                            plazo) + '&fiv=' + inicioVigencia + '&idas=' + str(id_aseguradora)
                        encoded_emision_string = base64.b64encode(encode_string)
                        parseado['emision'] = [{'url': emision_url + encoded_emision_string}]
                        cotizaciones.append(parseado)
            return {'seguros': cotizaciones}
        else:
            return [{'status': 'Error desconocido'}]
    else:
        return [{'status': r.status_code}]
























