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

tabla1=[]
tabla_TF=[]
tabla_W=[]

tabla_id=[]


v_max=0

#avanzar=[]

#cantidad_datos=24713177

palabra="aal"

try:
    with conexion.cursor() as cursor:
        # En este caso no necesitamos limpiar ningún dato
        #cursor.execute("select R.raiz, J.raiz, valor from PRelacion_2, raices as R, raices as J where palabra1_id=(select id_raiz from raices where raiz= ?) and palabra1_id = R.id_raiz and palabra2_id = j.id_raiz order by R.raiz, J.raiz asc;",palabra)
        cursor.execute("select R.raiz, J.raiz, valor from PRelacion_2, raices as R, raices as J where palabra1_id=1 and palabra1_id = R.id_raiz and palabra2_id = j.id_raiz order by R.raiz, J.raiz asc;")

        # Con fetchall traemos todas las filas
        datos = cursor.fetchall()

        # Recorrer e imprimir
        for dato in datos:
            #print(dato)
            tabla1.append(dato)
            tabla_TF.append(dato)
            tabla_W.append(dato)

        '''
        cursor.execute("select  count(palabra2_id) from PRelacion_2 group by palabra1_id order by palabra1_id order by R.raiz, J.raiz asc")
        aux = cursor.fetchall()
        for aux_1 in aux:
        avanzar.append(aux_1)'''

        #cursor.execute("select  max(valor) from PRelacion_2 where palabra1_id=(select id_raiz from raices where raiz= ?) group by palabra1_id order by palabra1_id;",palabra)
        cursor.execute("select  max(valor) from PRelacion_2 where palabra1_id=1 group by palabra1_id order by palabra1_id;")
        m= cursor.fetchall()
        v_max=m[0]
        
        #cursor.execute("select palabra2_id from PRelacion_2 where palabra1_id=(select id_raiz from raices where raiz= ?) order by palabra2_id asc;",palabra)
        cursor.execute("select palabra2_id from PRelacion_2 where palabra1_id=1 order by palabra2_id asc;")
        d= cursor.fetchall()
        for d_1 in d:
            tabla_id.append(d_1)


        

except Exception as e:
    print("Ocurrió un error al consultar: ", e)

finally:
    conexion.close()


'''for i in range(len(tabla_TF)):
    print(tabla_TF[i][2])'''


'''
print(tabla1[0][0])
print(cantidad_raiz_2[0])
for i in range(0,len(tabla1),cantidad_raiz_2):
    palabra=tabla1[i][0]
    max_valor=tabla1[i][2]
    #avanzar segun la cantidad de raices 2 que existe 
    for j in range(i,i+cantidad_raiz_2):
        if(tabla1[j][2]>max_valor): max_valor=tabla1[j][2]
    tabla_v_max.append(max_valor)
'''
#print(tabla_v_max)
print("TF:")
print(v_max[0])
f=open('tabla_TF.txt','w',encoding ="utf-8")

#primer for para saber el numero de palabras1, para aaceder al mayor valor de cada uno
for i in range(len(tabla1)):
    #Para moverse en la tabla grande
    
    tabla_TF[i][2]=tabla1[i][2]/v_max[0]
    f.write(tabla_TF[i][0]+ '\t'+ tabla_TF[i][1]+'\t' + str(tabla_TF[i][2])+ '\n')

f.close()


idf=open('tabla_IDF.txt','r',encoding ="utf-8")
tabla_IDF=tokenizes(idf.readlines())
idf.close()





print("W:")
w=open('tabla_W.txt','w',encoding ="utf-8")
for i in range(len(tabla_id)):
    indice= tabla_id[i][0]
    val=0
    in_aux=0
    for aux in range(in_aux,len(tabla_IDF)):
        if(indice==float(tabla_IDF[aux][0])):
            val=float(tabla_IDF[aux][1])
            in_aux=aux
            break
    
    tabla_W[i][2]=tabla_TF[i][2]*val
    w.write(tabla_W[i][0]+ '\t'+ tabla_W[i][1]+'\t' + str(tabla_W[i][2])+ '\n')

w.close()

#//////////////////////////////////////////////////////////////////////////////////////
