import os
from datetime import datetime

import pandas as pd
from flask import Flask, Response, request, send_file

from database import connect_to_database
from queries_download import * #Importación de funciones para los queries de descarga
from queries_upload import * #Importación de funciones para los queries de carga

app = Flask(__name__)
connection = connect_to_database()

#Función definida para la descarga del archivo excel de la materia prima con o sin filtros
@app.route('/download/companias/',  methods=["GET"])
def download_companies():
    pais = request.args.get('pais')
    vendedor = request.args.get('vendedor')
    catalogo = request.args.get('catalogo')
    estado = request.args.get('estado')
    query = companies_download(pais, vendedor, catalogo, estado)

    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    # Convertir los resultados en un DataFrame de pandas y guardarlo en un arhivo de excel
    excel = save_results_to_excel(rows,'resultados_companias',cursor)

    cursor.close()
    return excel

#Función definida para la descarga del archivo excel de la materia prima con o sin filtros
@app.route('/download/materia/',  methods=["GET"])
def download_materia():
    pais = request.args.get('pais')
    bodega_sap = request.args.get('bodega_sap')
    categoria = request.args.get('categoria')
    urea = request.args.get('urea')
    estado = request.args.get('estado')
    sector = request.args.get('sector')
    query = raw_material_download(pais, bodega_sap, categoria, urea, estado, sector)

    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    # Convertir los resultados en un DataFrame de pandas y guardarlo en un arhivo de excel
    excel = save_results_to_excel(rows,'resultados_materia',cursor)

    cursor.close()
    return excel


#Función definida para la descarga del archivo excel de los clientes con o sin filtros
@app.route('/download/clientes/',  methods=["GET"])
def download_clients():
    compania_sap = request.args.get('compania_sap')
    pais = request.args.get('pais')
    estado = request.args.get('estado')
    query = clients_download(compania_sap, pais, estado)

    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    # Convertir los resultados en un DataFrame de pandas y guardarlo en un arhivo de excel
    excel = save_results_to_excel(rows,'resultados_clientes',cursor)

    cursor.close()
    return excel

#Función definida para la descarga del archivo excel de los destinatarios con o sin filtros
@app.route('/download/destinatario/',  methods=["GET"])
def download_addressee():
    compania_sap = request.args.get('compania_sap')
    pais = request.args.get('pais')
    vendedor = request.args.get('vendedor')
    estado = request.args.get('estado')
    query = addressee_download(compania_sap, pais, vendedor, estado)

    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    # Convertir los resultados en un DataFrame de pandas y guardarlo en un arhivo de excel
    excel = save_results_to_excel(rows,'resultados_destinatario',cursor)

    cursor.close()
    return excel

# Falta mapeo de datos para cada tabla, AUN NO FUNCIONA CORRECTAMENTE
# sintaxis en español pasar a ingles
@app.route('/upload/companias/', methods=["POST"])
def upload():
    excel_file = request.files['archivo']

    df = read_excel_file(excel_file)
    cursor = connection.cursor()

    compania_sap_list = bd_list_column("select compania_sap from compania")
    correo_vendedor_and_vendedor_id_dict = bd_list_two_columns("select correo_vendedor, vendedor_id from vendedor")
    abreviatura_and_pais_id_dict = bd_list_two_columns("select abreviatura, pais_id from pais")

    # Iterar sobre las filas del DataFrame
    for index, row in df.iterrows():
        correo_vendedor = row['correo_vendedor']
        if pd.isnull(correo_vendedor):
            return "No colocó al vendedor", 422

        # Verificar si el correo del vendedor ya existe en el diccionario si no lo inserta en la tabla vendedor
        if correo_vendedor not in correo_vendedor_and_vendedor_id_dict:
            cursor.execute("INSERT INTO vendedor (correo_vendedor) VALUES (%s)", (correo_vendedor,))
            connection.commit()
            # Actualizar el diccionario con el nuevo vendedor
            correo_vendedor_and_vendedor_id_dict = bd_list_two_columns("select correo_vendedor, vendedor_id from vendedor")

        vendedor_id = correo_vendedor_and_vendedor_id_dict[correo_vendedor] #varchar
        nombre_compania = row['nombre_compania']
        if pd.isnull(nombre_compania):
            return "No colocó el nombre de la compania", 422

        compania_sap = row['compania_sap']
        if pd.isnull(compania_sap):
            return "No colocó la compania sap", 422

        abreviatura = row['abreviatura']
        if pd.isnull(abreviatura):
            return 'No colocó la abreviatura del país', 422

        abreviatura = abreviatura.upper()
        if abreviatura not in abreviatura_and_pais_id_dict:
            cursor.execute("INSERT INTO pais (abreviatura) VALUES (%s)", (abreviatura,))
            connection.commit()
            # Actualizar el diccionario con el nuevo pais
            abreviatura_and_pais_id_dict = bd_list_two_columns("select abreviatura, pais_id from pais")

        pais_compania = abreviatura_and_pais_id_dict[abreviatura] #varchar

        telefono_compania = row['telefono_compania']
        if not pd.isnull(telefono_compania):
            telefono_compania = str(int(row['telefono_compania']))

        nit_compania = row['nit_compania']
        if not pd.isnull(nit_compania):
            nit_compania = str(int(row['nit_compania']))


        # Crear el diccionario de datos
        data = {
            'vendedor_id': vendedor_id,
            'compania_sap': str(int(row['compania_sap'])),
            'nombre_compania': nombre_compania,
            'negociacion': bool(row['negociacion']),
            'correo_compania': str(row['correo_compania']),
            'telefono_compania': telefono_compania, # El telefono lo guarda como un float para despues convertirlo en int y por último a string
            'nit_compania': nit_compania,
            'pais_compania': pais_compania,
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
        # Esto es temporal, debido a los datos de prueba se necesitaba esta correción
        while len(str(object=data.get('compania_sap'))) < 7: # Agrega los 0 al inicio que se pierden cuando se obtiene la compania_sap del excel
            data['compania_sap'] = '0' + data['compania_sap']

        values = [vendedor_id, data['compania_sap'], data['nombre_compania']]

        if data['compania_sap'] in compania_sap_list:
            # Ejecutar la consulta SQL para actualizar la base de data
            query = create_query_update_company(data, values)
            query = query.replace('\'','',query.count('\''))
            values.append(data['compania_sap'])
            cursor.execute(query, values)
            connection.commit()
        else:
            # Ejecutar la consulta SQL para insertar la base de data
            query = create_query_insert_company(data, values)
            query = query.replace('\'','',query.count('\''))
            cursor.execute(query, values)
            connection.commit()

    # Cerrar el cursor
    cursor.close()

    dir_validation(os.path.dirname(__file__) + '\\uploads_log\\')
    df.to_excel(os.path.dirname(__file__) + '\\uploads_log\\' + 'resultados_compania {}.xlsx'.format(datetime.now().strftime("%d-%m-%Y %H_%M_%S")), index=False)

    # Retornar una respuesta exitosa
    return "Base de datos actualizada correctamente", 200

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
    excel_file_path = os.path.join(os.path.dirname(__file__), 'downloads_log', f'{file_name} {datetime.now().strftime("%d-%m-%Y %H_%M_%S")}.xlsx')
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