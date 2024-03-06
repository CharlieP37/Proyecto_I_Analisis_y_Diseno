import pandas as pd
import openpyxl as op

ruta_excel = 'MOCK_DATA.xlsx'

datos_excel = pd.read_excel(ruta_excel)

print(datos_excel)