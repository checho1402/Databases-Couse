import pyodbc
import math as ma
import nltk
from nltk.tokenize import word_tokenize

direccion_servidor = 'ROD-LAPTOP'
nombre_bd = 'Porter'
nombre_usuario = 'sa'
password = 'R1234'
try:
    conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                              direccion_servidor+';DATABASE='+nombre_bd+';UID='+nombre_usuario+';PWD=' + password)
    print("conexion exitosa")
    # OK! conexión exitosa
except Exception as e:
    # Atrapar error
    print("Ocurrió un error al conectar a SQL Server: ", e)


def tokenizes(file):
    token = []
    for i in range(len(file)):
        token.append(file[i].split())
    return token

cantidad_datos=24713177
f=open('tabla_IDF.txt','w',encoding ="utf-8")

try:
    with conexion.cursor() as cursor:
        # En este caso no necesitamos limpiar ningún dato
        cursor.execute("select  palabra2_id,count(*) from PRelacion_2 group by palabra2_id order by palabra2_id;")

        # Con fetchall traemos todas las filas
        datos = cursor.fetchall()

        # Recorrer e imprimir
        for i in range(len(datos)):
            num=cantidad_datos/datos[i][1]
            n_num=ma.log10(num)
            f.write(str(datos[i][0])+'\t'+str(n_num) + '\n')
            


        

except Exception as e:
    print("Ocurrió un error al consultar: ", e)

finally:
    conexion.close()

f.close()