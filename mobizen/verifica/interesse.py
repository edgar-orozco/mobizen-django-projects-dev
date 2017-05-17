# -*- coding: utf-8 -*- 
import requests
import base64
import math

def parse_cotizacion(aseguradora, id_aseguradora):
    try:
        compania = aseguradora.get('aseguradora')
        deposito_bancario = False
        if id_aseguradora == 22:
            deposito_bancario = True
        seguro = {'aseguradora': compania, 'hasMeses': False, 'deposito_bancario': deposito_bancario}

        resumen = aseguradora.get('resumen_coberturas_asegurado')

        # coberturas
        coberturas = aseguradora.get('coberturas')
        seguro_coberturas = {}

        # inicializa valores
        danos_materiales = False
        suma_danos_materiales = 0
        deducible_danos_materiales = 0
        robo_total = False
        suma_robo_total = 0
        deducible_robo_total = 0
        danos_terceros = False
        suma_danos_terceros = 0
        deducible_danos = 0
        gastos_medicos = False
        suma_gastos_medicos = 0
        deducible_gastos_medicos = 0

        asistencia_vial = resumen.get('asistencia_vial')
        asistencia_legal = resumen.get('asistencia_legal')

        if 'danos_materiales' in resumen:
            suma_danos_materiales = resumen.get('danos_materiales')
            deducible_danos_materiales = resumen.get('deducible_danos_materiales')
            danos_materiales = suma_danos_materiales != 0
        if 'robo_total' in resumen:
            suma_robo_total = resumen.get('robo_total')
            deducible_robo_total = resumen.get('deducible_robo_total')
            robo_total = suma_robo_total != 0
        if 'danos_terceros' in resumen:
            suma_danos_terceros = resumen.get('danos_terceros')
            deducible_danos = resumen.get('deducible_danos_terceros')
            danos_terceros = suma_danos_materiales != 0
        if 'gastos_medicos' in resumen:
            suma_gastos_medicos = resumen.get('gastos_medicos')
            deducible_gastos_medicos = resumen.get('deducible_gastos_medicos')
            gastos_medicos = suma_gastos_medicos != 0
        #    Esto era en caso de que fuera necesario obtener cada cobertura de manera individual
        #
        #     for key, cob in coberturas.iteritems():
        #         cobertura = cob.get('id_cobertura')
        #         if cobertura == 1:
        #             # Daños Mat
        #             danos_materiales = True
        #             suma_danos_materiales = cob.get('suma_asegurada')
        #             # viene como 0.05 o 0.1 etc
        #             deducible_danos_materiales = cob.get('deducible')
        #         if cobertura == 2:
        #             # Robo Total
        #             robo_total = True
        #             suma_robo_total = cob.get('suma_asegurada')
        #             deducible_robo_total = cob.get('deducible')
        #         if cobertura == 3 or cobertura == 473:
        #             # Danos Terceros
        #             danos_terceros = True
        #             suma_danos_terceros += cob.get('suma_asegurada')
        #             deducible_danos = cob.get('deducible')
        #         if cobertura == 4:
        #             # Gastos Medicos
        #             gastos_medicos = True
        #             suma_gastos_medicos = cob.get('suma_asegurada')
        #             deducible_gastos_medicos = cob.get('deducible')
        #         if cobertura == 116:
        #             # Asistencia Vial
        #             asistencia_vial = True
        #         if cobertura == 78:
        #             # Asistcia Legal
        #             asistencia_legal = True
        #     # Guarda todos los valores en el diccionario
        seguro_coberturas['danos_materiales'] = danos_materiales
        seguro_coberturas['danosMatDesc'] = {'sumaAsegurada': 'VALOR COMERCIAL',
                                             'deducible': str(deducible_danos_materiales)}
        seguro_coberturas['robo_total'] = robo_total
        seguro_coberturas['roboTotalDesc'] = {'sumaAsegurada': 'VALOR COMERCIAL', 'deducible': str(deducible_robo_total)}
        seguro_coberturas['danos_terceros'] = danos_terceros
        seguro_coberturas['danosTercerosDesc'] = {'sumaAsegurada': str(suma_danos_terceros),
                                                  'deducible': str(deducible_danos)}
        seguro_coberturas['gastos_medicos'] = gastos_medicos
        seguro_coberturas['gastosMedicosDesc'] = {'sumaAsegurada': str(suma_gastos_medicos),
                                                  'deducible': str(deducible_gastos_medicos)}
        seguro_coberturas['asistencia_vial'] = asistencia_vial
        seguro_coberturas['asistencia_legal'] = asistencia_legal
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

def request_cotizacion(id_auto, cp, paquete, plazo, inicio_vigencia, cod_colonia, id_cliente='557', valor_factura='', placa=None, serie=None,
       device_token=None, telefono="55245044", nombre="ND", email="noreply@mobizen.com.mx", descripcion=None):
    ## API Key Prod
    apikey = '41b317e3-741b-5bae-97b2-5b19a9e8e26d'
    url = 'http://api.interesse.com.mx/api/autos/cotizaciones'

    plazo_multianual = 12
    id_subgrupo = id_cliente

    headers = {'content-type': 'application/json', 'apikey': apikey}
    payload = {
        'id_auto': id_auto,
        'id_forma_pago': plazo,
        'codigo_postal': cp,
        'udi': None,
        'email_usuario': email,
        'numero_telefono': telefono,
        'nombre_usuario': nombre,
        'apellido_paterno_usuario': 'ND',
        'apellido_materno_usuario': 'ND',
        'fecha_inicio_vigencia': inicio_vigencia,
        'id_paquete': paquete,
        'id_subgrupo': id_subgrupo,
        'id_aseguradora': None,
        'valor_factura': valor_factura,
        'id_uso': None,
        'id_tipo': None,
        'edad_conductor': None,
        'id_moneda': None,
        'coberturas': None,
        'adaptaciones_especiales': None,
        'equipo_especial': None,
        'plazo_multianual': plazo_multianual,
    }
    try:
        r = requests.get(url, params=payload, headers=headers, timeout=59.00)
    except requests.exceptions.Timeout:
        print 'error'
        return r
    if r.status_code == 200:
        r.encoding = 'utf-8'
        try:
            content = r.json()
        except:
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
                        encode_string = 'ida=' + str(id_auto) + '&cp=' + cp + '&idp=' + str(paquete) + '&idf=' + str(
                            plazo) + '&fiv=' + inicio_vigencia + '&idas=' + str(id_aseguradora)
                        encoded_emision_string = base64.b64encode(encode_string)
                        parseado['emision'] = [{'url': emision_url + encoded_emision_string}]
                        cotizaciones.append(parseado)
            return {'seguros': cotizaciones}
        else:
            return [{'status': 'Error desconocido'}]
    else:
        return [{'status': r.status_code}]
