# controllers/productos_controller.py

from .database import get_db_connection # type: ignore
from models.productos import Producto  # Suponiendo que tienes un modelo Producto

# Obtener todos los productos
def obtener_productos():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Productos")  # Ajusta esta consulta según tu base de datos
    rows = cursor.fetchall()
    productos = [Producto(id_producto=row[0], nombre=row[1], marca=row[2], precio=row[3], stock=row[4], litros=row[5]) for row in rows]
    connection.close()
    return productos

# Obtener un producto por su ID
def obtener_producto_por_id(producto_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Productos WHERE id_producto = %s", (producto_id,))
    row = cursor.fetchone()
    connection.close()
    if row:
        return Producto(id_producto=row[0], nombre=row[1], marca=row[2], precio=row[3], stock=row[4], litros=row[5])
    return None

# Agregar un nuevo producto
def agregar_producto(nombre, marca, precio, stock, litros):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO Productos (nombre, marca, precio, stock, litros)
        VALUES (%s, %s, %s, %s, %s)
    """, (nombre, marca, precio, stock, litros))
    connection.commit()
    connection.close()

# Modificar un producto existente
def modificar_producto(producto_id, nombre, marca, precio, stock, litros):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Productos
        SET nombre = %s, marca = %s, precio = %s, stock = %s, litros = %s
        WHERE id_producto = %s
    """, (nombre, marca, precio, stock, litros, producto_id))
    connection.commit()
    connection.close()

# Eliminar un producto por su ID
def eliminar_producto(producto_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Productos WHERE id_producto = %s", (producto_id,))
    connection.commit()
    connection.close()
