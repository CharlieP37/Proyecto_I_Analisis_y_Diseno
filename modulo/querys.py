#Query básico para la descarga de información de materia prima
rawmaterialquery = """select	MP.materia_prima_id, MP.nombre, MP.codigo, MP.es_urea, MP.nutrientes, MP.categoria, MP.sector, B.bodega_sap, MP.estado, MP.stock_minimo, PS.abreviatura
from	materia_prima MP
		inner join bodega B on (B.bodega_id = MP.bodega_id)
		inner join pais PS on (PS.pais_id = B.pais_bodega)"""

#Query básico para la descarga de información de clientes
clientsquery ="""select	U.nombre_usuario, U.apellido_usuario, U.correo_usuario, U.telefono_usuario, U.estado_usuario, COMP.compania_sap, U.password_usuario, U.usuario_ref, PS.abreviatura
from	usuario U
		inner join compania COMP on (COMP.compania_id = U.compania_id)
		inner join pais PS on (PS.pais_id = COMP.pais_compania)"""

#Query básico para la descarga de información de destinatarios
addresseequery = """select	COMP.compania_sap, DES.destinatario_sap, DES.ciudad, DES.departamento, DES.zip, DES.telefono_destinatario,
		DES.detalle, DES.punto, DES.estado_id, DES.contacto, DES.despacho, DES.facturacion, DES.nombre_destinatario,
		DES.apellido_destinatario, DES.envio, DES.nombre_referencia
from	destinatario DES
		inner join compania COMP on (COMP.compania_id = DES.compania_id)
		inner join pais PS on (PS.pais_id = COMP.pais_compania)
		inner join vendedor V on (V.vendedor_id = COMP.vendedor_id)"""

#Función que construye el query para la descarga con o sin filtro de la información de materia prima
def rawmaterialdownload(pais, bodega_sap, categoria, urea, estado, sector):
	conditionalstr = ""
 
	if pais is not None or "":
		if conditionalstr == "":
			conditionalstr = "where	(PS.abreviatura = '{}')".format(pais)
		else:
			conditionalstr = conditionalstr + " and (PS.abreviatura = '{}')".format(pais)
	if bodega_sap is not None or "":
		if conditionalstr == "":
			conditionalstr = "where	(B.bodega_sap = '{}')".format(bodega_sap)
		else:
			conditionalstr = conditionalstr + " and (B.bodega_sap = '{}')".format(bodega_sap)
	if categoria is not None or "":
		if conditionalstr == "":
			conditionalstr = "where	(MP.categoria = '\x7B"+ str(categoria) +"\x7D')"
		else:
			conditionalstr = conditionalstr + " and (MP.categoria = '\x7B"+ str(categoria) +"\x7D')"
	if urea is not None or "":
		if conditionalstr == "":
			conditionalstr = "where	(MP.es_urea = {})".format(urea)
		else:
			conditionalstr = conditionalstr + " and (MP.es_urea = {})".format(urea)
	if estado is not None or "":
		if conditionalstr == "":
			conditionalstr = "where	(MP.estado = {})".format(estado)
		else:
			conditionalstr = conditionalstr + " and (MP.estado = {})".format(estado)
	if sector is not None or "":
		if conditionalstr == "":
			conditionalstr = "where	(MP.sector = '{}')".format(sector)
		else:
			conditionalstr = conditionalstr + " and (MP.sector = '{}')".format(sector)
	
	return rawmaterialquery + '\n'+ conditionalstr

#Función que construye el query para la descarga con o sin filtro de la información de clientes
def clientsdownload(compania_sap, pais, estado):
	conditionalstr = ""

	if compania_sap is not None or "":
		if conditionalstr == "":
			conditionalstr = "where	(COMP.compania_sap = '{}')".format(compania_sap)
		else:
			conditionalstr = conditionalstr + " and (COMP.compania_sap = '{}')".format(compania_sap)

	if pais is not None or "":
		if conditionalstr == "":
			conditionalstr = "where	(PS.abreviatura = '{}')".format(pais)
		else:
			conditionalstr = conditionalstr + " and (PS.abreviatura = '{}')".format(pais)

	if estado is not None or "":
		if conditionalstr == "":
			conditionalstr = "where	(U.estado_usuario = {})".format(estado)
		else:
			conditionalstr = conditionalstr + " and (U.estado_usuario = {})".format(estado)
	
	return clientsquery + '\n' + conditionalstr

#Función que construye el query para la descarga con o sin filtro de la información de destinatarios
def addresseedownload(compania_sap, pais, correo_vendedor, estado):
	conditionalstr = ""
 
	if compania_sap is not None or "":
		if conditionalstr == "":
			conditionalstr = "where	(COMP.compania_sap = '{}')".format(compania_sap)
		else:
			conditionalstr = conditionalstr + " and (COMP.compania_sap = '{}')".format(compania_sap)

	if pais is not None or "":
		if conditionalstr == "":
			conditionalstr = "where	(PS.abreviatura = '{}')".format(pais)
		else:
			conditionalstr = conditionalstr + " and (PS.abreviatura = '{}')".format(pais)

	if correo_vendedor is not None or "":
		if conditionalstr == "":
			conditionalstr = "where	(V.correo_vendedor = '{}')".format(correo_vendedor)
		else:
			conditionalstr = conditionalstr + " and (V.correo_vendedor = '{}')".format(correo_vendedor)

	if estado is not None or "":
		if conditionalstr == "":
			conditionalstr = "where	(DES.estado_id = {})".format(estado)
		else:
			conditionalstr = conditionalstr + " and (DES.estado_id = {})".format(estado)

	return addresseequery + '\n' + conditionalstr