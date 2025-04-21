# productos.py
from database import get_db_connection
from tkinter import messagebox

# Función para crear un nuevo producto
def crear_producto(nombre, marca, precio, stock, litros, imagen):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                INSERT INTO Productos (nombre, marca, precio, stock, litros, imagen) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (nombre, marca, precio, stock, litros, imagen))
                conn.commit()
        return True
    except Exception as e:
        print(f"Error al crear producto: {e}")
        return False

# Función para obtener todos los productos
def obtener_productos():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id_producto, nombre, marca, precio, stock, litros, imagen FROM Productos")
                productos = cursor.fetchall()
        return productos
    except Exception as e:
        print(f"Error al obtener productos: {e}")
        return []

# Función para eliminar un producto por ID
def eliminar_producto(producto_id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM Productos WHERE id_producto = %s", (producto_id,))
                conn.commit()
        return True
    except Exception as e:
        print(f"Error al eliminar producto: {e}")
        return False

# Función para actualizar un producto existente
def actualizar_producto(producto_id, nombre, marca, precio, stock, litros, imagen):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                UPDATE Productos 
                SET nombre = %s, marca = %s, precio = %s, stock = %s, litros = %s, imagen = %s 
                WHERE id_producto = %s
                """
                cursor.execute(query, (nombre, marca, precio, stock, litros, imagen, producto_id))
                conn.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar producto: {e}")
        return False

def filtrar_productos(nombre=None, marca=None, precio_min=None, precio_max=None, stock_min=None, stock_max=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT id_producto, nombre, marca, precio, stock, litros, imagen FROM Productos WHERE 1=1"
        valores = []

        if nombre:
            query += " AND nombre LIKE %s"
            valores.append(f"%{nombre}%")
        if marca:
            query += " AND marca LIKE %s"
            valores.append(f"%{marca}%")
        if precio_min is not None:
            query += " AND precio >= %s"
            valores.append(precio_min)
        if precio_max is not None:
            query += " AND precio <= %s"
            valores.append(precio_max)
        if stock_min is not None:
            query += " AND stock >= %s"
            valores.append(stock_min)
        if stock_max is not None:
            query += " AND stock <= %s"
            valores.append(stock_max)

        cursor.execute(query, valores)
        resultados = cursor.fetchall()

        conn.close()
        return resultados

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron filtrar los productos: {e}")
        return []

def filtrar_productos(nombre='', marca=''):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT id_producto, nombre, marca, precio, stock, litros FROM Productos WHERE 1=1"
                params = []

                if nombre:
                    query += " AND nombre LIKE %s"
                    params.append(f"%{nombre}%")
                if marca:
                    query += " AND marca LIKE %s"
                    params.append(f"%{marca}%")

                cursor.execute(query, tuple(params))
                return cursor.fetchall()
    except Exception as e:
        print(f"Error al filtrar productos: {e}")
        return []


def verificar_stock_bajo():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT nombre, stock, stock_minimo FROM productos WHERE stock <= stock_minimo")
                productos_bajo_stock = cursor.fetchall()

                if productos_bajo_stock:
                    mensaje = "¡Atención! Los siguientes productos tienen bajo stock:\n\n"
                    for nombre, stock, minimo in productos_bajo_stock:
                        mensaje += f"- {nombre}: {stock} unidades (mínimo: {minimo})\n"
                    messagebox.showwarning("Stock Bajo", mensaje)
    except Exception as e:
        print(f"Error al verificar stock bajo: {e}")
