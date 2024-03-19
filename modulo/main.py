import email
from numpy import DataSource
import pandas as pd
import openpyxl as op
from flask import Flask, request, send_file
import psycopg2

import io
from database import connect_to_database

ruta_excel = 'MOCK_DATA.xlsx'
ruta_excel2 = 'id_empresa.xlsx'

datos_excel = pd.read_excel(ruta_excel)
datos_Nombres_empresa = pd.read_excel(ruta_excel2)


datos_excel['company'] = datos_excel['company'].astype(str)
datos_Nombres_empresa['name_company'] = datos_Nombres_empresa['name_company'].astype(str)

datos_combinados = pd.DataFrame(datos_excel)
#datos_combinados['company'].iloc[0] = datos_Nombres_empresa['name_company'].iloc[0]

#print(datos_combinados.head(4))


mapping_dict = dict(zip(datos_Nombres_empresa['id_empresa'], datos_Nombres_empresa['name_company']))
datos_excel['company'] = datos_excel['company'].map(mapping_dict)

nombres_columas = datos_excel.columns
nombres_esperados = ['id', 'first_name', 'last_name', 'email', 'company', 'product']


#print("Datos Excel despues de la modificacion:")
#print(datos_excel.head())
#print(datos_excel.iloc[0]["first_name"])
#print(datos_excel.iloc[0])


#verifica los nombres de las columnas al momento de cargar el excel
def verificar_nombres_columnas(datos_excel, nombres_esperados):
    nombres_columas = datos_excel.columns.tolist()
    if nombres_columas == nombres_esperados:
        return True
    else:
        return False

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


app = Flask(__name__)
conexion1 = connect_to_database()

@app.route("/producto", methods=["GET"])
def listar_productos():
    if(set(nombres_esperados) == set(nombres_columas)):
        return f"Datos:\n\n{datos_excel.head(4)}"
    else:
        print('Hubo un error con los nombres')
        print('Nombres esperados: ', nombres_esperados)
        print('Nombres en el documentos: ', nombres_columas)
        return "Nombre de las columnas incorrectos", 400


@app.route('/descargar_excel',  methods=["POST"])
def descargar_excel():
    data = request.json  # Obtener los datos enviados en el cuerpo de la solicitud como JSON
    correo = data.get('correo')  # Obtener el correo electrónico del JSON

    # Buscar el correo electrónico en el DataFrame 'datos_excel'
    resultado = datos_combinados[datos_combinados['email'] == correo]
    if resultado.empty:
        return "Correo electrónico no encontrado", 404

    # Elimina las columnas deseadas
    eliminar = ['id','product']
    resultado.drop(eliminar, axis=1, inplace=True,)

    # Convierte el DataFrame a un objeto BytesIO para la descarga
    buffer = io.BytesIO()
    # Archivo a descargar
    resultado.to_excel(buffer, index=False, sheet_name='Datos', engine='openpyxl')
    buffer.seek(0)

    # Configura las cabeceras para la descarga del archivo
    return send_file(buffer, download_name='datos_descargados.xlsx', as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route("/datos_combinados", methods=["GET"])
def mostrar_datos_combinados():
    return f"Datos Combinados:\n\n{datos_combinados.head(4)}"


@app.route('/download',  methods=["GET"])
def download():
    cursor1 = conexion1.cursor()
    cursor1.execute("select * from compania")
    filas = cursor1.fetchall()

    # Convertir los resultados en un DataFrame de pandas
    df = pd.DataFrame(filas, columns=[desc[0] for desc in cursor1.description])

    # Guardar los resultados en un archivo Excel temporal
    ruta_excel = 'resultados_query.xlsx'
    df.to_excel(ruta_excel, index=False)

    # Cerrar el cursor
    cursor1.close()

    # Enviar el archivo Excel como respuesta para descargar
    return send_file(ruta_excel, as_attachment=True, download_name='resultados_query.xlsx')