import pymysql

def obtener_conexion():
    return pymysql.connect(host='localhost',
                       user='Pokecharlie',
                       password='root',
                       db='juegos')
                            