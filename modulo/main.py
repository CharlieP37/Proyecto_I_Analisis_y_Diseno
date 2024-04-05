from numpy import DataSource
import pandas as pd
import openpyxl as op
import re
from flask import Flask, request, send_file

import io
from database import connect_to_database

#Importación de funciones para los querys de descarga
from querys import *

def verificar_filas(datos_excel):
    # Verifica que el DataFrame no tenga valores nulos
    if datos_excel.isnull().values.any():
        return False

    # Verifica los tipos de datos de cada columna, al email le coloque str porque los correos estan inventados y no llevan una secuencia
    tipos_esperados = {'id': int, 'first_name': str, 'last_name': str, 'email': str, 'company': int, 'product': str}
    for columna, tipo_esperado in tipos_esperados.items():
        if datos_excel[columna].dtype != tipo_esperado:
            return False

    # Verifica que el id sea un número entero valor unico
    if datos_excel['id'].dtype != int:
        return False

    # Verifica que el id no tenga valores negativos
    if (datos_excel['id'] < 0).any():
        return False

    return True


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
    ruta_excel = 'resultados_companias.xlsx'
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
    ruta_excel = 'resultados_materia.xlsx'
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
    ruta_excel = 'resultados_clientes.xlsx'
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
    ruta_excel = 'resultados_destinatario.xlsx'
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

        elif columna == 'telefono_compania':
            for valor in df[columna]:
                if not ((isinstance(valor, str) or isinstance(valor, int)) and len(str(valor)) <= 45):
                    return f"La columna '{columna}' es incorrecta", 400
                
        elif columna == 'nit_compania':
            for valor in df[columna]:
                if not ((isinstance(valor, str) or isinstance(valor, int)) and len(str(valor)) <= 45):
                    return f"La columna '{columna}' es incorrecta", 400


    # Validar el formato del correo electrónico
    patron_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    for index, fila in df.iterrows():
        if not re.match(patron_email, str(fila['correo_compania'])):
            return f"El correo electrónico '{fila['correo_compania']}' no tiene un formato válido.", 400

    df = pd.read_excel(archivo_excel)
    cursor1 = conexion1.cursor()

    lista_compania_sap = BD_listar_columna("select compania_sap from compania")

    # Iterar sobre las filas del DataFrame
    for index, fila in df.iterrows():
        # Obtener los valores de las columnas para la fila actual
        vendedor_id = fila['vendedor_id'] #integer
        compania_sap = fila['compania_sap'] #varchar - pero lo toma como int
        nombre_compania = fila['nombre_compania'] #varchar
        correo_compania = fila['correo_compania'] #varchar
        telefono_compania = fila['telefono_compania'] #varchar
        nit_compania = fila['nit_compania'] #varchar
        pais_compania = fila['pais_compania'] # integer

        lista_compania_sap = [int(i) for i in lista_compania_sap] #Conversión de str a int de la consulta a bd

        if compania_sap in lista_compania_sap:
            # Ejecutar la consulta SQL para actualizar la base de datos
            consulta =  """ UPDATE  compania
                            SET     vendedor_id = %s, nombre_compania = %s, correo_compania = %s, telefono_compania = %s, nit_compania = %s, pais_compania = %s
                            WHERE   compania_sap = %s
                        """
            datos= (vendedor_id, str(nombre_compania), str(correo_compania), str(telefono_compania), str(nit_compania), pais_compania, str(compania_sap))
            cursor1.execute(consulta, datos)
            conexion1.commit()

        else:
            consulta =  """ INSERT INTO compania(vendedor_id, compania_sap, nombre_compania, correo_compania, telefono_compania, nit_compania, pais_compania)
                            values (%s,%s,%s,%s,%s,%s,%s)
                        """
            datos=(vendedor_id, compania_sap, nombre_compania, correo_compania, telefono_compania, nit_compania, pais_compania)
            cursor1.execute(consulta, datos)
            conexion1.commit()

    # Cerrar el cursor
    cursor1.close()

    # Retornar una respuesta exitosa
    return "Base de datos actualizada correctamente", 200


