# database/db_connection.py

import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",  # Usa tu contraseña
            database="gestionbebidas"
        )
        return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
