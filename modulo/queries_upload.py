import pandas as pd

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

