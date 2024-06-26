#Query básico para la descarga de información de compañias
companies_query = """select	V.correo_vendedor, COMP.compania_sap, COMP.nombre_compania, COMP.negociacion, COMP.correo_compania, COMP.telefono_compania, COMP.nit_compania, PS.abreviatura, COMP.estado_compania, COMP.banco, COMP.centro, COMP.informacion_legal, COMP.direccion_legal, COMP.metodo_pago, COMP.despacho, COMP.catalogo_id, COMP.canal
from	compania COMP
		inner join pais PS on (PS.pais_id = COMP.pais_compania)
		inner join vendedor V on (V.vendedor_id = COMP.vendedor_id)"""

#Query básico para la descarga de información de materia prima
raw_material_query = """select	MP.materia_prima_id, MP.nombre, MP.codigo, MP.es_urea, MP.nutrientes, MP.categoria, MP.sector, B.bodega_sap, MP.estado, MP.stock_minimo, PS.abreviatura
from	materia_prima MP
		inner join bodega B on (B.bodega_id = MP.bodega_id)
		inner join pais PS on (PS.pais_id = B.pais_bodega)"""

#Query básico para la descarga de información de clientes
clients_query ="""select	U.nombre_usuario, U.apellido_usuario, U.correo_usuario, U.telefono_usuario, U.estado_usuario, COMP.compania_sap, U.password_usuario, U.usuario_ref, PS.abreviatura
from	usuario U
		inner join compania COMP on (COMP.compania_id = U.compania_id)
		inner join pais PS on (PS.pais_id = COMP.pais_compania)"""

#Query básico para la descarga de información de destinatarios
addressee_query = """select	COMP.compania_sap, DES.destinatario_sap, DES.ciudad, DES.departamento, DES.zip, DES.telefono_destinatario,
		DES.detalle, DES.punto, DES.estado_id, DES.contacto, DES.despacho, DES.facturacion, DES.nombre_destinatario,
		DES.apellido_destinatario, DES.envio, DES.nombre_referencia
from	destinatario DES
		inner join compania COMP on (COMP.compania_id = DES.compania_id)
		inner join pais PS on (PS.pais_id = COMP.pais_compania)
		inner join vendedor V on (V.vendedor_id = COMP.vendedor_id)"""

#Función que construye el query para la descarga con o sin filtro de la información de materia prima
def companies_download(pais, correo_vendedor, catalogo, estado):
	conditional_str = ""

	if pais is not None or "":
		if conditional_str == "":
			conditional_str = "where	(PS.abreviatura = '{}')".format(pais)
		else:
			conditional_str = conditional_str + " and (PS.abreviatura = '{}')".format(pais)

	if correo_vendedor is not None or "":
		if conditional_str == "":
			conditional_str = "where	(V.correo_vendedor = '{}')".format(correo_vendedor)
		else:
			conditional_str = conditional_str + " and (V.correo_vendedor = '{}')".format(correo_vendedor)

	if catalogo is not None or "":
		if conditional_str == "":
			conditional_str = "where	(COMP.catalogo_id = '{}')".format(catalogo)
		else:
			conditional_str = conditional_str + " and (COMP.catalogo_id = '{}')".format(catalogo)

	if estado is not None or "":
		if conditional_str == "":
			conditional_str = "where	(COMP.estado_compania = {})".format(estado)
		else:
			conditional_str = conditional_str + " and (COMP.estado_compania = {})".format(estado)

	return companies_query + '\n'+ conditional_str

#Función que construye el query para la descarga con o sin filtro de la información de materia prima
def raw_material_download(pais, bodega_sap, categoria, urea, estado, sector):
	conditional_str = ""

	if pais is not None or "":
		if conditional_str == "":
			conditional_str = "where	(PS.abreviatura = '{}')".format(pais)
		else:
			conditional_str = conditional_str + " and (PS.abreviatura = '{}')".format(pais)
	if bodega_sap is not None or "":
		if conditional_str == "":
			conditional_str = "where	(B.bodega_sap = '{}')".format(bodega_sap)
		else:
			conditional_str = conditional_str + " and (B.bodega_sap = '{}')".format(bodega_sap)
	if categoria is not None or "":
		if conditional_str == "":
			conditional_str = "where	(MP.categoria = '\x7B"+ str(categoria) +"\x7D')"
		else:
			conditional_str = conditional_str + " and (MP.categoria = '\x7B"+ str(categoria) +"\x7D')"
	if urea is not None or "":
		if conditional_str == "":
			conditional_str = "where	(MP.es_urea = {})".format(urea)
		else:
			conditional_str = conditional_str + " and (MP.es_urea = {})".format(urea)
	if estado is not None or "":
		if conditional_str == "":
			conditional_str = "where	(MP.estado = {})".format(estado)
		else:
			conditional_str = conditional_str + " and (MP.estado = {})".format(estado)
	if sector is not None or "":
		if conditional_str == "":
			conditional_str = "where	(MP.sector = '{}')".format(sector)
		else:
			conditional_str = conditional_str + " and (MP.sector = '{}')".format(sector)

	return raw_material_query + '\n'+ conditional_str

#Función que construye el query para la descarga con o sin filtro de la información de clientes
def clients_download(compania_sap, pais, estado):
	conditional_str = ""

	if compania_sap is not None or "":
		if conditional_str == "":
			conditional_str = "where	(COMP.compania_sap = '{}')".format(compania_sap)
		else:
			conditional_str = conditional_str + " and (COMP.compania_sap = '{}')".format(compania_sap)

	if pais is not None or "":
		if conditional_str == "":
			conditional_str = "where	(PS.abreviatura = '{}')".format(pais)
		else:
			conditional_str = conditional_str + " and (PS.abreviatura = '{}')".format(pais)

	if estado is not None or "":
		if conditional_str == "":
			conditional_str = "where	(U.estado_usuario = {})".format(estado)
		else:
			conditional_str = conditional_str + " and (U.estado_usuario = {})".format(estado)

	return clients_query + '\n' + conditional_str

#Función que construye el query para la descarga con o sin filtro de la información de destinatarios
def addressee_download(compania_sap, pais, correo_vendedor, estado):
	conditional_str = ""

	if compania_sap is not None or "":
		if conditional_str == "":
			conditional_str = "where	(COMP.compania_sap = '{}')".format(compania_sap)
		else:
			conditional_str = conditional_str + " and (COMP.compania_sap = '{}')".format(compania_sap)

	if pais is not None or "":
		if conditional_str == "":
			conditional_str = "where	(PS.abreviatura = '{}')".format(pais)
		else:
			conditional_str = conditional_str + " and (PS.abreviatura = '{}')".format(pais)

	if correo_vendedor is not None or "":
		if conditional_str == "":
			conditional_str = "where	(V.correo_vendedor = '{}')".format(correo_vendedor)
		else:
			conditional_str = conditional_str + " and (V.correo_vendedor = '{}')".format(correo_vendedor)

	if estado is not None or "":
		if conditional_str == "":
			conditional_str = "where	(DES.estado_id = {})".format(estado)
		else:
			conditional_str = conditional_str + " and (DES.estado_id = {})".format(estado)

	return addressee_query + '\n' + conditional_str

def identifier_retreiver(column, table, condition1, condition2):
	querystring = []
	querystring.append("select")
	querystring.append(column)
	querystring.append("from")
	querystring.append(table)
	querystring.append("where (")
	querystring.append(condition1)
	querystring.append("=")
	querystring.append(condition2)
	querystring.append(")")
	newquery = ' '.join(querystring)
	return (newquery)