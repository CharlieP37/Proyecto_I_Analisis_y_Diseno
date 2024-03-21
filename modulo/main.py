from lib2to3.fixes.fix_tuple_params import tuple_name
from numpy import DataSource
import pandas as pd
import openpyxl as op
from flask import Flask, request, send_file

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


@app.route('/upload', methods=["POST"])
def upload():
    archivo_excel = request.files['archivo']
    df = pd.read_excel(archivo_excel)
    cursor1 = conexion1.cursor()

    lista_compania_sap = BD_listar_columna("select compania_sap from compania")

    # Iterar sobre las filas del DataFrame
    for index, fila in df.iterrows():
        # Obtener los valores de las columnas para la fila actual
        vendedor_id = fila['vendedor_id'] #integer
        compania_sap = fila['compania_sap'] #varchar
        nombre_compania = fila['nombre_compania'] #varchar
        correo_compania = fila['correo_compania'] #varchar
        telefono_compania = fila['telefono_compania'] #varchar
        nit_compania = fila['nit_compania'] #varchar
        pais_compania = fila['pais_compania'] # integer

        if str(compania_sap) in lista_compania_sap:
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


