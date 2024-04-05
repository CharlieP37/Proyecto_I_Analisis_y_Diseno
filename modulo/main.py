from ast import Not
from asyncio.windows_events import NULL
from datetime import *
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

#Importación de funciones para los querys de descarga
from querys import *

def BD_listar_columna(query):
    cursor1 = conexion1.cursor()
    cursor1.execute(query)
    filas = cursor1.fetchall()
    lista_identificadores = []
    for fila in filas:
        lista_identificadores.append(fila[0])
    return lista_identificadores

app = Flask(__name__)
conexion1 = connect_to_database()


@app.route('/download',  methods=["GET"])
def download():
    cursor1 = conexion1.cursor()
    cursor1.execute("select * from compania")
    filas = cursor1.fetchall()

    # Convertir los resultados en un DataFrame de pandas y guardarlo en un arhivo de excel
    df = pd.DataFrame(filas, columns=[desc[0] for desc in cursor1.description])
    ruta_excel = 'resultados_query.xlsx'
    df.to_excel(ruta_excel, index=False)

    cursor1.close()
    return send_file(ruta_excel, as_attachment=True, download_name='resultados_query.xlsx')

@app.route('/download/companias/',  methods=["GET"])
#Función definida para la descarga del archivo excel de la materia prima con o sin filtros
def dowloadcompanias():

    pais = request.args.get('pais')
    vendedor = request.args.get('vendedor')
    catalogo = request.args.get('catalogo')
    estado = request.args.get('estado')
    query = companiesdownload(pais, vendedor, catalogo, estado)

    cursor1 = conexion1.cursor()
    cursor1.execute(query)
    filas = cursor1.fetchall()

    # Convertir los resultados en un DataFrame de pandas y guardarlo en un arhivo de excel
    df = pd.DataFrame(filas, columns=[desc[0] for desc in cursor1.description])
    ruta_excel = os.path.dirname(__file__) + '\\downloadslog\\' + 'resultados_companias {}.xlsx'.format(datetime.now().strftime("%d-%m-%Y %H_%M_%S"))
    df.to_excel(ruta_excel, index=False)

    cursor1.close()
    return send_file(ruta_excel, as_attachment=True, download_name='resultados_companias.xlsx')

@app.route('/download/materia/',  methods=["GET"])
#Función definida para la descarga del archivo excel de la materia prima con o sin filtros
def dowloadmateria():
    pais = request.args.get('pais')
    bodega_sap = request.args.get('bodega_sap')
    categoria = request.args.get('categoria')
    urea = request.args.get('urea')
    estado = request.args.get('estado')
    sector = request.args.get('sector')
    query = rawmaterialdownload(pais, bodega_sap, categoria, urea, estado, sector)

    cursor1 = conexion1.cursor()
    cursor1.execute(query)
    filas = cursor1.fetchall()

    # Convertir los resultados en un DataFrame de pandas y guardarlo en un arhivo de excel
    df = pd.DataFrame(filas, columns=[desc[0] for desc in cursor1.description])
    ruta_excel = os.path.dirname(__file__) + '\\downloadslog\\' + 'resultados_materia {}.xlsx'.format(datetime.now().strftime("%d-%m-%Y %H_%M_%S"))
    df.to_excel(ruta_excel, index=False)

    cursor1.close()
    return send_file(ruta_excel, as_attachment=True, download_name='resultados_materia.xlsx')


@app.route('/download/clientes/',  methods=["GET"])
#Función definida para la descarga del archivo excel de los clientes con o sin filtros
def dowloadclientes():
    compania_sap = request.args.get('compania_sap')
    pais = request.args.get('pais')
    estado = request.args.get('estado')
    query = clientsdownload(compania_sap, pais, estado)

    cursor1 = conexion1.cursor()
    cursor1.execute(query)
    filas = cursor1.fetchall()

    # Convertir los resultados en un DataFrame de pandas y guardarlo en un arhivo de excel
    df = pd.DataFrame(filas, columns=[desc[0] for desc in cursor1.description])
    ruta_excel = os.path.dirname(__file__) + '\\downloadslog\\' + 'resultados_clientes {}.xlsx'.format(datetime.now().strftime("%d-%m-%Y %H_%M_%S"))
    df.to_excel(ruta_excel, index=False)

    cursor1.close()
    return send_file(ruta_excel, as_attachment=True, download_name='resultados_clientes.xlsx')

@app.route('/download/destinatario/',  methods=["GET"])
#Función definida para la descarga del archivo excel de los destinatarios con o sin filtros
def dowloaddestinatario():
    compania_sap = request.args.get('compania_sap')
    pais = request.args.get('pais')
    vendedor = request.args.get('vendedor')
    estado = request.args.get('estado')
    query = addresseedownload(compania_sap, pais, vendedor, estado)

    cursor1 = conexion1.cursor()
    cursor1.execute(query)
    filas = cursor1.fetchall()

    # Convertir los resultados en un DataFrame de pandas y guardarlo en un arhivo de excel
    df = pd.DataFrame(filas, columns=[desc[0] for desc in cursor1.description])
    ruta_excel = os.path.dirname(__file__) + '\\downloadslog\\' + 'resultados_destinatario {}.xlsx'.format(datetime.now().strftime("%d-%m-%Y %H_%M_%S"))
    df.to_excel(ruta_excel, index=False)

    cursor1.close()
    return send_file(ruta_excel, as_attachment=True, download_name='resultados_destinatario.xlsx')

@app.route('/upload', methods=["POST"])
def upload():
    archivo_excel = request.files['archivo']

    # Validar tipo archivo y manejo de error en la lectura (Información sobre el error "e")
    if not archivo_excel.filename.endswith('.xlsx'):
        return "Se esperaba un archivo Excel (.xlsx).", 400

    try:
        df = pd.read_excel(archivo_excel)
    except Exception as e:
        return f"Error al leer el archivo Excel: {str(e)}", 400

    # Validacion de datos por columna
    tipos_esperados = {'vendedor_id': int, 'compania_sap': str, 'nombre_compania': str, 'correo_compania': str, 'telefono_compania': str, 'nit_compania': str, 'pais_compania': int}
    for columna, tipo_esperado in tipos_esperados.items():
        if columna == 'vendedor_id':
            for valor in df[columna]:
                try:
                    valor_int = int(valor)
                    if valor_int < 0:
                        return f"La columna '{columna}' no puede contener valores negativos.", 400
                except ValueError:
                    return f"La columna '{columna}' debe contener valores numéricos enteros.", 400

    df = pd.read_excel(archivo_excel)
    cursor1 = conexion1.cursor()

    lista_compania_sap = BD_listar_columna("select compania_sap from compania")

    # Iterar sobre las filas del DataFrame
    for index, fila in df.iterrows():
        # Obtener los valores de las columnas para la fila actual
        vendedor_id = fila['vendedor_id'] #integer
        compania_sap = str(fila['compania_sap']) #varchar - pero lo toma como int
        nombre_compania = fila['nombre_compania'] #varchar
        pais_compania = fila['pais_compania'] # integer

        negociacion = fila['negociacion'] # boleano
        correo_compania = fila['correo_compania'] #varchar
        telefono_compania = fila['telefono_compania'] #varchar
        nit_compania = fila['nit_compania'] #varchar
        estado_compania = fila['estado_compania'] # integer
        banco = fila['banco'] #varchar
        centro = fila['centro'] #varchar
        informacion_legal = fila['informacion_legal'] #json
        direccion_legal = fila['direccion_legal'] #json
        metodo_pago = fila['metodo_pago'] #varchar
        despacho = fila['despacho'] #json
        catalogo_id = fila['catalogo_id'] #varchar
        canal = fila['canal'] #varchar

        while len(str(compania_sap)) < 7: # Agrega los 0 al inicio que se pierden cuando se obtiene la compania_sap del excel
            compania_sap = '0' + compania_sap

        datos = {
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


        if compania_sap in lista_compania_sap:
            # Ejecutar la consulta SQL para actualizar la base de datos
            valores = [vendedor_id,nombre_compania]
            consulta = crearQueryUpdateCompania(pd.isnull(fila['negociacion']),
                                pd.isnull(fila['correo_compania']),
                                pd.isnull(fila['telefono_compania']),
                                pd.isnull(fila['nit_compania']),
                                pd.isnull(fila['estado_compania']),
                                pd.isnull(fila['banco']),
                                pd.isnull(fila['centro']),
                                pd.isnull(fila['informacion_legal']),
                                pd.isnull(fila['direccion_legal']),
                                pd.isnull(fila['metodo_pago']),
                                pd.isnull(fila['despacho']),
                                pd.isnull(fila['catalogo_id']),
                                pd.isnull(fila['canal']),
                                datos,
                                valores)

            consulta = consulta.replace('\'','',consulta.count('\''))
            valores.append(compania_sap)
            cursor1.execute(consulta, valores)
            conexion1.commit()

        else:
            valores = [vendedor_id, compania_sap, nombre_compania]

            consulta = crearQueryInsertCompania(pd.isnull(fila['negociacion']),
                                pd.isnull(fila['correo_compania']),
                                pd.isnull(fila['telefono_compania']),
                                pd.isnull(fila['nit_compania']),
                                pd.isnull(fila['estado_compania']),
                                pd.isnull(fila['banco']),
                                pd.isnull(fila['centro']),
                                pd.isnull(fila['informacion_legal']),
                                pd.isnull(fila['direccion_legal']),
                                pd.isnull(fila['metodo_pago']),
                                pd.isnull(fila['despacho']),
                                pd.isnull(fila['catalogo_id']),
                                pd.isnull(fila['canal']),
                                datos,
                                valores)
            consulta = consulta.replace('\'','',consulta.count('\''))

            cursor1.execute(consulta, valores)
            conexion1.commit()

    # Cerrar el cursor
    cursor1.close()

    archivo_excel.save(os.path.dirname(__file__) + '\\uploadslog\\' + 'carga {}.xlsx'.format(datetime.now().strftime("%d-%m-%Y %H_%M_%S")))

    # Retornar una respuesta exitosa
    return "Base de datos actualizada correctamente", 200

def crearQueryUpdateCompania(negociacion,correo_compania,telefono_compania,nit_compania,estado_compania,
                        banco,centro,informacion_legal,direccion_legal,metodo_pago,despacho,catalogo_id, canal, datos, valores):
    consulta = "UPDATE compania SET"
    columnas = ['vendedor_id = %s', 'nombre_compania = %s']

    if not negociacion:
        columnas.append('negociacion = %s')
        valores.append(datos['negociacion'])

    if not correo_compania:
        columnas.append('correo_compania = %s')
        valores.append(datos['correo_compania'])

    if not telefono_compania:
        columnas.append('telefono_compania = %s')
        valores.append(datos['telefono_compania'])

    if not nit_compania:
        columnas.append('nit_compania = %s')
        valores.append(datos['nit_compania'])

    columnas.append('pais_compania = %s')
    valores.append(datos['pais_compania'])

    if not estado_compania:
        columnas.append('estado_compania = %s')
        valores.append(datos['estado_compania'])

    if not banco:
        columnas.append('banco = %s')
        valores.append(str(datos['banco'].replace("[", "{").replace("]", "}")))

    if not centro:
        columnas.append('centro = %s')
        valores.append(str(datos['centro'].replace("[", "{").replace("]", "}")))

    if not informacion_legal:
        columnas.append('informacion_legal = %s')
        valores.append(datos['informacion_legal'])

    if not direccion_legal:
        columnas.append('direccion_legal = %s')
        valores.append(datos['direccion_legal'])

    if not metodo_pago:
        columnas.append('metodo_pago = %s')
        valores.append(str(datos['metodo_pago'].replace("[", "{").replace("]", "}")))

    if not despacho:
        columnas.append('despacho = %s')
        valores.append(datos['despacho'])

    if not catalogo_id:
        columnas.append('catalogo_id = %s')
        valores.append(datos['catalogo_id'])

    if not canal:
        columnas.append('canal = %s')
        valores.append(str(datos['canal'].replace("[", "{").replace("]", "}")))

    consulta = f"{consulta}{columnas}"
    consulta = consulta.replace("[", " ").replace("]", "")

    return consulta + ' WHERE compania_sap = %s'



def crearQueryInsertCompania(negociacion,correo_compania,telefono_compania,nit_compania,estado_compania,
                        banco,centro,informacion_legal,direccion_legal,metodo_pago,despacho,catalogo_id, canal, datos, valores):
    consulta = "INSERT INTO compania"
    columnas = ['vendedor_id', 'compania_sap', 'nombre_compania']

    if not negociacion:
        columnas.append('negociacion')
        valores.append(datos['negociacion'])

    if not correo_compania:
        columnas.append('correo_compania')
        valores.append(datos['correo_compania'])

    if not telefono_compania:
        columnas.append('telefono_compania')
        valores.append(datos['telefono_compania'])

    if not nit_compania:
        columnas.append('nit_compania')
        valores.append(datos['nit_compania'])

    columnas.append('pais_compania')
    valores.append(datos['pais_compania'])

    if not estado_compania:
        columnas.append('estado_compania')
        valores.append(datos['estado_compania'])

    if not banco:
        columnas.append('banco')
        valores.append(str(datos['banco'].replace("[", "{").replace("]", "}")))

    if not centro:
        columnas.append('centro')
        valores.append(str(datos['centro'].replace("[", "{").replace("]", "}")))

    if not informacion_legal:
        columnas.append('informacion_legal')
        valores.append(datos['informacion_legal'])

    if not direccion_legal:
        columnas.append('direccion_legal')
        valores.append(datos['direccion_legal'])

    if not metodo_pago:
        columnas.append('metodo_pago')
        valores.append(str(datos['metodo_pago'].replace("[", "{").replace("]", "}")))

    if not despacho:
        columnas.append('despacho')
        valores.append(datos['despacho'])

    if not catalogo_id:
        columnas.append('catalogo_id')
        valores.append(datos['catalogo_id'])

    if not canal:
        columnas.append('canal')
        valores.append(str(datos['canal'].replace("[", "{").replace("]", "}")))

    consulta = f"{consulta}{columnas}"
    consulta = consulta.replace("[", "(").replace("]", ")")

    value = ['%s']
    while len(value) < len(columnas):
        value.append('%s')

    values = f" values {value}"
    values = values.replace("[", "(").replace("]", ")")

    return consulta + values
