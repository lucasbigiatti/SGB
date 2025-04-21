from database import get_db_connection
from models.clientes import Cliente

class ClienteController:

    @staticmethod
    def obtener_clientes():
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Clientes")
        rows = cursor.fetchall()
        clientes = [Cliente(id_cliente=row[0], nombre=row[1]) for row in rows]
        connection.close()
        return clientes

    @staticmethod
    def agregar_cliente(nombre):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Clientes (nombre) VALUES (%s)", (nombre,))
        connection.commit()
        connection.close()
