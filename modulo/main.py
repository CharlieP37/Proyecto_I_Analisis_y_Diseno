from numpy import DataSource
import pandas as pd
import openpyxl as op
from flask import Flask, request, send_file
import io

ruta_excel = 'MOCK_DATA.xlsx'
ruta_excel2 = 'id_empresa.xlsx'

datos_excel = pd.read_excel(ruta_excel)
datos_Nombres_empresa = pd.read_excel(ruta_excel2)


datos_excel['company'] = datos_excel['company'].astype(str)
datos_Nombres_empresa['name_company'] = datos_Nombres_empresa['name_company'].astype(str)

datos_combinados = datos_excel
datos_combinados['company'].iloc[0] = datos_Nombres_empresa['name_company'].iloc[0]
#print(datos_combinados.head())


nombres_columas = datos_excel.columns
nombres_esperados = ['id', 'first_name', 'last_name', 'email', 'company', 'product']

#print(datos_excel.iloc[0]["first_name"])
#print(datos_excel.iloc[0])

app = Flask(__name__)

@app.route("/producto", methods=["GET"])
def listar_productos():
    if(set(nombres_esperados) == set(nombres_columas)):
        return f"Datos:\n\n{datos_excel.head(4)}"
    else:
        print('Hubo un error con los nombres')
        print('Nombres esperados: ', nombres_esperados)
        print('Nombres en el documentos: ', nombres_columas)
        return "Nombre de las columnas incorrectos", 400

@app.route('/descargar_excel')
def descargar_excel():

    # Convierte el DataFrame a un objeto BytesIO para la descarga
    buffer = io.BytesIO()
    # Archivo a descargar
    datos_excel.to_excel(buffer, index=False, sheet_name='Datos', engine='openpyxl')
    buffer.seek(0)

    # Configura las cabeceras para la descarga del archivo
    return send_file(buffer, download_name='datos_descargados.xlsx', as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route("/datos_combinados", methods=["GET"])
def mostrar_datos_combinados():
    return f"Datos Combinados:\n\n{datos_combinados.head(4)}"