# -*- coding: utf-8 -*-
import requests
import datetime
import logging
from lxml import html
from lxml.etree import tostring

URI_WS_VERIFICACIONES = 'https://api-datos.appspot.com/_ah/api/vehicles/v2/getEnvironmentVerifications/'
URI_WS_MULTAS = 'https://api-datos.appspot.com/_ah/api/vehicles/v2/getTrafficTickets/'
URI_WS_TENENCIAS = 'https://api-datos.appspot.com/_ah/api/vehicles/v2/getOwnershipTaxDebts/'
URI_WS_FINANZAS = 'https://data.finanzas.cdmx.gob.mx/sma/detallePlaca.php?placa='
URI_WS_FINANZAS_PAGO = 'https://data.finanzas.cdmx.gob.mx/formato_lc/infracciones/inf_html_folio3.php?folio='

class ApiGobInfoConsumer(object):
    """
    Consumidor del API de gobierno de informacion de multas, verificaciones y tenencias

    Examples:
        Obtiene los resultados de los tres servicios, multas, verificaciones y tenencias en formato JSON
            ApiGobInfoConsumer('123ABC').get()

        Ejecuta solo el servicio de multas
            ApiGobInfoConsumer('123ABC').multas()

        Ejecuta solo el servicio de verificaciones
            ApiGobInfoConsumer('123ABC').verificaciones()

        Ejecuta solo el servicio de tenencias
            ApiGobInfoConsumer('123ABC').tenencias()    

    ToDo: Como el nuevo ws solo va a traer las multas y tenencias con adeudo, se debe buscar en la base los que ya no 
    vengan en el ws y actualizar su situacion a "pagado"
    """

    def __init__(self, placa):
        """
        :param placa: La cadena de la placa del vehiculo
        """
        self.ejecucion_verificaciones = False
        self.ejecucion_infracciones = False
        self.ejecucion_tenencias = False
        self.ejecucion_finanzas = False

        self.placa = placa.replace(' ', '').replace('-', '').upper()
        self.resultado = {'verificaciones': [], 'infracciones': [], 'tenencias': ''}

      	self.logger = logging.getLogger('testlogging')
        hdlr = logging.FileHandler('/tmp/apigobinfo.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.INFO)

    def verificaciones(self):
        self.ejecucion_verificaciones = True
        placa = self.placa
        req = requests.get(URI_WS_VERIFICACIONES + placa + '')
        try:
            data = req.json()
        except ValueError:
            #             raise requests.exceptions.RequestException(req)
            return False
        verificaciones_list = []
        if 'verificationList' in data:
            for verificacion in data['verificationList']:
                if 'resultado' in verificacion:
                    verificacion_dict = {
                        'placa': placa,
                        'resultado': verificacion.get('resultado'),
                        'vigencia': datetime.datetime.strptime(verificacion.get('vigencia'), "%Y/%m/%d").strftime(
                            "%Y-%m-%d"),
                        'fecha_verificacion': datetime.datetime.strptime(verificacion.get('fechaVerificacion'),
                                                                         "%Y/%m/%d").strftime("%Y-%m-%d"),
                        'hora_verificacion': verificacion.get('horaVerificacion'),
                        'vin': verificacion.get('vin'),
                        'modelo': int(verificacion.get('modelo')),
                        'marca': verificacion.get('marca'),
                        'submarca': verificacion.get('submarca'),
                        'combustible': verificacion.get('combustible'),
                        'certificado': verificacion.get('certificado'),
                        'cancelado': verificacion.get('cancelado'),
                        'verificentro': verificacion.get('verificentro'),
                        'equipo_gdf': verificacion.get('equipoGDF'),
                        'linea': verificacion.get('linea'),
                        'causa_rechazo': verificacion.get('causaRechazo')
                    }
                    verificaciones_list.append(verificacion_dict)
        self.resultado['verificaciones'] = verificaciones_list
        return self

    def infracciones(self):
        self.ejecucion_infracciones = True
        placa = self.placa
        req = requests.get(URI_WS_MULTAS + placa + '')
        try:
            data = req.json()
        except ValueError:
            #             raise requests.exceptions.RequestException(req)
            return False
        infracciones_list = []
        if 'ticketList' in data:
            for infraccion in data['ticketList']:
                if 'folio' in infraccion:
                    infraccion_dict = {
                        'folio': infraccion.get('folio'),
                        'fecha': infraccion.get('fecha_infraccion'),
                        'fundamento': 'Art&amp;iacute;culo: ' + str(infraccion.get(
                            'articulo')) + ', Fracci&amp;oacute;n: ' + str(
                            infraccion.get('fraccion')) + ', Parrafo: , Inciso: ',
                        'motivo': infraccion.get('motivo'),
                        'sancion': infraccion.get(
                            'multa_salarios_minimos') + ' d&amp;iacute;as de salario m&amp;iacute;nimo',
                        'situacion': 'No pagada'
                    }
                    infracciones_list.append(infraccion_dict)
        self.resultado['infracciones'] = infracciones_list
        return self

    def finanzas(self, con_lineacaptura=False):
        self.ejecucion_finanzas = True
        placa = self.placa
        infracciones_list = self._finanzas_cdmx_parser_infraccion(placa, con_lineacaptura)
        self.resultado['infracciones'] = infracciones_list
        return self

    def tenencias(self):
        self.ejecucion_tenencias = True
        placa = self.placa
        req = requests.get(URI_WS_TENENCIAS + placa + '')
        try:
            data = req.json()
        except ValueError:
            #             raise requests.exceptions.RequestException(req)
            return False
        if 'tiene_adeudos' in data and data['tiene_adeudos'] == "1":
            tieneadeudos = "0"
            if len(data['adeudos']) > 1:
                tieneadeudos = "1"
            self.resultado['tenencias'] = {'placa': placa, 'adeudos': data['adeudos'],
                                           'tieneadeudos': tieneadeudos}
        return self

    def get(self, tipo=''):
        if tipo == 'verificaciones' or self.ejecucion_verificaciones:
            self.verificaciones()
        if tipo == 'infracciones' or self.ejecucion_infracciones:
            self.infracciones()
        if tipo == 'tenencias' or self.ejecucion_tenencias:
            self.tenencias()
        if tipo == '' \
                and self.ejecucion_tenencias == False \
                and self.ejecucion_infracciones == False \
                and self.ejecucion_verificaciones == False \
                and self.ejecucion_finanzas == False:

            self.verificaciones()
            self.finanzas()
            self.tenencias()

        respuesta_dict = {
            'consulta': {
                'placa': self.placa,
                'verificaciones': self.resultado['verificaciones'],
                'tenencias': self.resultado['tenencias'],
                'infracciones': self.resultado['infracciones']
            }}
        self.ejecucion_tenencias = False
        self.ejecucion_infracciones = False
        self.ejecucion_verificaciones = False
        self.ejecucion_finanzas = False
	self.logger.info(respuesta_dict)
        return respuesta_dict

    def _finanzas_cdmx_parser_infraccion(self, placa, con_lineacaptura):
        """
        Obtiene los datos de las infracciones del portal de la secretaria de finanzas de la cdmx
        :param placa: placa del vehiculo
        :return: 
        """
        page = requests.get(URI_WS_FINANZAS + placa)
        tree = html.fromstring(page.content)
        folio = ''
        fecha = ''
        situacion = ''
        motivo = ''
        url = ''
        sancion = ''
        fundamento_articulo = ''
        fundamento_fraccion = ''
        fundamento_parrafo = ''
        fundamento_inciso = ''

        infracciones_list = []
        for infraccion in tree.xpath('//*[@id="tablaDatos"]'):

            nodo_folio = html.fromstring(tostring(infraccion)).xpath('(//td[1])[1]/text()')
            if len(nodo_folio):
                folio = nodo_folio[0]
            else:
                continue

            nodo_fecha = html.fromstring(tostring(infraccion)).xpath('(//td[2])[1]/text()')
            if len(nodo_fecha):
                fecha = nodo_fecha[0]

            nodo_situacion = html.fromstring(tostring(infraccion)).xpath('(//td[3])[1]/descendant::*/text()')
            if len(nodo_situacion):
                situacion = nodo_situacion[0]
                situacion = situacion.strip()
                if situacion == 'No pagada':
                    nodo_url_linea_captura = html.fromstring(tostring(infraccion)).xpath('(//td[4]/a)[1]')
                    if len(nodo_url_linea_captura):
                        # url = nodo_url_linea_captura[0].attrib['href']
                        url = URI_WS_FINANZAS_PAGO + folio

            nodo_motivo = html.fromstring(tostring(infraccion)).xpath('(//tr[2]/td[2])[1]/descendant::*/text()')
            if len(nodo_motivo):
                motivo = nodo_motivo[0]
                motivo = motivo.strip()

            nodo_fundamento = html.fromstring(tostring(infraccion)).xpath('//tr[3]/td[2]/text()')
            if len(nodo_fundamento):
                fundamento_articulo, fundamento_fraccion, fundamento_parrafo, fundamento_inciso = map(
                    lambda x: x.strip(', '), nodo_fundamento)

            nodo_sancion = html.fromstring(tostring(infraccion)).xpath('//tr[4]/td[2]/descendant::*/text()')
            if len(nodo_sancion):
                sancion = nodo_sancion[0]
                sancion = sancion.strip()

            """
            dict_infraccion = {
                'folio': folio,
                'fecha_infraccion': fecha,
                'situacion': situacion,
                'motivo': motivo,
                'fundamento_articulo': fundamento_articulo,
                'fundamento_fraccion': fundamento_fraccion,
                'fundamento_parrafo': fundamento_parrafo,
                'fundamento_inciso': fundamento_inciso,
                'sancion': sancion,
                'url_linea_captura': url,
                'datos_linea_captura': dict_linea_captura
            }
            """


            infraccion_dict = {
                'folio': folio,
                'fecha': fecha,
                'fundamento': 'Art&amp;iacute;culo: ' + str(fundamento_articulo) +
                              ', Fracci&amp;oacute;n: ' + str(fundamento_fraccion) +
                              ', Parrafo: ' + str(fundamento_parrafo) +
                              ', Inciso: ' + str(fundamento_inciso),
                'motivo': motivo,
                'sancion': sancion,
                'situacion': situacion
            }

            if con_lineacaptura and url:
                dict_linea_captura = self._finanzas_cdmx_linea_captura(url)
                infraccion_dict['url_linea_captura'] = url
                infraccion_dict['datos_linea_captura'] = dict_linea_captura

            infracciones_list.append(infraccion_dict)
        return infracciones_list

    def _finanzas_cdmx_linea_captura(self, url):
        """
        Obtiene los valores asociados a la linea de captura para el pago de infraccion asi como su descuento
        :param url: El url para obtener la pag con los datos
        :return: dict
        """
        page = requests.get(url)
        tree = html.fromstring(page.content)
        mapa_campos_dict = {
            'clave': 'clave_pago',
            'anio_vig': 'vigencia_anio',
            'mes_vig': 'vigencia_mes',
            'dia_vig': 'vigencia_dia',
            'salmin': 'monto_unidad_cuenta',
            'salarios': 'cantidad',
            'importe': 'importe',
            'descuento': 'descuento',
            'actualizacion': 'actualizacion',
            'recargos': 'recargos',
            'total': 'total',
            'lineacaptura': 'linea_captura',
            'folio': 'folio',
        }
        resultado = {}
        for campo in tree.xpath('//input[@type="hidden"]'):
            if campo.name in mapa_campos_dict:
                resultado[mapa_campos_dict[campo.name]] = campo.value
        return resultado
