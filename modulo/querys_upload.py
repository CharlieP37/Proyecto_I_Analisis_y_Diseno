def create_query_update_company(negociacion,correo_compania,telefono_compania,nit_compania,estado_compania,banco,centro,
                                informacion_legal,direccion_legal,metodo_pago,despacho,catalogo_id, canal, data, values):
    consulta = "UPDATE compania SET"
    columnas = ['vendedor_id = %s', 'nombre_compania = %s']

    if not negociacion:
        columnas.append('negociacion = %s')
        values.append(data['negociacion'])

    if not correo_compania:
        columnas.append('correo_compania = %s')
        values.append(data['correo_compania'])

    if not telefono_compania:
        columnas.append('telefono_compania = %s')
        values.append(data['telefono_compania'])

    if not nit_compania:
        columnas.append('nit_compania = %s')
        values.append(data['nit_compania'])

    columnas.append('pais_compania = %s')
    values.append(data['pais_compania'])

    if not estado_compania:
        columnas.append('estado_compania = %s')
        values.append(data['estado_compania'])

    if not banco:
        columnas.append('banco = %s')
        values.append(str(data['banco'].replace("[", "{").replace("]", "}")))

    if not centro:
        columnas.append('centro = %s')
        values.append(str(data['centro'].replace("[", "{").replace("]", "}")))

    if not informacion_legal:
        columnas.append('informacion_legal = %s')
        values.append(data['informacion_legal'])

    if not direccion_legal:
        columnas.append('direccion_legal = %s')
        values.append(data['direccion_legal'])

    if not metodo_pago:
        columnas.append('metodo_pago = %s')
        values.append(str(data['metodo_pago'].replace("[", "{").replace("]", "}")))

    if not despacho:
        columnas.append('despacho = %s')
        values.append(data['despacho'])

    if not catalogo_id:
        columnas.append('catalogo_id = %s')
        values.append(data['catalogo_id'])

    if not canal:
        columnas.append('canal = %s')
        values.append(str(data['canal'].replace("[", "{").replace("]", "}")))

    consulta = f"{consulta}{columnas}"
    consulta = consulta.replace("[", " ").replace("]", "")

    return consulta + ' WHERE compania_sap = %s'


def create_query_insert_company(negociacion,correo_compania,telefono_compania,nit_compania,estado_compania,banco,centro,
                                informacion_legal,direccion_legal,metodo_pago,despacho,catalogo_id, canal, data, values):
    consulta = "INSERT INTO compania"
    columnas = ['vendedor_id', 'compania_sap', 'nombre_compania']

    if not negociacion:
        columnas.append('negociacion')
        values.append(data['negociacion'])

    if not correo_compania:
        columnas.append('correo_compania')
        values.append(data['correo_compania'])

    if not telefono_compania:
        columnas.append('telefono_compania')
        values.append(data['telefono_compania'])

    if not nit_compania:
        columnas.append('nit_compania')
        values.append(data['nit_compania'])

    columnas.append('pais_compania')
    values.append(data['pais_compania'])

    if not estado_compania:
        columnas.append('estado_compania')
        values.append(data['estado_compania'])

    if not banco:
        columnas.append('banco')
        values.append(str(data['banco'].replace("[", "{").replace("]", "}")))

    if not centro:
        columnas.append('centro')
        values.append(str(data['centro'].replace("[", "{").replace("]", "}")))

    if not informacion_legal:
        columnas.append('informacion_legal')
        values.append(data['informacion_legal'])

    if not direccion_legal:
        columnas.append('direccion_legal')
        values.append(data['direccion_legal'])

    if not metodo_pago:
        columnas.append('metodo_pago')
        values.append(str(data['metodo_pago'].replace("[", "{").replace("]", "}")))

    if not despacho:
        columnas.append('despacho')
        values.append(data['despacho'])

    if not catalogo_id:
        columnas.append('catalogo_id')
        values.append(data['catalogo_id'])

    if not canal:
        columnas.append('canal')
        values.append(str(data['canal'].replace("[", "{").replace("]", "}")))

    consulta = f"{consulta}{columnas}"
    consulta = consulta.replace("[", "(").replace("]", ")")

    value = ['%s']
    while len(value) < len(columnas):
        value.append('%s')

    values = f" values {value}"
    values = values.replace("[", "(").replace("]", ")")

    return consulta + values