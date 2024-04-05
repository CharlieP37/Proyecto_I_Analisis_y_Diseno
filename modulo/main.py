from ast import Not
from asyncio.windows_events import NULL
from datetime import datetime
from errno import ESTALE
from msilib import PID_REVNUMBER
import os
from xml.sax.handler import property_interning_dict
from numpy import DataSource
import pandas as pd
import openpyxl as op
import re
from flask import Flask, request, send_file

import io
from database import connect_to_database
from querys_download import * #Importación de funciones para los querys de descarga
from querys_upload import *

def BD_list_column(query):
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    list_identifiers = []
    for row in rows:
        list_identifiers.append(row[0])
    return list_identifiers

def BD_list_two_columns(query):
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

app = Flask(__name__)
connection = connect_to_database()

@app.route('/download/companias/',  methods=["GET"])
#Función definida para la descarga del archivo excel de la materia prima con o sin filtros
def dowload_companias():

    pais = request.args.get('pais')
    vendedor = request.args.get('vendedor')
    catalogo = request.args.get('catalogo')
    estado = request.args.get('estado')
    query = companies_download(pais, vendedor, catalogo, estado)

    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    # Convertir los resultados en un DataFrame de pandas y guardarlo en un arhivo de excel
    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
    dir_validation(os.path.dirname(__file__) + '\\downloadslog\\')
    ruta_excel = os.path.dirname(__file__) + '\\downloadslog\\' + 'resultados_companias {}.xlsx'.format(datetime.now().strftime("%d-%m-%Y %H_%M_%S"))
    df.to_excel(ruta_excel, index=False)

    cursor.close()
    return send_file(ruta_excel, as_attachment=True, download_name='resultados_companias.xlsx')

@app.route('/download/materia/',  methods=["GET"])
#Función definida para la descarga del archivo excel de la materia prima con o sin filtros
def download_materia():
    pais = request.args.get('pais')
    bodega_sap = request.args.get('bodega_sap')
    categoria = request.args.get('categoria')
    urea = request.args.get('urea')
    estado = request.args.get('estado')
    sector = request.args.get('sector')
    query = rawmaterial_download(pais, bodega_sap, categoria, urea, estado, sector)

    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    # Convertir los resultados en un DataFrame de pandas y guardarlo en un arhivo de excel
    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
    dir_validation(os.path.dirname(__file__) + '\\downloadslog\\')
    ruta_excel = os.path.dirname(__file__) + '\\downloadslog\\' + 'resultados_materia {}.xlsx'.format(datetime.now().strftime("%d-%m-%Y %H_%M_%S"))
    df.to_excel(ruta_excel, index=False)

    cursor.close()
    return send_file(ruta_excel, as_attachment=True, download_name='resultados_materia.xlsx')


@app.route('/download/clientes/',  methods=["GET"])
#Función definida para la descarga del archivo excel de los clientes con o sin filtros
def dowload_clientes():
    compania_sap = request.args.get('compania_sap')
    pais = request.args.get('pais')
    estado = request.args.get('estado')
    query = clients_download(compania_sap, pais, estado)

    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    # Convertir los resultados en un DataFrame de pandas y guardarlo en un arhivo de excel
    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
    dir_validation(os.path.dirname(__file__) + '\\downloadslog\\')
    ruta_excel = os.path.dirname(__file__) + '\\downloadslog\\' + 'resultados_clientes {}.xlsx'.format(datetime.now().strftime("%d-%m-%Y %H_%M_%S"))
    df.to_excel(ruta_excel, index=False)

    cursor.close()
    return send_file(ruta_excel, as_attachment=True, download_name='resultados_clientes.xlsx')

@app.route('/download/destinatario/',  methods=["GET"])
#Función definida para la descarga del archivo excel de los destinatarios con o sin filtros
def dowload_destinatario():
    compania_sap = request.args.get('compania_sap')
    pais = request.args.get('pais')
    vendedor = request.args.get('vendedor')
    estado = request.args.get('estado')
    query = addressee_download(compania_sap, pais, vendedor, estado)

    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    # Convertir los resultados en un DataFrame de pandas y guardarlo en un arhivo de excel
    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
    dir_validation(os.path.dirname(__file__) + '\\downloadslog\\')
    ruta_excel = os.path.dirname(__file__) + '\\downloadslog\\' + 'resultados_destinatario {}.xlsx'.format(datetime.now().strftime("%d-%m-%Y %H_%M_%S"))
    df.to_excel(ruta_excel, index=False)

    cursor.close()
    return send_file(ruta_excel, as_attachment=True, download_name='resultados_destinatario.xlsx')

# Falta mapeo de datos para cada tabla, AUN NO FUNCIONA CORRECTAMENTE
@app.route('/upload/companias/', methods=["POST"])
def upload():
    excel_file = request.files['archivo']

    # Validar tipo archivo y manejo de error en la lectura (Información sobre el error "e")
    if not excel_file.filename.endswith('.xlsx'):
        return "Se esperaba un archivo Excel (.xlsx).", 400

    try:
        df = pd.read_excel(excel_file)
    except Exception as e:
        return f"Error al leer el archivo Excel: {str(e)}", 400

    # Validacion de data por column
    expected_types = {'vendedor_id': int, 'compania_sap': str, 'nombre_compania': str, 'correo_compania': str, 'telefono_compania': str, 'nit_compania': str, 'pais_compania': int}
    for column, expected_type in expected_types.items():
        if column == 'vendedor_id':
            for value in df[column]:
                try:
                    value_int = int(value)
                    if value_int < 0:
                        return f"La columna '{column}' no puede contener valores negativos.", 400
                except ValueError:
                    return f"La columna '{column}' debe contener valores numéricos enteros.", 400

    df = pd.read_excel(excel_file)
    cursor = connection.cursor()

    company_list_sap = BD_list_column("select compania_sap from compania")

    # Iterar sobre las filas del DataFrame
    for index, row in df.iterrows():
        # Obtener los valores de las columns para la fila actual
        vendedor_id = row['vendedor_id'] #integer
        compania_sap = str(row['compania_sap']) #varchar - pero lo toma como int
        nombre_compania = row['nombre_compania'] #varchar
        pais_compania = row['pais_compania'] # integer

        negociacion = row['negociacion'] # boleano
        correo_compania = row['correo_compania'] #varchar
        telefono_compania = row['telefono_compania'] #varchar
        nit_compania = row['nit_compania'] #varchar
        estado_compania = row['estado_compania'] # integer
        banco = row['banco'] #varchar
        centro = row['centro'] #varchar
        informacion_legal = row['informacion_legal'] #json
        direccion_legal = row['direccion_legal'] #json
        metodo_pago = row['metodo_pago'] #varchar
        despacho = row['despacho'] #json
        catalogo_id = row['catalogo_id'] #varchar
        canal = row['canal'] #varchar

        # Esto es temporal, debido a los datos de prueba se necesitaba esta correción
        while len(str(compania_sap)) < 7: # Agrega los 0 al inicio que se pierden cuando se obtiene la compania_sap del excel
            compania_sap = '0' + compania_sap

        data = {
                'vendedor_id':vendedor_id,
                'compania_sap':compania_sap,
                'nombre_compania':nombre_compania,
                'negociacion':bool(negociacion),
                'correo_compania':str(correo_compania),
                'telefono_compania':str(telefono_compania),
                'nit_compania':str(nit_compania),
                'pais_compania':pais_compania,
                'estado_compania':estado_compania,
                'banco':banco,
                'centro':centro,
                'informacion_legal':informacion_legal,#json
                'direccion_legal':direccion_legal,#json
                'metodo_pago':metodo_pago,
                'despacho':despacho,#json
                'catalogo_id':str(catalogo_id),
                'canal':canal
                }


        if compania_sap in company_list_sap:
            # Ejecutar la consulta SQL para actualizar la base de data
            values = [vendedor_id,nombre_compania]
            consult = create_query_update_company(pd.isnull(row['negociacion']),
                                pd.isnull(row['correo_compania']),
                                pd.isnull(row['telefono_compania']),
                                pd.isnull(row['nit_compania']),
                                pd.isnull(row['estado_compania']),
                                pd.isnull(row['banco']),
                                pd.isnull(row['centro']),
                                pd.isnull(row['informacion_legal']),
                                pd.isnull(row['direccion_legal']),
                                pd.isnull(row['metodo_pago']),
                                pd.isnull(row['despacho']),
                                pd.isnull(row['catalogo_id']),
                                pd.isnull(row['canal']),
                                data,
                                values)

            consult = consult.replace('\'','',consult.count('\''))
            values.append(compania_sap)
            cursor.execute(consult, values)
            connection.commit()

        else:
            values = [vendedor_id, compania_sap, nombre_compania]

            consult = create_query_insert_company(pd.isnull(row['negociacion']),
                                                    pd.isnull(row['correo_compania']),
                                                    pd.isnull(row['telefono_compania']),
                                                    pd.isnull(row['nit_compania']),
                                                    pd.isnull(row['estado_compania']),
                                                    pd.isnull(row['banco']),
                                                    pd.isnull(row['centro']),
                                                    pd.isnull(row['informacion_legal']),
                                                    pd.isnull(row['direccion_legal']),
                                                    pd.isnull(row['metodo_pago']),
                                                    pd.isnull(row['despacho']),
                                                    pd.isnull(row['catalogo_id']),
                                                    pd.isnull(row['canal']),
                                                    data,
                                                    values)
            consult = consult.replace('\'','',consult.count('\''))

            cursor.execute(consult, values)
            connection.commit()

    # Cerrar el cursor
    cursor.close()

    dir_validation(os.path.dirname(__file__) + '\\uploadslog\\')

    df.to_excel(os.path.dirname(__file__) + '\\uploadslog\\' + 'carga {}.xlsx'.format(datetime.now().strftime("%d-%m-%Y %H_%M_%S")), index=False)

    # Retornar una respuesta exitosa
    return "Base de datos actualizada correctamente", 200
