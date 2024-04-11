import pandas as pd

# Compañia
def create_query_update_company(data, values):
    consult = "UPDATE compania SET"
    columns = ['vendedor_id = %s', 'compania_sap = %s', 'nombre_compania = %s']

    if not pd.isnull(data['negociacion']):
        columns.append('negociacion = %s')
        values.append(data['negociacion'])

    if not pd.isnull(data['correo_compania']):
        columns.append('correo_compania = %s')
        values.append(data['correo_compania'])

    if not pd.isnull(data['telefono_compania']):
        columns.append('telefono_compania = %s')
        values.append(data['telefono_compania'])

    if not pd.isnull(data['nit_compania']):
        columns.append('nit_compania = %s')
        values.append(data['nit_compania'])

    columns.append('pais_compania = %s')
    values.append(data['pais_compania'])

    if not pd.isnull(data['estado_compania']):
        columns.append('estado_compania = %s')
        values.append(data['estado_compania'])

    if not pd.isnull(data['banco']):
        columns.append('banco = %s')
        values.append(str(data['banco'].replace("[", "{").replace("]", "}")))

    if not pd.isnull(data['centro']):
        columns.append('centro = %s')
        values.append(str(data['centro'].replace("[", "{").replace("]", "}")))

    if not pd.isnull(data['informacion_legal']):
        columns.append('informacion_legal = %s')
        values.append(data['informacion_legal'])

    if not pd.isnull(data['direccion_legal']):
        columns.append('direccion_legal = %s')
        values.append(data['direccion_legal'])

    if not pd.isnull(data['metodo_pago']):
        columns.append('metodo_pago = %s')
        values.append(str(data['metodo_pago'].replace("[", "{").replace("]", "}")))

    if not pd.isnull(data['despacho']):
        columns.append('despacho = %s')
        values.append(data['despacho'])

    if not pd.isnull(data['catalogo_id']):
        columns.append('catalogo_id = %s')
        values.append(data['catalogo_id'])

    if not pd.isnull(data['canal']):
        columns.append('canal = %s')
        values.append(str(data['canal'].replace("[", "{").replace("]", "}")))

    consult = f"{consult}{columns}"
    consult = consult.replace("[", " ").replace("]", "")

    return consult + ' WHERE compania_sap = %s'

def create_query_insert_company(data, values):
    consult = "INSERT INTO compania"
    columns = ['vendedor_id', 'compania_sap', 'nombre_compania']

    if not pd.isnull(data['negociacion']):
        columns.append('negociacion')
        values.append(data['negociacion'])

    if not pd.isnull(data['correo_compania']):
        columns.append('correo_compania')
        values.append(data['correo_compania'])

    if not pd.isnull(data['telefono_compania']):
        columns.append('telefono_compania')
        values.append(data['telefono_compania'])

    if not pd.isnull(data['nit_compania']):
        columns.append('nit_compania')
        values.append(data['nit_compania'])

    columns.append('pais_compania')
    values.append(data['pais_compania'])

    if not pd.isnull(data['estado_compania']):
        columns.append('estado_compania')
        values.append(data['estado_compania'])

    if not pd.isnull(data['banco']):
        columns.append('banco')
        values.append(str(data['banco'].replace("[", "{").replace("]", "}")))

    if not pd.isnull(data['centro']):
        columns.append('centro')
        values.append(str(data['centro'].replace("[", "{").replace("]", "}")))

    if not pd.isnull(data['informacion_legal']):
        columns.append('informacion_legal')
        values.append(data['informacion_legal'])

    if not pd.isnull(data['direccion_legal']):
        columns.append('direccion_legal')
        values.append(data['direccion_legal'])

    if not pd.isnull(data['metodo_pago']):
        columns.append('metodo_pago')
        values.append(str(data['metodo_pago'].replace("[", "{").replace("]", "}")))

    if not pd.isnull(data['despacho']):
        columns.append('despacho')
        values.append(data['despacho'])

    if not pd.isnull(data['catalogo_id']):
        columns.append('catalogo_id')
        values.append(data['catalogo_id'])

    if not pd.isnull(data['canal']):
        columns.append('canal')
        values.append(str(data['canal'].replace("[", "{").replace("]", "}")))

    consult = f"{consult}{columns}"
    consult = consult.replace("[", "(").replace("]", ")")

    value = ['%s']
    while len(value) < len(columns):
        value.append('%s')

    values = f" values {value}"
    values = values.replace("[", "(").replace("]", ")")

    return consult + values

# Materia prima
def create_query_update_raw_material(data, values):
    consult = "UPDATE materia_prima SET"
    columns = ['nombre = %s', 'codigo = %s']

    if not pd.isnull(data['es_urea']):
        columns.append('es_urea = %s')
        values.append(data['es_urea'])

    if not pd.isnull(data['nutrientes']):
        columns.append('nutrientes = %s')
        values.append(data['nutrientes'])

    if not pd.isnull(data['categoria']):
        columns.append('categoria = %s')
        values.append(str(data['categoria'].replace("[", "{").replace("]", "}")))

    if not pd.isnull(data['sector']):
        columns.append('sector = %s')
        values.append(data['sector'])

    columns.append('bodega_id = %s')
    values.append(data['bodega_id'])

    if not pd.isnull(data['estado']):
        columns.append('estado = %s')
        values.append(data['estado'])

    if not pd.isnull(data['stock_minimo']):
        columns.append('stock_minimo = %s')
        values.append(data['stock_minimo'])

    consult = f"{consult}{columns}"
    consult = consult.replace("[", " ").replace("]", "")

    return consult + ' WHERE codigo = %s'

def create_query_insert_raw_material(data, values):
    consult = "INSERT INTO materia_prima"
    columns = ['nombre', 'codigo']
    # categoria', 'sector']
    if not pd.isnull(data['es_urea']):
        columns.append('es_urea')
        values.append(data['es_urea'])

    if not pd.isnull(data['nutrientes']):
        columns.append('nutrientes')
        values.append(data['nutrientes'])

    if not pd.isnull(data['categoria']):
        columns.append('categoria')
        values.append(str(data['categoria'].replace("[", "{").replace("]", "}")))

    if not pd.isnull(data['sector']):
        columns.append('sector')
        values.append(data['sector'])

    columns.append('bodega_id')
    values.append(data['bodega_id'])

    if not pd.isnull(data['estado']):
        columns.append('estado')
        values.append(data['estado'])

    if not pd.isnull(data['stock_minimo']):
        columns.append('stock_minimo')
        values.append(data['stock_minimo'])

    consult = f"{consult}{columns}"
    consult = consult.replace("[", "(").replace("]", ")")

    value = ['%s']
    while len(value) < len(columns):
        value.append('%s')

    values = f" values {value}"
    values = values.replace("[", "(").replace("]", ")")

    return consult + values

# Cliente
def create_query_update_client(data, values):
    consult = "UPDATE usuario SET"
    columns = ['nombre_usuario = %s']

    if not pd.isnull(data['apellido_usuario']):
        columns.append('apellido_usuario = %s')
        values.append(data['apellido_usuario'])

    columns.append('correo_usuario = %s')
    values.append(data['correo_usuario'])

    if not pd.isnull(data['telefono_usuario']):
        columns.append('telefono_usuario = %s')
        values.append(data['telefono_usuario'])

    if not pd.isnull(data['estado_usuario']):
        columns.append('estado_usuario = %s')
        values.append(data['estado_usuario'])

    columns.append('compania_id = %s')
    values.append(data['compania_id'])

    if not pd.isnull(data['password_usuario']):
        columns.append('password_usuario = %s')
        values.append(data['password_usuario'])

    if not pd.isnull(data['usuario_ref']):
        columns.append('usuario_ref = %s')
        values.append(data['usuario_ref'])

    consult = f"{consult}{columns}"
    consult = consult.replace("[", " ").replace("]", "")

    return consult + ' WHERE correo_usuario = %s'

def create_query_insert_client(data, values):
    consult = "INSERT INTO usuario"
    columns = ['nombre_usuario']

    if not pd.isnull(data['apellido_usuario']):
        columns.append('apellido_usuario = %s')
        values.append(data['apellido_usuario'])

    columns.append('correo_usuario = %s')
    values.append(data['correo_usuario'])

    if not pd.isnull(data['telefono_usuario']):
        columns.append('telefono_usuario = %s')
        values.append(data['telefono_usuario'])

    if not pd.isnull(data['estado_usuario']):
        columns.append('estado_usuario = %s')
        values.append(data['estado_usuario'])

    columns.append('compania_id = %s')
    values.append(data['compania_id'])

    if not pd.isnull(data['password_usuario']):
        columns.append('password_usuario = %s')
        values.append(data['password_usuario'])

    if not pd.isnull(data['usuario_ref']):
        columns.append('usuario_ref = %s')
        values.append(data['usuario_ref'])

    consult = f"{consult}{columns}"
    consult = consult.replace("[", "(").replace("]", ")")

    value = ['%s']
    while len(value) < len(columns):
        value.append('%s')

    values = f" values {value}"
    values = values.replace("[", "(").replace("]", ")")

    return consult + values

# Destinatario
def create_query_update_addressee(data, values):
    consult = "UPDATE destinatario SET"
    columns = ['compania_id = %s', 'destinatario_sap = %s', 'ciudad = %s']

    if not pd.isnull(data['departamento']):
        columns.append('departamento = %s')
        values.append(data['departamento'])

    if not pd.isnull(data['zip']):
        columns.append('zip = %s')
        values.append(data['zip'])

    if not pd.isnull(data['telefono_destinatario']):
        columns.append('telefono_destinatario = %s')
        values.append(data['telefono_destinatario'])

    if not pd.isnull(data['detalle']):
        columns.append('detalle = %s')
        values.append(data['detalle'])

    if not pd.isnull(data['punto']):
        columns.append('punto = %s')
        values.append(data['punto'])

    if not pd.isnull(data['estado_id']):
        columns.append('estado_id = %s')
        values.append(data['estado_id'])

    if not pd.isnull(data['contacto']):
        columns.append('contacto = %s')
        values.append(data['contacto'])

    if not pd.isnull(data['despacho']):
        columns.append('despacho = %s')
        values.append(data['despacho'])

    if not pd.isnull(data['facturacion']):
        columns.append('facturacion = %s')
        values.append(data['facturacion'])

    if not pd.isnull(data['nombre_destinatario']):
        columns.append('nombre_destinatario = %s')
        values.append(data['nombre_destinatario'])

    if not pd.isnull(data['apellido_destinatario']):
        columns.append('apellido_destinatario = %s')
        values.append(data['apellido_destinatario'])

    if not pd.isnull(data['envio']):
        columns.append('envio = %s')
        values.append(data['envio'])

    if not pd.isnull(data['nombre_referencia']):
        columns.append('nombre_referencia = %s')
        values.append(data['nombre_referencia'])

    consult = f"{consult}{columns}"
    consult = consult.replace("[", " ").replace("]", "")

    return consult + ' WHERE destinatario_sap = %s'

def create_query_insert_addressee(data, values):
    consult = "INSERT INTO destinatario"
    columns = ['compania_id', 'destinatario_sap', 'ciudad']

    if not pd.isnull(data['departamento']):
        columns.append('departamento')
        values.append(data['departamento'])

    if not pd.isnull(data['zip']):
        columns.append('zip')
        values.append(data['zip'])

    if not pd.isnull(data['telefono_destinatario']):
        columns.append('telefono_destinatario')
        values.append(data['telefono_destinatario'])

    if not pd.isnull(data['detalle']):
        columns.append('detalle')
        values.append(data['detalle'])

    if not pd.isnull(data['punto']):
        columns.append('punto')
        values.append(data['punto'])

    if not pd.isnull(data['estado_id']):
        columns.append('estado_id')
        values.append(data['estado_id'])

    if not pd.isnull(data['contacto']):
        columns.append('contacto')
        values.append(data['contacto'])

    if not pd.isnull(data['despacho']):
        columns.append('despacho')
        values.append(data['despacho'])

    if not pd.isnull(data['facturacion']):
        columns.append('facturacion')
        values.append(data['facturacion'])

    if not pd.isnull(data['nombre_destinatario']):
        columns.append('nombre_destinatario')
        values.append(data['nombre_destinatario'])

    if not pd.isnull(data['apellido_destinatario']):
        columns.append('apellido_destinatario')
        values.append(data['apellido_destinatario'])

    if not pd.isnull(data['envio']):
        columns.append('envio')
        values.append(data['envio'])

    if not pd.isnull(data['nombre_referencia']):
        columns.append('nombre_referencia')
        values.append(data['nombre_referencia'])

    consult = f"{consult}{columns}"
    consult = consult.replace("[", "(").replace("]", ")")

    value = ['%s']
    while len(value) < len(columns):
        value.append('%s')

    values = f" values {value}"
    values = values.replace("[", "(").replace("]", ")")

    return consult + values