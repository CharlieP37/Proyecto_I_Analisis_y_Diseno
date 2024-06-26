import os
from datetime import datetime

import pandas as pd
from flask import Flask, Response, request, send_file

from database import connect_to_database
from queries_download import *
from queries_upload import *

app = Flask(__name__)
connection = connect_to_database()

@app.route('/download/companias/',  methods=["GET", "POST"])
#Función definida para la descarga del archivo excel de la materia prima con o sin filtros
def download_companies():

    pais = request.values.get('pais')
    vendedor = request.values.get('vendedor')
    catalogo = request.values.get('catalogo')
    estado = request.values.get('estado')
    query = companies_download(pais, vendedor, catalogo, estado)

    if pais is not None:
        if len(pais) > 5:
            return "El campo PAÍS es inválido", 422

    if estado is not None:
        try:
            int(estado)
            if int(estado) != 0 and int(estado) != 1:
                return "El estado solo puede ser activo o inactivo", 422
        except:
            return "El estado no es un valor numérico", 422

    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    # Convertir los resultados en un DataFrame de pandas y guardarlo en un arhivo de excel
    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
    dir_validation(os.path.dirname(__file__) + '\\downloads_log\\')
    ruta_excel = os.path.dirname(__file__) + '\\downloads_log\\' + 'resultados_companias {}.xlsx'.format(datetime.now().strftime("%d-%m-%Y %H_%M_%S"))
    df.to_excel(ruta_excel, index=False)

    cursor.close()
    return send_file(ruta_excel, as_attachment=True, download_name='resultados_companias.xlsx')

@app.route('/download/materia/',  methods=["GET", "POST"])
#Función definida para la descarga del archivo excel de la materia prima con o sin filtros
def download_raw_material():
    pais = request.values.get('pais')
    bodega_sap = request.values.get('bodega_sap')
    categoria = request.values.get('categoria')
    urea = request.values.get('urea')
    estado = request.values.get('estado')
    sector = request.values.get('sector')
    query = raw_material_download(pais, bodega_sap, categoria, urea, estado, sector)

    if pais is not None:
        if len(pais) > 5:
            return "El campo PAÍS es inválido", 422

    if urea is not None:
        try:
            int(urea)
            if int(urea) != 0 and int(urea) != 1:
                return "Urea solo puede ser verdadero o falso", 422
        except:
            return "Urea no es un valor numérico", 422

    if estado is not None:
        try:
            int(estado)
            if int(estado) != 0 and int(estado) != 1:
                return "El estado solo puede ser activo o inactivo", 422
        except:
            return "El estado no es un valor numérico", 422

    if sector is not None:
        if len(sector) > 4:
            return "El campo SECTOR es inválido", 422

    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    # Convertir los resultados en un DataFrame de pandas y guardarlo en un arhivo de excel
    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
    dir_validation(os.path.dirname(__file__) + '\\downloads_log\\')
    ruta_excel = os.path.dirname(__file__) + '\\downloads_log\\' + 'resultados_materia {}.xlsx'.format(datetime.now().strftime("%d-%m-%Y %H_%M_%S"))
    df.to_excel(ruta_excel, index=False)

    cursor.close()
    return send_file(ruta_excel, as_attachment=True, download_name='resultados_materia.xlsx')


@app.route('/download/clientes/',  methods=["GET", "POST"])
#Función definida para la descarga del archivo excel de los clientes con o sin filtros
def download_clients():
    compania_sap = request.values.get('compania_sap')
    pais = request.values.get('pais')
    estado = request.values.get('estado')
    query = clients_download(compania_sap, pais, estado)

    if pais is not None:
        if len(pais) > 5:
            return "El campo PAÍS es inválido", 422

    if estado is not None:
        try:
            int(estado)
            if int(estado) != 0 and int(estado) != 1:
                return "El estado solo puede ser activo o inactivo", 422
        except:
            return "El estado no es un valor numérico", 422

    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    # Convertir los resultados en un DataFrame de pandas y guardarlo en un arhivo de excel
    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
    dir_validation(os.path.dirname(__file__) + '\\downloads_log\\')
    ruta_excel = os.path.dirname(__file__) + '\\downloads_log\\' + 'resultados_clientes {}.xlsx'.format(datetime.now().strftime("%d-%m-%Y %H_%M_%S"))
    df.to_excel(ruta_excel, index=False)

    cursor.close()
    return send_file(ruta_excel, as_attachment=True, download_name='resultados_clientes.xlsx')

@app.route('/download/destinatario/',  methods=["GET", "POST"])
#Función definida para la descarga del archivo excel de los destinatarios con o sin filtros
def download_addressee():
    compania_sap = request.values.get('compania_sap')
    pais = request.values.get('pais')
    vendedor = request.values.get('vendedor')
    estado = request.values.get('estado')
    query = addressee_download(compania_sap, pais, vendedor, estado)

    if pais is not None:
        if len(pais) > 5:
            return "El campo PAÍS es inválido", 422

    if estado is not None:
        try:
            int(estado)
            if int(estado) != 0 and int(estado) != 1:
                return "El estado solo puede ser activo o inactivo", 422
        except:
            return "El estado no es un valor numérico", 422

    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    # Convertir los resultados en un DataFrame de pandas y guardarlo en un arhivo de excel
    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
    dir_validation(os.path.dirname(__file__) + '\\downloads_log\\')
    ruta_excel = os.path.dirname(__file__) + '\\downloads_log\\' + 'resultados_destinatario {}.xlsx'.format(datetime.now().strftime("%d-%m-%Y %H_%M_%S"))
    df.to_excel(ruta_excel, index=False)

    cursor.close()
    return send_file(ruta_excel, as_attachment=True, download_name='resultados_destinatario.xlsx')

@app.route('/upload/companias/', methods=["POST"])
def upload_companies():
    excel_file = request.files['archivo']

    df = read_excel_file(excel_file)
    cursor = connection.cursor()

    # Obtener los datos necesarios para las validaciones
    compania_sap_list = bd_list_column("select compania_sap from compania")
    correo_vendedor_and_vendedor_id_dict = bd_list_two_columns("select correo_vendedor, vendedor_id from vendedor")
    abreviatura_and_pais_id_dict = bd_list_two_columns("select abreviatura, pais_id from pais")

    # Comprobar si df es del tipo correcto
    if not isinstance(df, pd.DataFrame):
        return "DataFrame no válido", 400

    # Crear una lista para almacenar los datos que no se pudieron insertar en la base de datos
    data_error = []

    for index, row in df.iterrows():

        try:
            # Crear el diccionario de datos
            data = {
                'vendedor_id': row['correo_vendedor'],
                'compania_sap': row['compania_sap'],
                'nombre_compania': row['nombre_compania'],
                'negociacion': bool(row['negociacion']),
                'correo_compania': row['correo_compania'],
                'telefono_compania': row['telefono_compania'],
                'nit_compania': row['nit_compania'],
                'pais_compania': row['abreviatura'],
                'estado_compania': row['estado_compania'],
                'banco': row['banco'],
                'centro': row['centro'],
                'informacion_legal': row['informacion_legal'],
                'direccion_legal': row['direccion_legal'],
                'metodo_pago': row['metodo_pago'],
                'despacho': row['despacho'],
                'catalogo_id': row['catalogo_id'],
                'canal': row['canal']
            }

            correo_vendedor = data['vendedor_id']
            if pd.isnull(correo_vendedor):
                raise Exception("No colocó al vendedor", 422)

            nombre_compania = data['nombre_compania']
            if pd.isnull(nombre_compania):
                raise Exception("No colocó el nombre de la compania", 422)

            abreviatura = data['pais_compania']
            if pd.isnull(abreviatura):
                raise Exception("No colocó la abreviatura del país", 422)

            compania_sap = data['compania_sap']
            if pd.isnull(compania_sap):
                raise Exception("No colocó la compania sap", 422)
            data['compania_sap'] = str(int(compania_sap))

            # Verificar si el correo del vendedor ya existe en el diccionario si no lo inserta en la tabla vendedor
            if correo_vendedor not in correo_vendedor_and_vendedor_id_dict:
                cursor.execute("INSERT INTO vendedor (correo_vendedor) VALUES (%s)", (correo_vendedor,))
                connection.commit()
                # Actualizar el diccionario con el nuevo vendedor
                correo_vendedor_and_vendedor_id_dict = bd_list_two_columns("select correo_vendedor, vendedor_id from vendedor")
            # Reemplazar el correo del vendedor por el vendedor_id
            data['vendedor_id'] = correo_vendedor_and_vendedor_id_dict[correo_vendedor]

            telefono_compania = data['telefono_compania']
            if not pd.isnull(telefono_compania):
                telefono_compania = str(int(row['telefono_compania'])) #telefono_compania, # El telefono lo guarda como un float para despues convertirlo en int y por último a string

            abreviatura = abreviatura.upper()
            if abreviatura not in abreviatura_and_pais_id_dict:
                raise Exception("El país no existe", 422)
            # Reemplazar la abreviatura por el pais_id
            data['pais_compania'] = abreviatura_and_pais_id_dict[abreviatura]

            nit_compania = data['nit_compania']
            if not pd.isnull(nit_compania):
                nit_compania = str(int(row['nit_compania']))

            # Esto es temporal, debido a los datos de prueba se necesitaba esta correción
            while len(str(object=data.get('compania_sap'))) < 7: # Agrega los 0 al inicio que se pierden cuando se obtiene la compania_sap del excel. Ejemplo: 0000001
                data['compania_sap'] = '0' + data['compania_sap']

            # Crear una lista con los valores de los datos
            values = [data['vendedor_id'], data['compania_sap'], data['nombre_compania']]

            # Verificar si la compania sap ya existe en la base de datos, si no la inserta en la tabla compania
            if data['compania_sap'] in compania_sap_list:
                # Crea la consulta SQL para actualizar la base de data
                query = create_query_update_company(data, values)
                # Quita las comillas simples, para evitar errores en la consulta SQL
                query = query.replace('\'','',query.count('\''))
                # Se agrega al final ya que este valor es la condición con los que se van a actualizar. En la consutla se ve asi: WHERE compania_sap = data['compania_sap']
                values.append(data['compania_sap'])
                cursor.execute(query, values)
                connection.commit()
            else:
                # Crea la consulta SQL para insertar la base de data
                query = create_query_insert_company(data, values)
                # Quita las comillas simples, para evitar errores en la consulta SQL
                query = query.replace('\'','',query.count('\''))
                cursor.execute(query, values)
                connection.commit()

        except Exception as e:
            # Si hay un error, se agrega el diccionario de datos a la lista de errores
            data_error.append(data)
            connection.rollback()

    # Cerrar el cursor
    cursor.close()

    # Crear un directorio para guardar los archivos de excel
    dir_validation(os.path.dirname(__file__) + '\\uploads_log\\')

    # Guardar el archivo de excel con los resultados
    upload_save_results_to_excel('resultados_compania', df)

    # Si hay errores, se crea un archivo de excel con los datos que no se pudieron insertar
    if len(data_error) >= 1:
        df_error = pd.DataFrame(data_error)

        # Cambiar el nombre de las columnas para que coincidan con el archivo de excel, ya que se cambió el nombre de las columnas en el diccionario de datos, pero no en el archivo de excel
        df_error.rename(columns={'vendedor_id': 'correo_vendedor','pais_compania': 'abreviatura'}, inplace=True)

        # Guardar el archivo de excel con los datos que no se pudieron insertar
        excel = upload_save_results_to_excel('registros_fallidos-resultados_compania', df_error)
        return excel

    # Retornar una respuesta exitosa
    return "Base de datos actualizada correctamente", 200

@app.route('/upload/materia/', methods=["POST"])
def upload_raw_material():
    excel_file = request.files['archivo']

    df = read_excel_file(excel_file)
    cursor = connection.cursor()

    # Obtener los datos necesarios para las validaciones
    codigo_list = bd_list_column("select codigo from materia_prima")
    bodega_sap_and_bodega_id_dict = bd_list_two_columns("select bodega_sap, bodega_id from bodega")
    abreviatura_and_pais_id_dict = bd_list_two_columns("select abreviatura, pais_id from pais")

    # Comprobar si df es del tipo correcto
    if not isinstance(df, pd.DataFrame):
        return "DataFrame no válido", 400

    # Crear una lista para almacenar los datos que no se pudieron insertar en la base de datos
    data_error = []

    for index, row in df.iterrows():
        try:
            data = {
                'nombre': row['nombre'],
                'codigo': row['codigo'],
                'es_urea': bool(row['es_urea']),
                'nutrientes': row['nutrientes'],
                'categoria': row['categoria'],
                'sector': row['sector'],
                'bodega_id': row['bodega_sap'],
                'estado': row['estado'],
                'stock_minimo': float(row['stock_minimo']),
                'abreviatura': row['abreviatura']
            }

            nombre = data['nombre']
            if pd.isnull(nombre):
                raise Exception("No colocó el nombre de la materia prima", 422)

            codigo = data['codigo']
            if pd.isnull(codigo):
                print(codigo)
                raise Exception("No colocó el código de la materia prima", 422)
            data['codigo'] = int(codigo)

            abreviatura = data['abreviatura']
            if pd.isnull(abreviatura):
                raise Exception('No colocó la abreviatura del país', 422)

            abreviatura = abreviatura.upper()
            if abreviatura not in abreviatura_and_pais_id_dict:
                raise Exception("El país no existe", 422)

            bodega_sap = data['bodega_id']
            if pd.isnull(bodega_sap):
                raise Exception("No colocó la bodega sap", 422)

            # Verificar si la bodega sap ya existe en el diccionario si no la inserta en la tabla bodega, junto con el pais_id
            if bodega_sap not in bodega_sap_and_bodega_id_dict:
                cursor.execute("INSERT INTO bodega (pais_bodega, bodega_sap) VALUES (%s, %s)", (abreviatura_and_pais_id_dict[abreviatura], bodega_sap,))
                connection.commit()
                # Actualizar el diccionario con la nueva bodega
                bodega_sap_and_bodega_id_dict = bd_list_two_columns("select bodega_sap, bodega_id from bodega")
            # Reemplazar la bodega_sap por la bodega_id
            data['bodega_id'] = bodega_sap_and_bodega_id_dict[bodega_sap]

            # Crear una lista con los valores de los datos
            values = [data['nombre'], data['codigo']]

            # Verificar si el codigo de la materia prima ya existe en la base de datos, si no la inserta en la tabla materia_prima
            if data['codigo'] in codigo_list:
                # Crea la consulta SQL para actualizar la base de data
                query = create_query_update_raw_material(data, values)
                # Quita las comillas simples, para evitar errores en la consulta SQL
                query = query.replace('\'','',query.count('\''))
                # Se agrega al final ya que este valor es la condición con los que se van a actualizar. En la consutla se ve asi: WHERE codigo = data['codigo']
                values.append(str(data['codigo']))
                cursor.execute(query, values)
                connection.commit()
            else:
                # Crea la consulta SQL para insertar la base de data
                query = create_query_insert_raw_material(data, values)
                # Quita las comillas simples, para evitar errores en la consulta SQL
                query = query.replace('\'','',query.count('\''))
                cursor.execute(query, values)
                connection.commit()

        except Exception as e:
            data_error.append(data)
            connection.rollback()

    # Cerrar el cursor
    cursor.close()

    # Crear un directorio para guardar los archivos de excel
    dir_validation(os.path.dirname(__file__) + '\\uploads_log\\')

    # Guardar el archivo de excel con los resultados
    upload_save_results_to_excel('resultados_materia_prima', df)

    # Si hay errores, se crea un archivo de excel con los datos que no se pudieron insertar
    if len(data_error) >= 1:
        df_error = pd.DataFrame(data_error)
        # Cambiar el nombre de las columnas para que coincidan con el archivo de excel, ya que se cambió el nombre de las columnas en el diccionario de datos, pero no en el archivo de excel
        df_error.rename(columns={'bodega_id': 'bodega_sap'}, inplace=True)
        excel = upload_save_results_to_excel('registros_fallidos-resultados_materia_prima', df_error)
        return excel

    return "Base de datos actualizada correctamente", 200

@app.route('/upload/clientes/', methods=["POST"])
def upload_clients():
    excel_file = request.files['archivo']

    df = read_excel_file(excel_file)
    cursor = connection.cursor()

    # Obtener los datos necesarios para las validaciones
    correo_usuario_list = bd_list_column("select correo_usuario from usuario")
    abreviatura_and_pais_id_dict = bd_list_two_columns("select abreviatura, pais_id from pais")
    compania_sap_and_compania_id_dict = bd_list_two_columns("select compania_sap, compania_id from compania")

    # Comprobar si df es del tipo correcto
    if not isinstance(df, pd.DataFrame):
        return "DataFrame no válido", 400

    # Crear una lista para almacenar los datos que no se pudieron insertar en la base de datos
    data_error = []

    for index, row in df.iterrows():
        try:
            data = {
                'nombre_usuario': row['nombre_usuario'],
                'apellido_usuario': row['apellido_usuario'],
                'correo_usuario': row['correo_usuario'],
                'telefono_usuario': row['telefono_usuario'],
                'estado_usuario': row['estado_usuario'],
                'compania_id': row['compania_sap'],
                'password_usuario': row['password_usuario'],
                'usuario_ref': row['usuario_ref'],
                'abreviatura': row['abreviatura']
            }

            if pd.isnull(data['nombre_usuario']) or pd.isnull(data['correo_usuario']) or pd.isnull(data['compania_id'] or pd.isnull(data['abreviatura'])):
                raise Exception("Los campos nombre_usario, correo_usuario, compañía_sap y abreviatura no pueden venir vacíos", 422)

            compania_sap = str(data['compania_id'])
            if compania_sap not in compania_sap_and_compania_id_dict:
                raise Exception("La compañía_sap no existe", 422)
            data['compania_id'] = compania_sap_and_compania_id_dict[compania_sap]

            if data['abreviatura'].upper() not in abreviatura_and_pais_id_dict:
                raise Exception("El país no existe", 422)

            # Crear una lista con los valores de los datos
            values = [data['nombre_usuario']]

            # Verificar si el correo del usuario ya existe en la base de datos, si no lo inserta en la tabla usuario
            if data['correo_usuario'] in correo_usuario_list:
                # Crea la consulta SQL para actualizar la base de data
                query = create_query_update_client(data, values)
                # Quita las comillas simples, para evitar errores en la consulta SQL
                query = query.replace('\'','',query.count('\''))
                # Se agrega al final ya que este valor es la condición con los que se van a actualizar. En la consutla se ve asi: WHERE correo_usuario = data['correo_usuario']
                values.append(data['correo_usuario'])
                cursor.execute(query, values)
                connection.commit()
            else:
                # Crea la consulta SQL para insertar la base de data
                query = create_query_insert_client(data, values)
                # Quita las comillas simples, para evitar errores en la consulta SQL
                query = query.replace('\'','',query.count('\''))
                cursor.execute(query, values)
                connection.commit()

        except Exception as e:
            data_error.append(data)
            connection.rollback()

    # Cerrar el cursor
    cursor.close()

    # Crear un directorio para guardar los archivos de excel
    dir_validation(os.path.dirname(__file__) + '\\uploads_log\\')

    # Guardar el archivo de excel con los resultados
    upload_save_results_to_excel('resultados_clientes', df)

    # Si hay errores, se crea un archivo de excel con los datos que no se pudieron insertar
    if len(data_error) >= 1:
        df_error = pd.DataFrame(data_error)
        # Cambiar el nombre de las columnas para que coincidan con el archivo de excel, ya que se cambió el nombre de las columnas en el diccionario de datos, pero no en el archivo de excel
        df_error.rename(columns={'compania_id': 'compania_sap'}, inplace=True)
        # Guardar el archivo de excel con los datos que no se pudieron insertar
        excel = upload_save_results_to_excel('registros_fallidos-resultados_clientes', df_error)
        return excel

    return "Base de datos actualizada correctamente", 200

@app.route('/upload/destinatario/', methods=["POST"])
def upload_addressee():
    excel_file = request.files['archivo']

    df = read_excel_file(excel_file)
    cursor = connection.cursor()

    compania_sap_and_compania_id_dict = bd_list_two_columns("select compania_sap, compania_id from compania")
    destinatario_sap_list = bd_list_column("select destinatario_sap from destinatario")

    # Comprobar si df es del tipo correcto
    if not isinstance(df, pd.DataFrame):
        return "DataFrame no válido", 400

    data_error = []

    for index, row in df.iterrows():
        try:
            data = {
                'compania_id': row['compania_sap'],
                'destinatario_sap': row['destinatario_sap'],
                'ciudad': row['ciudad'],
                'departamento': row['departamento'],
                'zip': row['zip'],
                'telefono_destinatario': row['telefono_destinatario'],
                'detalle': row['detalle'],
                'punto': row['punto'],
                'estado_id': row['estado_id'],
                'contacto': row['contacto'],
                'despacho': row['despacho'],
                'facturacion': bool(row['facturacion']),
                'nombre_destinatario': row['nombre_destinatario'],
                'apellido_destinatario': row['apellido_destinatario'],
                'envio': bool(row['envio']),
                'nombre_referencia': row['nombre_referencia'],
            }

            if pd.isnull(data['compania_id']) or pd.isnull(data['destinatario_sap']) or pd.isnull(data['ciudad']):
                raise Exception("Los campos compania_id, destinatario_sap, ciudad no pueden venir vacíos", 422)

            compania_sap = str(data['compania_id'])
            if compania_sap not in compania_sap_and_compania_id_dict:
                raise Exception("La compañía_sap no existe", 422)
            # Reemplazar la compania_sap por la compania_id
            data['compania_id'] = compania_sap_and_compania_id_dict[compania_sap]

            # Crear una lista con los valores de los datos
            values = [data['compania_id'], data['destinatario_sap'], data['ciudad']]

            # Verificar si el destinatario sap ya existe en la base de datos, si no lo inserta en la tabla destinatario
            if data['destinatario_sap'] in destinatario_sap_list:
                # Crea la consulta SQL para actualizar la base de data
                query = create_query_update_addressee(data, values)
                # Quita las comillas simples, para evitar errores en la consulta SQL
                query = query.replace('\'','',query.count('\''))
                # Se agrega al final ya que este valor es la condición con los que se van a actualizar. En la consutla se ve asi: WHERE destinatario_sap = data['destinatario_sap']
                values.append(data['destinatario_sap'])
                cursor.execute(query, values)
                connection.commit()
            else:
                # Crea la consulta SQL para insertar la base de data
                query = create_query_insert_addressee(data, values)
                # Quita las comillas simples, para evitar errores en la consulta SQL
                query = query.replace('\'','',query.count('\''))
                cursor.execute(query, values)
                connection.commit()

        except Exception as e:
            data_error.append(data)
            connection.rollback()

    # Cerrar el cursor
    cursor.close()

    # Crear un directorio para guardar los archivos de excel
    dir_validation(os.path.dirname(__file__) + '\\uploads_log\\')

    # Guardar el archivo de excel con los resultados
    upload_save_results_to_excel('resultados_destinatario', df)
    # Si hay errores, se crea un archivo de excel con los datos que no se pudieron insertar
    if len(data_error) >= 1:
        df_error = pd.DataFrame(data_error)
        # Cambiar el nombre de las columnas para que coincidan con el archivo de excel, ya que se cambió el nombre de las columnas en el diccionario de datos, pero no en el archivo de excel
        df_error.rename(columns={'compania_id': 'compania_sap'}, inplace=True)
        # Guardar el archivo de excel con los datos que no se pudieron insertar
        excel = upload_save_results_to_excel('registros_fallidos-resultados_destinatario', df_error)
        return excel

    return "Base de datos actualizada correctamente", 200


def upload_save_results_to_excel(file_name, df):
    excel_file_path = os.path.dirname(__file__) + '\\uploads_log\\' + ' {}.xlsx'.format(datetime.now().strftime("%d-%m-%Y %H_%M_%S") + ' ' + file_name)
    df.to_excel(excel_file_path, index=False)
    return send_file(excel_file_path, as_attachment=True, download_name=f'{file_name}.xlsx')

def bd_list_column(query):
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    list_identifiers = []
    for row in rows:
        list_identifiers.append(row[0])
    return list_identifiers

def bd_list_two_columns(query):
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    dict_identifiers = {}
    for row in rows:
        dict_identifiers[row[0]] = row[1]
    return dict_identifiers

def dir_validation(path: str):
    if not os.path.exists(path):
        os.mkdir(path)

def save_results_to_excel(rows: list, file_name: str, cursor) -> Response:
    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
    dir_validation(os.path.join(os.path.dirname(__file__), 'downloads_log'))
    excel_file_path = os.path.join(os.path.dirname(__file__), 'downloads_log', f'{datetime.now().strftime("%d-%m-%Y %H_%M_%S")} {file_name}.xlsx')
    df.to_excel(excel_file_path, index=False)
    return send_file(excel_file_path, as_attachment=True, download_name=f'{file_name}.xlsx')

def read_excel_file(excel_file):
    # Validar tipo archivo y manejo de error en la lectura (Información sobre el error "e")
    if not excel_file.filename.endswith('.xlsx'):
        return "Se esperaba un archivo Excel (.xlsx).", 400
    try:
        return pd.read_excel(excel_file)
    except Exception as e:
        return f"Error al leer el archivo Excel: {str(e)}", 500