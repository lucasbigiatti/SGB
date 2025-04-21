import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Función para conectar a la base de datos
def conectar_db():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="GestionBebidas"
        )
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {e}")
        return None


def abrir_ventana():
    ventana = tk.Toplevel()
    ventana.title("Ventana Secundaria")
    ventana.geometry("400x300")
    
    # Botón "Volver"
    boton_volver = tk.Button(ventana, text="← Volver", font=("Segoe UI", 10, "bold"), bg="#7289DA", fg="white",
                             command=ventana.destroy)
    boton_volver.pack(padx=10, pady=10, anchor="nw")  # Arriba a la izquierda


# Función para abrir la ventana de agregar productos
def ventana_agregar_producto():
    def guardar_producto():
        nombre = entry_nombre.get()
        marca = entry_marca.get()
        precio = entry_precio.get()
        stock = entry_stock.get()
        id_proveedor = entry_proveedor.get()
        
        if not nombre or not marca or not precio or not stock or not id_proveedor:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        conn = conectar_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Productos (nombre, marca, precio, stock, id_proveedor) VALUES (%s, %s, %s, %s, %s)",
                           (nombre, marca, precio, stock, id_proveedor))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            ventana.destroy()
    
    ventana = tk.Toplevel(root)
    ventana.title("Agregar Producto")
    tk.Label(ventana, text="Nombre:").grid(row=0, column=0)
    entry_nombre = tk.Entry(ventana)
    entry_nombre.grid(row=0, column=1)
    tk.Label(ventana, text="Marca:").grid(row=1, column=0)
    entry_marca = tk.Entry(ventana)
    entry_marca.grid(row=1, column=1)
    tk.Label(ventana, text="Precio:").grid(row=2, column=0)
    entry_precio = tk.Entry(ventana)
    entry_precio.grid(row=2, column=1)
    tk.Label(ventana, text="Stock:").grid(row=3, column=0)
    entry_stock = tk.Entry(ventana)
    entry_stock.grid(row=3, column=1)
    tk.Label(ventana, text="ID Proveedor:").grid(row=4, column=0)
    entry_proveedor = tk.Entry(ventana)
    entry_proveedor.grid(row=4, column=1)
    tk.Button(ventana, text="Guardar", command=guardar_producto).grid(row=5, column=0, columnspan=2)

# Ventana principal
root = tk.Tk()
root.title("Gestión de Bebidas")

# Botones para elegir qué agregar
tk.Label(root, text="Seleccione qué desea agregar").pack()
tk.Button(root, text="Agregar Producto", command=ventana_agregar_producto).pack()

root.mainloop()
