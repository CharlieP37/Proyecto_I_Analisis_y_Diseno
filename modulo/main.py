from numpy import DataSource
import pandas as pd
import openpyxl as op
from flask import Flask, request

ruta_excel = 'MOCK_DATA.xlsx'

datos_excel = pd.read_excel(ruta_excel)

nombres_columas = datos_excel.columns
nombres_esperados = ['id', 'first_name', 'last_name', 'co', 'company', 'product']

print(datos_excel.iloc[0]["id"])

#print(datos_excel.head(2))


app = Flask(__name__)

@app.route("/producto", methods=["GET"])
def listar_productos():
    if(set(nombres_esperados) == set(nombres_columas)):
        productos = datos_excel.columns

        return f"Datos:\n\n{datos_excel.head(4)}"
    else:
        print('Hubo un error con los nombres')
        print('Nombres esperados: ', nombres_esperados)
        print('Nombres en el documentos: ', nombres_columas)
        return "Invalid Data, try again", 400

