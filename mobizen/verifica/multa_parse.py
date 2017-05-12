# -*- coding: utf-8 -*- 
def get_infraccion(articulo, fraccion, parrafo=None, inciso=None):
    ## 
    ## 5-19, 22-25, 31, 32, 34
    short_fundamento = None #u'No Se Encuentra en el Catálogo'
    if articulo == 5:
        if fraccion == u'I':
            short_fundamento = u'Sin Licencia'
        elif fraccion == u'II':
            short_fundamento = u'Sin Tarjeta Circulación'
        elif fraccion == u'III':
            short_fundamento = u'Desobedecer Señalamientos'
        elif fraccion == u'IV':
            short_fundamento = u'Sentido Contrario'
        elif fraccion == u'V':
            short_fundamento = u'Exceso de Velocidad'
        elif fraccion == u'VI':
            short_fundamento = u'Sin Cinturón de Seguridad'
        elif fraccion == u'VII':
            short_fundamento = u'Vehículo Extranjero Sin Papeles'
        elif fraccion == u'VIII':
            short_fundamento = u'Rebase Ilegal'
        elif fraccion == u'IX':
            short_fundamento = u'Giro Sin Aviso'
    elif articulo == 6:
        if fraccion == u'I':
            short_fundamento = u'Circular Sobre Banquetas'
        elif fraccion == u'II':
            short_fundamento = u'Circular en Contraflujo'
        elif fraccion == u'III':
            short_fundamento = u'Invasión Paso Peatonal'
        elif fraccion == u'IV':
            short_fundamento = u'Reversa Prohibida'
        elif fraccion == u'V':
            short_fundamento = u'Vuelta Prohibida'
        elif fraccion == u'VI':
            short_fundamento = u'Carril Prohibido'
        elif fraccion == u'VII':
            short_fundamento = u'Ascenso/Descenso Prohibido'
        elif fraccion == u'VIII':
            short_fundamento = u'Exceso de Pasajeros'
        elif fraccion == u'IX':
            short_fundamento = u'Menores al Frente'
        elif fraccion == u'X':
            short_fundamento = u'Pasajero en Carrocería'
        elif fraccion == u'XI':
            short_fundamento = u'Uso de Celular'
        elif fraccion == u'XII':
            short_fundamento = u'Obstruir Eventos Cívicos'
        elif fraccion == u'XIII':
            short_fundamento = u'Antiradar'
        elif fraccion == u'XIV':
            short_fundamento = u'Ofender Autoridad'
        elif fraccion == u'XV':
            short_fundamento = u'Vuelta Prohibida'
        elif fraccion == u'XVI':
            short_fundamento = u'Invadir Ciclovías'
        elif fraccion == u'XVII':
            short_fundamento = u'Estacionar en Ciclovías'
    elif articulo == 7:
        short_fundamento = u'No Circula'            
    elif articulo == 8:
        if fraccion == u'I':
            short_fundamento = u'Desobedecer Agente'
        elif fraccion == u'II':
            short_fundamento = u'Ignorar Luz Roja'
        elif fraccion == u'III':
            short_fundamento = u'No Ceder Paso'
        elif fraccion == u'IV':
            short_fundamento = u'No Respetar Luz Intermitente'
        elif fraccion == u'VI':
            short_fundamento = u'Obstruit Calle Transversal'
        elif fraccion == u'VII':
            short_fundamento = u'Vuelta Continua'
        elif fraccion == u'XI':
            short_fundamento = u'No Ceder Paso'
        elif fraccion == u'XII':
            short_fundamento = u'No Ceder Paso'
        else:
            short_fundamento = u'No Respetar Preferencia'        
    elif articulo == 9:
        if fraccion == u'I':
            short_fundamento = u'Exceso de Velocidad'
        elif fraccion == u'II':
            short_fundamento = u'Exceso de Velocidad'
        else:
            short_fundamento = u'No Ceder Paso a Peatón'
    elif articulo == 10:
        if fraccion == u'X':
            short_fundamento = u'Vuelta Prohibida'
        elif fraccion == u'VI':
            short_fundamento = u'No Respetar Intersecciones'
    elif articulo == 11:
        short_fundamento = u'No Ceder Paso a Ciclista'
    elif articulo == 12:
        if fraccion == u'I':
            short_fundamento = u'Estacionar en Vías Primarias'
        elif fraccion == u'III':
            short_fundamento = u'Estacionar en Doble Fila'
        elif fraccion == u'IX':
            short_fundamento = u'Estacionar en Área Peatonal'
        else:
            short_fundamento = u'Estacionar en Zona Prohibida'
    elif articulo == 13:
        short_fundamento = u'Parquímetro Agotado'
    elif articulo == 14:
        if fraccion == u'I':
            short_fundamento = u'Reparaciones en Vía Pública'
        elif fraccion == u'IV':
            short_fundamento = u'Vehículo Abandonado'
        elif fraccion == u'V':
            short_fundamento = u'Reservar Estacionamiento'
        elif fraccion == u'VI':
            short_fundamento = u'Arrancones'
        else:
            short_fundamento = u'Obstruir Vialidad'
    elif articulo == 15:
        short_fundamento = u'No Señalizar'
    elif articulo == 16:
        if fraccion == u'I':
            short_fundamento = u'No Traer Gasolina'
        elif fraccion == u'II':
            short_fundamento = u'Faros No Funcionan'
        elif fraccion == u'III':
            short_fundamento = u'Luces Adicionales No Sirven'
        elif fraccion == u'IV':
            short_fundamento = u'Cuartos No Funcionan'
        elif fraccion == u'V':
            short_fundamento = u'Llantas en Mal Estado'
        elif fraccion == u'VI':
            short_fundamento = u'Falta Equipo de Emergencia'
        elif fraccion == u'VII':
            short_fundamento = u'Falta de Espejos'
        elif fraccion == u'VIII':
            short_fundamento = u'Defensas Incompletas'
        elif fraccion == u'IX':
            short_fundamento = u'No Cuenta Con Cinturones'
        elif fraccion == u'X':
            short_fundamento = u'Parabrisas Roto'
        elif fraccion == u'XI':
            short_fundamento = u'No Cuenta con GPS'
    elif articulo == 17:
        if fraccion == u'I':
            short_fundamento = u'Sin Placas/Permiso'
        elif fraccion == u'II':
            short_fundamento = u'No Porta Calcomanía'
        elif fraccion == u'III':
            short_fundamento = u'Sin Verificación Vigente'
        elif fraccion == u'IV':
            short_fundamento = u'No Porta Distintivo Discapacidad'            
    elif articulo == 18:
        short_fundamento = u'Remolque No Cubre Requisitos'
    elif articulo == 19:
        if fraccion == u'I':
            short_fundamento = u'Imagen Indebida'
        elif fraccion == u'II':
            short_fundamento = u'Dispositivos Indebidos'
        elif fraccion == u'III':
            short_fundamento = u'Faros Deslumbrantes'
        elif fraccion == u'IV':
            short_fundamento = u'Neón en Placa'
        elif fraccion == u'V':
            short_fundamento = u'Publicidad No Autorizada'
        elif fraccion == u'VI':
            short_fundamento = u'TV en Cabina'
        elif fraccion == u'VII':
            short_fundamento = u'Polarizado Extremo'
    elif articulo == 22:
        if fraccion == u'I':
            short_fundamento = u'Sin Tarjetón'
        elif fraccion == u'II':
            short_fundamento = u'Circular por Carril Derecho'
        elif fraccion == u'III':
            short_fundamento = u'Circular con Puertas Abiertas'
        elif fraccion == u'IV':
            short_fundamento = u'Ascenso/Descenso Prohibido'
        elif fraccion == u'V':
            short_fundamento = u'Ascenso/Descenso en Movimiento'
        elif fraccion == u'VI':
            short_fundamento = u'Circular Sin Luces Interiores'
        elif fraccion == u'VII':
            short_fundamento = u'Estacionar/Base No Autorizada'
        elif fraccion == u'VIII':
            short_fundamento = u'Bicitaxi'
        elif fraccion == u'IX':
            short_fundamento = u'Rebase Ilegal a Ciclistas'
    elif articulo == 23:
        if fraccion == u'I':
            short_fundamento = u'Rebase Ilegal'
        elif fraccion == u'II':
            short_fundamento = u'Ascenso/Descenso Prohibido'
        elif fraccion == u'III':
            short_fundamento = u'Vidrios Polarizados'
        elif fraccion == u'IV':
            short_fundamento = u'Visibilidad Obstruida'
        elif fraccion == u'V':
            short_fundamento = u'Pantallas/TVs Prohibidas'
        elif fraccion == u'VI':
            short_fundamento = u'Faros Deslumbrantes'
        elif fraccion == u'VII':
            short_fundamento = u'Cargar Gasolina con Pasaje'
        elif fraccion == u'VIII':
            short_fundamento = u'Circular Carriles Prohibidos'
        elif parrafo == u'PENULTIMO':
            short_fundamento = u'Circular en Carriles Centrales'
    elif articulo == 24:
        if fraccion == u'I':
            short_fundamento = u'Circular en Carriles Centrales'
        elif fraccion == u'II':
            short_fundamento = u'Carga Irregular'
    elif articulo == 25:
        if fraccion == u'I':
            short_fundamento = u'Circular Por Carril Derecho'
        elif fraccion == u'II':
            short_fundamento = u'No Respetar Días y Horarios'
        elif fraccion == u'III':
            short_fundamento = u'Estacionar/Base No Autorizada'
        elif fraccion == u'IV':
            short_fundamento = u'Sin Placas/Permiso'
        elif fraccion == u'V':
            short_fundamento = u'Sin Licencia Vigente'
        elif fraccion == u'VI':
            short_fundamento = u'Derrame de Sustancias'
        elif fraccion == u'VII':
            short_fundamento = u'Carga/Descarga Irregular'
        elif fraccion == u'VIII':
            short_fundamento = u'Sin Señalamientos/Autorización'
    elif articulo == 29:
        if fraccion == u'IV':
            short_fundamento = u'Por No Usar Casco'
        elif fraccion == u'VI':
            short_fundamento = u'Rebase Ilegal'
        elif fraccion == u'IX':
            short_fundamento = u'Circular Sin Luces'
    elif articulo == 30:
        if fraccion == u'I':
            short_fundamento = u'Circular Por Carril Controlado'
        elif fraccion == u'II':
            short_fundamento = u'Circular Entre Carriles'
        elif fraccion == u'XII':
            short_fundamento = u'Estacionar en Doble Fila'
    elif articulo == 31:
        short_fundamento = u'Bajo Influencia del Alcohol'
    elif articulo == 32:
        short_fundamento = u'Bajo Influencia del Alcohol'
    elif articulo == 34:
        short_fundamento = u'Sin Seguro Responsabilidad Civil'
    elif articulo == 38:
        if fraccion == u'II':
            short_fundamento = u'Utilizar celular'
    elif articulo == 43:
        if fraccion == u'I':
            short_fundamento = u'Llantas que dañan la superficie'
        elif fraccion == u'II':
            short_fundamento = u'Usar Faros Deslumbrantes'
        elif fraccion == u'III':
            short_fundamento = u'Luces neón o portaplacas'
        elif fraccion == u'IV':
            short_fundamento = u'Usar Anti Radar'
        elif fraccion == u'V':
            short_fundamento = u'Ruido Excesivo (Escape)'
        elif fraccion == u'VI':
            short_fundamento = u'Ruido Excesivo (Claxón)'
        elif fraccion == u'VII':
            short_fundamento = u'Polarizado mayor al 20%'
    elif articulo == 45:
        if fraccion == u'I':
            short_fundamento = u'Sin Placas'
        elif fraccion == u'II':
            short_fundamento = u'Sin Calcomanía de Circulación'
        elif fraccion == u'III':
            short_fundamento = u'Sin Verificación'
        elif fraccion == u'IV':
            short_fundamento = u'Sin Tarjeta de Circulación'
    return short_fundamento

def parse_fundamento(fundamento=None):
    if not fundamento:
        return None
    comps = fundamento.split(',')
    try:
        articulo = int(comps[0].split(': ')[1])
    except:
        articulo = 0
    fraccion = comps[1].split(': ')[1]
    parrafo = comps[2].split(': ')[1]
    return get_infraccion(articulo, fraccion, parrafo)
    
def parse_sancion(sancion):
    parts = sancion.split()
    if len(parts)==1:
        return sancion
    return sancion.split()[0]
    