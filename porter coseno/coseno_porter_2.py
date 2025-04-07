import pyodbc
import math
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import time

direccion_servidor = 'DESKTOP-KO6OH42'
nombre_bd = 'Porter'
nombre_usuario = 'sa'
password = 'ramitos2025'
try:
    conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                              direccion_servidor+';DATABASE='+nombre_bd+';UID='+nombre_usuario+';PWD=' + password)
    print("conexion exitosa")
    # OK! conexión exitosa
except Exception as e:
    # Atrapar error
    print("Ocurrió un error al conectar a SQL Server: ", e)

#funciones---------------------------------------------------------------------------------------
def  denominador(v_1):
    valor=0
    p_1=0
    for i in range(len(v_1)):
        p_1+=(v_1[i]*v_1[i])
    valor=math.sqrt(p_1)
    return valor

def numerador(v_1,v_2):
    res=0
    for i in range(len(v_1)):
        res+=(v_1[i]*v_2[i])
    return res

def calcular_coseno(mat_1, mat_2):
    i=0
    #para la primera palabra
    valor_1=[]
    #para la segunda palabra
    valor_2=[]
    for i in range(len(mat_1)):
        valor_1.append(float(mat_1[i][2]))
        valor_2.append(float(mat_2[i][2]))

    den_1=denominador(valor_1)
    den_2=denominador(valor_2)
    num = numerador(valor_1,valor_2)

    angulo=num/(den_1*den_2)
    return angulo



#--PALABRA 1 y PALABRA 2----------------------
ps=PorterStemmer()
palabra_1=[]
p1="run"
word1 = ps.stem(p1)


#-----PROCEDIMIENTO 1 CON TODOS
#----PALABRA 2

word2=[]
try:
    with conexion.cursor() as cursor:
        

        cursor.execute("select  distinct raices.raiz from PRelacion_2, raices where palabra1_id <> 1 and palabra1_id <> (select id_raiz from raices where raiz=?) and PRelacion_2.palabra1_id=raices.id_raiz order by raices.raiz;",word1)
        # Con fetchall traemos todas las filas
        word2 = cursor.fetchall()
       

except Exception as e:
    print("Ocurrió un error al consultar: ", e)



#---------------------

print(word1)
#print(len(word2))
for i in range (41500):
    palabra_2=[]
    try:
        with conexion.cursor() as cursor:
            #print("\nentra sacado: ")
            cursor.execute("select lema_1, lema_2, W from hallar_w(?) ",word1)
            # Con fetchall traemos todas las filas
            palabra_1 = cursor.fetchall()

            cursor.execute("select lema_1, lema_2, W from hallar_w(?)",word2[i][0])
            # Con fetchall traemos todas las filas
            palabra_2 = cursor.fetchall()
            #print("\nsacado: ")

    except Exception as e:
        print("Ocurrió un error al consultar: ", e)

    print("\nlema 2: "+word2[i][0])
    print(calcular_coseno(palabra_1,palabra_2))




#-----PROCEDIMIENTO 1 A 1
'''
palabra_2=[]
p2="cat"


word2=ps.stem(p2)

try:
    with conexion.cursor() as cursor:
        
        cursor.execute("select lema_1,lema_2,sum(W) from (	select lema_1, lema_2, W from hallar_w(?) union	select ?,lema_2,0 from hallar_w(?) ) as R group by lema_1,lema_2 order by lema_2",word1,word1, word2)
        # Con fetchall traemos todas las filas
        palabra_1 = cursor.fetchall()

        cursor.execute("select lema_1,lema_2,sum(W) from (	select lema_1, lema_2, W from hallar_w(?) union	select ?,lema_2,0 from hallar_w(?) ) as R group by lema_1,lema_2 order by lema_2",word2,word2, word1)
        # Con fetchall traemos todas las filas
        palabra_2 = cursor.fetchall()
    

except Exception as e:
    print("Ocurrió un error al consultar: ", e)

print("lema1: "+word1+"\nlema 2: "+word2)
print(calcular_coseno(palabra_1,palabra_2))
'''


#start = time.time()
#end = time.time()

#print(end - start)