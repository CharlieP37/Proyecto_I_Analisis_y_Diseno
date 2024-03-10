from numpy import DataSource
import pandas as pd
import openpyxl as op
from flask import Flask, request

ruta_excel = 'MOCK_DATA.xlsx'

datos_excel = pd.read_excel(ruta_excel)

nombres_columas = datos_excel.columns
nombres_esperados = ['id', 'first_name', 'last_name', 'email', 'company', 'product']

print(datos_excel.iloc[0]["first_name"])
print(datos_excel.iloc[0])

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

