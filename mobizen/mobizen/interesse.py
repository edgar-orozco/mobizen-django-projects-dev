# -*- coding: utf-8 -*- 
import requests
from lxml import etree, objectify
from io import StringIO
import base64
import math
from verifica import slackbot
from verifica import models
# import HTMLParser
# html_parser = HTMLParser.HTMLParser()
# unescaped = html_parser.unescape(my_string)

def request_cotizacion(idAuto, cp, paquete, plazo, inicioVigencia, codColonia, idCliente='219', valorFactura='', placa=None, serie=None, deviceToken=None, telefono=None, nombre=None, email=None, descripcion=None):
#     headers = {'content-type': 'text/xml'}
#     url = 'https://esb.interesse.com.mx/services/cotiza_proxy.cotiza_proxyHttpEndpoint/cotiza'
#     url = 'http://apps.ohkasystems.com/wso2/services/cotiza_proxy.cotiza_proxyHttpEndpoint/cotiza'
#     payload = '<?xml version="1.0" encoding="UTF-8"?><cotiza><cp>'+cp+'</cp><idCliente>'+idCliente+'</idCliente><idAuto>'+idAuto+'</idAuto><paquete>'+paquete+'</paquete><plazo>'+plazo+'</plazo><valorFactura>'+valorFactura+'</valorFactura><inicioVigencia>'+inicioVigencia+'</inicioVigencia><codColonia>'+codColonia+'</codColonia></cotiza>'
    headers = {'content-type': 'text/xml;charset=UTF-8', 'SOAPAction': '"urn:cotiza"'}
    url = 'https://esb.interesse.com.mx/services/cotiza_proxy.cotiza_proxyHttpSoap11Endpoint'
#     url = 'http://189.254.19.101:8280/services/cotiza_proxy.cotiza_proxyHttpSoap11Endpoint'
    debug = True
    if not telefono:
        telefono = ' '
    if not email:
        email = ' '
    if not nombre:
        nombre = ' '
    paterno = ' '
    materno = ' '
    if debug:
        url = 'http://189.254.19.101:8280/services/cotiza_proxy.cotiza_proxyHttpSoap11Endpoint'
        payload= '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="http://services.interesse.ohka.com"><soapenv:Header/><soapenv:Body><ser:cotiza><ser:cp>'+cp+'</ser:cp><ser:idCliente>'+idCliente+'</ser:idCliente><ser:idAuto>'+idAuto+'</ser:idAuto><ser:paquete>'+paquete+'</ser:paquete><ser:plazo>'+plazo+'</ser:plazo><ser:valorFactura>'+valorFactura+'</ser:valorFactura><ser:inicioVigencia>'+inicioVigencia+'</ser:inicioVigencia><ser:codColonia>'+codColonia+'</ser:codColonia><ser:paterno>'+paterno+'</ser:paterno><ser:materno>'+materno+'</ser:materno><ser:nombre>'+nombre+'</ser:nombre><ser:email>'+email+'</ser:email><ser:telefono>'+telefono+'</ser:telefono></ser:cotiza></soapenv:Body></soapenv:Envelope>'
    else :    
        url = 'https://esb.interesse.com.mx/services/cotiza_proxy.cotiza_proxyHttpSoap11Endpoint'
        payload= '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="http://services.interesse.ohka.com"><soapenv:Header/><soapenv:Body><ser:cotiza><ser:cp>'+cp+'</ser:cp><ser:idCliente>'+idCliente+'</ser:idCliente><ser:idAuto>'+idAuto+'</ser:idAuto><ser:paquete>'+paquete+'</ser:paquete><ser:plazo>'+plazo+'</ser:plazo><ser:valorFactura>'+valorFactura+'</ser:valorFactura><ser:inicioVigencia>'+inicioVigencia+'</ser:inicioVigencia><ser:codColonia>'+codColonia+'</ser:codColonia></ser:cotiza></soapenv:Body></soapenv:Envelope>'
#     r = requests.post(url, data=payload, headers=headers, verify=False)
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
        slackbot.send_message(message='Cotizacion: Timeout, idAuto: '+idAuto, channel='#cotizaciones')
        comparacion.timeout = True
        comparacion.elapsed = r.elapsed.total_seconds()
        comparacion.save()
    comparacion.elapsed = r.elapsed.total_seconds()
    if r.status_code == 200:
        slackbot.send_message(message='Nueva Cotizacion, idAuto: '+idAuto, channel='#cotizaciones')
        parser = etree.XMLParser(remove_blank_text=True)
        try:
            tree = etree.parse(StringIO(r.content.decode('utf-8')), parser)
            root = tree.getroot()
        except:
            tree  = r.text.encode('utf-8')
            root = etree.fromstring(tree, parser)        
        for elem in root.getiterator():
            if not hasattr(elem.tag, 'find'): continue
            i = elem.tag.find('}')
            if i >= 0:
                elem.tag = elem.tag[i+1:]
        
        objectify.deannotate(root, cleanup_namespaces=True)
        cotizaciones = []
        aba = root.find('.//aba')
#         emision_url = 'https://webapp.interesse.com.mx/autos/app/cliente/mobizen/data/'
        emision_url = 'https://autos.interesse.com.mx/autos/app/cliente/mobizen/data/'
        if aba:
            aba_result = aba_parser(aba, plazo)
            if aba_result:
                encode_string = 'ida='+idAuto+'&cp='+cp+'&idp='+paquete+'&idf='+plazo+'&fiv='+inicioVigencia+'&idas=23'
                if placa is not None:
                    encode_string += '&plc='+placa
                if serie is not None:
                    encode_string += '&ser='+serie
                aba_emision = base64.b64encode(encode_string)
                aba_result['emision'] = [{'url': emision_url+aba_emision}]
                cotizaciones.append(aba_result)
#         atlas = root.find('.//atlas')
#         if atlas:
#             atlas_result = atlas_parser(atlas, paquete)
#             if atlas_result:
#                 encode_string = 'ida='+idAuto+'&cp='+cp+'&idp='+paquete+'&idf='+plazo+'&fiv='+inicioVigencia+'&nombre='+nombre+'&paterno='+paterno+'&materno='+materno+'&telefono='+telefono+'&email='+email+'&idas=1'
#                 if placa is not None:
#                     encode_string += '&plc='+placa
#                 if serie is not None:
#                     encode_string += '&ser='+serie
#                 atlas_emision = base64.b64encode(encode_string)
#                 atlas_result['emision'] = [{'url': emision_url+atlas_emision}]
#                 cotizaciones.append(atlas_result)
        qualitas = root.find('.//qualitas')
        if qualitas:
            qualitas_result = qualitas_parser(qualitas)
            if qualitas_result:
                encode_string = 'ida='+idAuto+'&cp='+cp+'&idp='+paquete+'&idf='+plazo+'&fiv='+inicioVigencia+'&idas=22'
                if placa is not None:
                    encode_string += '&plc='+placa
                if serie is not None:
                    encode_string += '&ser='+serie
                qualitas_emision = base64.b64encode(encode_string)
                qualitas_result['emision'] = [{'url': emision_url+qualitas_emision}]
                cotizaciones.append(qualitas_result)
#         mapfre = root.find('.//mapfre')
#         if mapfre:
#             mapfre_result = mapfre_parser(mapfre)
#             if mapfre_result:
#                 encode_string = 'ida='+idAuto+'&cp='+cp+'&idp='+paquete+'&idf='+plazo+'&fiv='+inicioVigencia+'&idas=29'
#                 if placa is not None:
#                     encode_string += '&plc='+placa
#                 if serie is not None:
#                     encode_string += '&ser='+serie
#                 mapfre_emision = base64.b64encode(encode_string)
#                 mapfre_result['emision'] = [{'url': emision_url+mapfre_emision}]
#                 cotizaciones.append(mapfre_result)        
        if len(cotizaciones) == 0:
            comparacion.error_message = 'No hubo aseguradoras'
            comparacion.save()
            return [{'status':'Cotización no disponible'}]
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
        return {'seguros' : cotizaciones}
    elif r.status_code == 202:
        comparacion.error_message = 'Fallo cotizacion, reintentar'
        comparacion.save()
        slackbot.send_message(message='Fallo cotizacion: Reintenta Más tarde, idAuto: '+idAuto, channel='#cotizaciones')
        return [{'status':'Reintenta más tarde'}]
    else:
        comparacion.error_message = 'Error en Servidor'
        comparacion.save()
        slackbot.send_message(message='Fallo cotizacion: Error Server, idAuto: '+idAuto, channel='#cotizaciones')
        return [{'status':r.status_code}]
        

def aba_parser(xmlroot, plazo):
    if plazo == '1' or plazo == 1:
        return None
    if plazo == '2' or plazo == 2:
        return None
    if plazo == '3' or plazo == 3:
        return None
    failure = xmlroot.find('.//echoStringResponse')
    if failure is not None:
        return None
    hasMeses = False
    if len(xmlroot.xpath('hasMeses')) == 1:
        if xmlroot.find('hasMeses').text == '1':
            hasMeses = True
    seguro = {'aseguradora' : 'aba', 'hasMeses' : hasMeses, 'depositoBancario':True}
    
    tree_root = xmlroot.find('.//strSalida')
    if tree_root == None:
        return None
    aba_root = etree.fromstring(tree_root.text.encode('utf-8'))
    # emision
    cotid = aba_root.find('.//COTID')
    verid = aba_root.find('.//VERID')    
    cotincid = aba_root.find('.//COTINCID')
    verincid = aba_root.find('.//VERINCID')
#     emision = [
#         {'value' : cotid.text, 'key' : 'COTID'},
#         {'value' : verid.text, 'key' : 'VERID'},
#         {'value' : cotincid.text, 'key' : 'COTINCID'},
#         {'value' : verincid.text, 'key' : 'VERINCID'}        
#     ]
#     
#     seguro['emision'] = emision
    
    # coberturas
    coberturas = aba_root.find('INCISOS//COBS')
    seguro_coberturas = {}
    
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
    asistenciaVial = False
    asistenciaLegal = False
    for cob in list(coberturas):
        cobertura = cob.find('COBID').text
        if cobertura == '1':
            # Daños Mat
            if cob.find('SEL').text == '1':
                danosMateriales = True
                try:
                    sumaDanosMateriales = int(cob.find('SADESC').text)
                except ValueError:
                    sumaDanosMateriales = cob.find('SADESC').text
                # viene como 0.05 o 0.1 etc
                deducibleDanosMateriales = int(float(cob.find('DPCT').text) * 100)
        if cobertura == '2':
            # Robo Total
            if cob.find('SEL').text == '1':
                roboTotal = True
                try:
                    sumaRoboTotal = int(cob.find('SADESC').text)
                except ValueError:
                    sumaRoboTotal = cob.find('SADESC').text
                deducibleRoboTotal = int(float(cob.find('DPCT').text) * 100)
        if cobertura == '3' or cobertura == '473':
            # Danos Terceros
            if cob.find('SEL').text == '1':
                danosTerceros = True
                sumaDanosTerceros += int(cob.find('SUMAASEG').text)
                deducibleDanos = int(float(cob.find('DPCT').text) * 100)
        if cobertura == '4':
            # Gastos Medicos
            if cob.find('SEL').text == '1':
                gastosMedicos = True
                try:
                    sumaGastosMedicos = int(float(cob.find('SADESC').text.replace(',','').replace('$','')))
                except ValueError:
                    sumaGastosMedicos = cob.find('SADESC').text
                deducibleGastosMedicos = int(float(cob.find('DPCT').text))
        if cobertura == '116':
            # Asistencia Vial
            if cob.find('SEL').text == '1':
                asistenciaVial = True
        if cobertura == '78':
            # Asistcia Legal
            if cob.find('SEL').text == '1':
                asistenciaLegal = True
    # Guarda todos los valores en el diccionario
    
    seguro_coberturas['danosMateriales'] = danosMateriales
    seguro_coberturas['danosMatDesc'] = {'sumaAsegurada' : 'VALOR COMERCIAL', 'deducible' : str(deducibleDanosMateriales)}
    seguro_coberturas['roboTotal'] = roboTotal
    seguro_coberturas['roboTotalDesc'] = {'sumaAsegurada' : 'VALOR COMERCIAL', 'deducible' : str(deducibleRoboTotal)}
    seguro_coberturas['danosTerceros'] = danosTerceros
    seguro_coberturas['danosTercerosDesc'] = {'sumaAsegurada' : str(sumaDanosTerceros), 'deducible' : str(deducibleDanos)}
    seguro_coberturas['gastosMedicos'] = gastosMedicos
    seguro_coberturas['gastosMedicosDesc'] = {'sumaAsegurada' : str(sumaGastosMedicos), 'deducible' : str(deducibleGastosMedicos)}
    seguro_coberturas['asistenciaVial'] = asistenciaVial
    seguro_coberturas['asistenciaLegal'] = asistenciaLegal
    seguro['cobertura'] = seguro_coberturas
    
    # costos
    ptotal = aba_root.find('PTOTAL')
    seguro['costoTotal'] = int(math.ceil(float(ptotal.text)))
    
    recibos = aba_root.find('INCISOS//RECIBOS').getchildren()
    pagos = []
    for recibo in recibos:
        num = recibo.find('NUM').text
        total = int(math.ceil(float(recibo.find('PTOTAL').text)))
        pagos += [{'num' : num, 'total' : total}]
    seguro['pagos'] = pagos
    return seguro

def atlas_parser(xmlroot, paquete):
    failure = xmlroot.find('.//echoStringResponse')
    if failure is not None:
        return None
    hasMeses = False
    if len(xmlroot.xpath('hasMeses')) == 1:
        if xmlroot.find('hasMeses').text == '1':
            hasMeses = True
    seguro = {'aseguradora' : 'atlas', 'hasMeses' : hasMeses, 'depositoBancario':False}
    
    atlas_root = xmlroot.find('.//response')
    if not atlas_root:
        return None
    errores = atlas_root.find('.//Errores')
    error = errores.find('.//Error')
    if error.text is not '0':
        return None
    # emision
#     num_cotiza = atlas_root.find('.//NumCotiza')
#     id_control = atlas_root.find('.//IdControl')    
#     fecha_cotiza = atlas_root.find('.//FechaCotiza')
#     fecha_inicio = atlas_root.find('.//FechaInicio')
#     fecha_fin = atlas_root.find('.//FechaTermino')
    if paquete == 1 or paquete == '1':
        plan = '2'
    elif paquete == 2 or paquete == '2':
        plan = '10'
    else:
        plan = '4'
#         
#     emision = [
#         {'value' : num_cotiza.text, 'key' : 'NumCotiza'},
#         {'value' : id_control.text, 'key' : 'IdControl'},
#         {'value' : fecha_cotiza.text, 'key' : 'FechaCotiza'},
#         {'value' : fecha_inicio.text, 'key' : 'FechaInicio'},
#         {'value' : fecha_fin.text, 'key' : 'FechaTermino'},     
#         {'value' : plan, 'key' : 'Plan'},
#     ]
#      
#     seguro['emision'] = emision
    
    # coberturas
    lista_planes = list(atlas_root.find('Planes'))
    seguro_coberturas = {}
    
    # Inicializamos los valores como falso para todo, ya que puede que no aparezcan en el xml de entrada
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
    asistenciaVial = False
    asistenciaLegal = False
    
    for planes in list(lista_planes):
        if planes.find('Plan').text == plan:
            # costos
            ptotal = planes.find('PPrimaTot')
            seguro['costoTotal'] = int(math.ceil(float(ptotal.text)))
            pagos = []
            for recibo in list(planes.find('Recibos')):
                num = recibo.find('Recibo').text
                total = int(math.ceil(float(recibo.find('RPrimaTot').text)))
                pagos += [{'num' : num, 'total' : total}]
            seguro['pagos'] = pagos            
            for cob in list(planes.find('Coberturas')):
                if cob.find('Cobertura').text == '1':
                    # Daños Materiales
                    danosMateriales = True
                    try:
                        sumaDanosMateriales = int(float(cob.find('SumaAseg').text))
                    except ValueError:
                        sumaDanosMateriales = ''
                    try:
                        deducibleDanosMateriales = int(float(cob.find('Deducible').text))
                    except ValueError:
                        deducibleDanosMateriales = '0'
                if cob.find('Cobertura').text == '2':
                    # Robo Total
                    roboTotal = True
                    try:
                        sumaRoboTotal = int(float(cob.find('SumaAseg').text))
                    except ValueError:
                        sumaRoboTotal = ''
                    try:
                        deducibleRoboTotal = int(float(cob.find('Deducible').text))
                    except ValueError:
                        deducibleRoboTotal = '0'
                if cob.find('Cobertura').text == '3' or cob.find('Cobertura').text == '96':
                    # Daños Terceros
                    danosTerceros = True
                    try:
                        sumaDanosTerceros += int(float(cob.find('SumaAseg').text))
                    except ValueError:
                        sumaDanosTerceros = ''
                    try:
                        deducibleDanos = int(float(cob.find('Deducible').text))
                    except ValueError:
                        deducibleDanos = '0'
                if cob.find('Cobertura').text == '4':
                    # Gastos Medicos
                    gastosMedicos = True
                    try:
                        sumaGastosMedicos = int(float(cob.find('SumaAseg').text))
                    except ValueError:
                        sumaGastosMedicos = ''
                    try:
                        deducibleGastosMedicos = int(float(cob.find('Deducible').text))
                    except ValueError:
                        deducibleGastosMedicos = '0'
                if cob.find('Cobertura').text == '33':
                        # Asistencia Vial
                        asistenciaVial = True
                if cob.find('Cobertura').text == '34':
                        # Asistencia Legal
                        asistenciaLegal = True
    # Guarda todos los valores en el diccionario        
    # Guarda todos los valores en el diccionario        
    seguro_coberturas['danosMateriales'] = danosMateriales
    seguro_coberturas['danosMatDesc'] = {'sumaAsegurada' : 'VALOR COMERCIAL', 'deducible' : str(deducibleDanosMateriales)}
    seguro_coberturas['roboTotal'] = roboTotal
    seguro_coberturas['roboTotalDesc'] = {'sumaAsegurada' : 'VALOR COMERCIAL', 'deducible' : str(deducibleRoboTotal)}
    seguro_coberturas['danosTerceros'] = danosTerceros
    seguro_coberturas['danosTercerosDesc'] = {'sumaAsegurada' : str(sumaDanosTerceros), 'deducible' : str(deducibleDanos)}
    seguro_coberturas['gastosMedicos'] = gastosMedicos
    seguro_coberturas['gastosMedicosDesc'] = {'sumaAsegurada' : str(sumaGastosMedicos), 'deducible' : str(deducibleGastosMedicos)}
    seguro_coberturas['asistenciaVial'] = asistenciaVial
    seguro_coberturas['asistenciaLegal'] = asistenciaLegal
    seguro['cobertura'] = seguro_coberturas
    
    return seguro

def qualitas_parser(xmlroot):
    failure = xmlroot.find('.//echoStringResponse')
    if failure is not None:
        return None
    hasMeses = False
    if len(xmlroot.xpath('hasMeses')) == 1:
        if xmlroot.find('hasMeses').text == '1':
            hasMeses = True
    seguro = {'aseguradora' : 'qualitas', 'hasMeses' : hasMeses, 'depositoBancario':False}
    
    root = xmlroot.find('.//obtenerNuevaEmisionResult')
    if root is None:
        return(None)
    qualitas_root = etree.fromstring(xmlroot.find('.//obtenerNuevaEmisionResult').text.encode('utf-8'))
    error = qualitas_root.find('.//CodigoError')
    if error.text is not None:
        return(None)
    # coberturas
    coberturas = qualitas_root.findall('.//Coberturas')
    seguro_coberturas = {}
    
    # Inicializamos los valores como falso para todo, ya que puede que no aparezcan en el xml de entrada
    danosMateriales = False
    sumaDanosMateriales = '0'
    deducibleDanosMateriales = '0'
    roboTotal = False
    sumaRoboTotal = '0'
    deducibleRoboTotal = '0'
    danosTerceros = False
    sumaDanosTerceros = '0'
    deducibleDanos = '0'
    gastosMedicos = False
    sumaGastosMedicos = '0'
    deducibleGastosMedicos = '0'
    asistenciaVial = False
    asistenciaLegal = False
    
    for cob in list(coberturas):
        cobertura = cob.attrib['NoCobertura']
        if cobertura == '1':
            # Daños Materiales
            danosMateriales = True
            try:
                sumaDanosMateriales = cob.find('SumaAsegurada').text
            except ValueError:
                sumaDanosMateriales = ''
            try:
                deducibleDanosMateriales = str(int(cob.find('Deducible').text))
            except ValueError:
                deducibleDanosMateriales = '0'
        if cobertura == '3':
            # Robo Total
            roboTotal = True
            try:
                sumaRoboTotal = cob.find('SumaAsegurada').text
            except ValueError:
                sumaRoboTotal = ''
            try:
                deducibleRoboTotal = str(int(cob.find('Deducible').text))
            except ValueError:
                deducibleRoboTotal = '0'
        if cobertura == '4':
            # Danos Terceros
            danosTerceros = True
            try:
                sumaDanosTerceros = cob.find('SumaAsegurada').text
            except ValueError:
                sumaDanosTerceros = ''
            try:
                deducibleDanos = str(int(cob.find('Deducible').text))
            except ValueError:
                deducibleDanos = '0'
        if cobertura == '5':
            # Gastos Medicos
            gastosMedicos = True
            try:
                sumaGastosMedicos = cob.find('SumaAsegurada').text
            except ValueError:
                sumaGastosMedicos = ''
            try:
                deducibleGastosMedicos = str(int(cob.find('Deducible').text))
            except ValueError:
                deducibleGastosMedicos = '0'
        if cobertura == '6':
            # Asistencia Vial
            asistenciaVial = True
        if cobertura == '7':
            # Asistcia Legal
            asistenciaLegal = True
        if cobertura == '14':
            asistenciaLegal = True
        if cobertura == '34':
            asistenciaLegal = True
    # Guarda todos los valores en el diccionario        
    # Guarda todos los valores en el diccionario        
    seguro_coberturas['danosMateriales'] = danosMateriales
    seguro_coberturas['danosMatDesc'] = {'sumaAsegurada' : str(sumaDanosMateriales), 'deducible' : str(deducibleDanosMateriales)}
    seguro_coberturas['roboTotal'] = roboTotal
    seguro_coberturas['roboTotalDesc'] = {'sumaAsegurada' : str(sumaRoboTotal), 'deducible' : str(deducibleRoboTotal)}
    seguro_coberturas['danosTerceros'] = danosTerceros
    seguro_coberturas['danosTercerosDesc'] = {'sumaAsegurada' : str(sumaDanosTerceros), 'deducible' : str(deducibleDanos)}
    seguro_coberturas['gastosMedicos'] = gastosMedicos
    seguro_coberturas['gastosMedicosDesc'] = {'sumaAsegurada' : str(sumaGastosMedicos), 'deducible' : str(deducibleGastosMedicos)}
    seguro_coberturas['asistenciaVial'] = asistenciaVial
    seguro_coberturas['asistenciaLegal'] = asistenciaLegal
    seguro['cobertura'] = seguro_coberturas
    
    # costos
    ptotal = qualitas_root.find('Movimiento/Primas/PrimaTotal')
    seguro['costoTotal'] = int(math.ceil(float(ptotal.text)))
    
    recibos = qualitas_root.findall('Movimiento/Recibos')
    pagos = []
    for recibo in recibos:
        num = recibo.attrib['NoRecibo']
        total = int(math.ceil(float(recibo.find('PrimaTotal').text)))
        pagos += [{'num' : num, 'total' : total}]
    seguro['pagos'] = pagos
    return seguro
    
def mapfre_parser(xmlroot):
    no_se_cotiza = xmlroot.find('.//respuesta//echoStringResponse')
    if no_se_cotiza:
        return None
    result = xmlroot.find('.//param//result')
    if result == 'false':
        return None
    hasMeses = False
    if len(xmlroot.xpath('hasMeses')) == 1:
        if xmlroot.find('hasMeses').text == '1':
            hasMeses = True
    seguro = {'aseguradora' : 'mapfre', 'hasMeses' : hasMeses, 'depositoBancario':False}
    
#     root = xmlroot.find('.//data//cotizacion')
#     if root is None:
#         return None
    temp_fix = etree.tostring(xmlroot.find('.//data'))
    try:
        mapfre_root = etree.fromstring(temp_fix.split('Con.Open',1)[0].encode('utf-8'))
    except:
        mapfre_root = etree.fromstring(temp_fix.encode('utf-8'))
#     mapfre_root = etree.fromstring(xmlroot.find('.//data').text.encode('utf-8'))
    # coberturas
    coberturas = mapfre_root.findall('.//coberturas')
    seguro_coberturas = {}
    
    # Inicializamos los valores como falso para todo, ya que puede que no aparezcan en el xml de entrada
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
    asistenciaVial = False
    asistenciaLegal = False
    
    for cob in list(coberturas):
        cobertura = cob.find('COD_COB').text
        if cobertura == '4000':
            # Daños Materiales
            danosMateriales = True
            try:
                sumaDanosMateriales = int(cob.find('LIMMAXRESP').text)
            except:
                sumaDanosMateriales = 0
            try:
                deducibleDanosMateriales = str(int(cob.find('DEDUCIBLE').text))
            except:
                deducibleDanosMateriales = 0
        if cobertura == '4001':
            # Robo Total
            roboTotal = True
            try:
                sumaRoboTotal = int(cob.find('LIMMAXRESP').text)
            except:
                sumaRoboTotal = 0
            try:
                deducibleRoboTotal = str(int(cob.find('DEDUCIBLE').text))
            except:
                deducibleRoboTotal = 0
        if cobertura == '4010' or cobertura == '4011' or cobertura == '4068':
            # Danos Terceros
            danosTerceros = True
            try:
                sumaDanosTerceros += int(cob.find('LIMMAXRESP').text)
            except:
                sumaDanosTerceros += 0
            try:
                deducibleDanos = int(cob.find('DEDUCIBLE').text)
            except:
                deducibleDanos = 0
        if cobertura == '4006':
            # Gastos Medicos
            gastosMedicos = True
            try:
                sumaGastosMedicos = int(cob.find('LIMMAXRESP').text)
            except:
                sumaGastosMedicos = 0
            try:
                deducibleGastosMedicos = int(cob.find('DEDUCIBLE').text)
            except:
                deducibleGastosMedicos = 0
        if cobertura == '4003':
            # Asistencia Vial
            asistenciaVial = True
        if cobertura == '4004':
            # Asistcia Legal
            asistenciaLegal = True
        # Guarda todos los valores en el diccionario        
        # Guarda todos los valores en el diccionario        
    seguro_coberturas['danosMateriales'] = danosMateriales
    seguro_coberturas['danosMatDesc'] = {'sumaAsegurada' : str(sumaDanosMateriales), 'deducible' : str(deducibleDanosMateriales)}
    seguro_coberturas['roboTotal'] = roboTotal
    seguro_coberturas['roboTotalDesc'] = {'sumaAsegurada' : str(sumaRoboTotal), 'deducible' : str(deducibleRoboTotal)}
    seguro_coberturas['danosTerceros'] = danosTerceros
    seguro_coberturas['danosTercerosDesc'] = {'sumaAsegurada' : str(sumaDanosTerceros), 'deducible' : str(deducibleDanos)}
    seguro_coberturas['gastosMedicos'] = gastosMedicos
    seguro_coberturas['gastosMedicosDesc'] = {'sumaAsegurada' : str(sumaGastosMedicos), 'deducible' : str(deducibleGastosMedicos)}
    seguro_coberturas['asistenciaVial'] = asistenciaVial
    seguro_coberturas['asistenciaLegal'] = asistenciaLegal
    seguro['cobertura'] = seguro_coberturas
        
        # costos
    ptotal = mapfre_root.find('cotizacion/Totales/prima_total')
    seguro['costoTotal'] = int(math.ceil(float(ptotal.text)))
    
    recibos = mapfre_root.findall('cotizacion/Recibos/Recibo')
    pagos = []
    for recibo in recibos:
        num = recibo.find('Serie').text.split('/')[0]
        total = int(math.ceil(float(recibo.find('PrimaTotal').text)))
        pagos += [{'num' : num, 'total' : total}]
    seguro['pagos'] = pagos
    return seguro

    
    
    
    
    
    
    
    
    
    