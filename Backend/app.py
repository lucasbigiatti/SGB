import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar_db
import os

# Función para obtener productos desde MySQL
def cargar_productos():
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Productos")
        productos = cursor.fetchall()
        conn.close()

        for row in tabla.get_children():
            tabla.delete(row)

        for producto in productos:
            tabla.insert("", "end", values=producto)

# Función para agregar un producto
def agregar_producto():
    nombre = entry_nombre.get()
    marca = entry_marca.get()
    precio = entry_precio.get()
    stock = entry_stock.get()

    if not nombre or not marca or not precio or not stock:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Productos (nombre, marca, precio, stock, id_proveedor) VALUES (%s, %s, %s, %s, 1)", 
                       (nombre, marca, precio, stock))
        conn.commit()
        conn.close()
        cargar_productos()
        limpiar_campos()
        messagebox.showinfo("Éxito", "Producto agregado correctamente")

# Función para cargar datos al seleccionar un producto
def seleccionar_producto(event):
    item = tabla.selection()
    if item:
        valores = tabla.item(item, "values")
        entry_id.delete(0, tk.END)
        entry_id.insert(0, valores[0])
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, valores[1])
        entry_marca.delete(0, tk.END)
        entry_marca.insert(0, valores[2])
        entry_precio.delete(0, tk.END)
        entry_precio.insert(0, valores[3])
        entry_stock.delete(0, tk.END)
        entry_stock.insert(0, valores[4])

# Función para editar un producto
def editar_producto():
    id_producto = entry_id.get()
    nombre = entry_nombre.get()
    marca = entry_marca.get()
    precio = entry_precio.get()
    stock = entry_stock.get()

    if not id_producto or not nombre or not marca or not precio or not stock:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Productos SET nombre=%s, marca=%s, precio=%s, stock=%s WHERE id_producto=%s", 
                       (nombre, marca, precio, stock, id_producto))
        conn.commit()
        conn.close()
        cargar_productos()
        limpiar_campos()
        messagebox.showinfo("Éxito", "Producto editado correctamente")

# Función para eliminar un producto
def eliminar_producto():
    id_producto = entry_id.get()
    if not id_producto:
        messagebox.showerror("Error", "Selecciona un producto para eliminar")
        return

    respuesta = messagebox.askyesno("Confirmar", "¿Seguro que quieres eliminar este producto?")
    if respuesta:
        conn = conectar_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Productos WHERE id_producto=%s", (id_producto,))
            conn.commit()
            conn.close()
            cargar_productos()
            limpiar_campos()
            messagebox.showinfo("Éxito", "Producto eliminado correctamente")

# Función para limpiar los campos de entrada
def limpiar_campos():
    entry_id.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_marca.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    entry_stock.delete(0, tk.END)

# Crear ventana principal
root = tk.Tk()
root.title("Gestión de Productos - Tkinter & MySQL")
root.geometry("650x450")

# Entradas
tk.Label(root, text="ID:").grid(row=0, column=0)
entry_id = tk.Entry(root)
entry_id.grid(row=0, column=1)
entry_id.config(state="readonly")  # Solo lectura

tk.Label(root, text="Nombre:").grid(row=1, column=0)
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=1, column=1)

tk.Label(root, text="Marca:").grid(row=2, column=0)
entry_marca = tk.Entry(root)
entry_marca.grid(row=2, column=1)

tk.Label(root, text="Precio:").grid(row=3, column=0)
entry_precio = tk.Entry(root)
entry_precio.grid(row=3, column=1)

tk.Label(root, text="Stock:").grid(row=4, column=0)
entry_stock = tk.Entry(root)
entry_stock.grid(row=4, column=1)

# Botones
btn_agregar = tk.Button(root, text="Agregar", command=agregar_producto)
btn_agregar.grid(row=5, column=0)

btn_editar = tk.Button(root, text="Editar", command=editar_producto)
btn_editar.grid(row=5, column=1)

btn_eliminar = tk.Button(root, text="Eliminar", command=eliminar_producto)
btn_eliminar.grid(row=5, column=2)

btn_limpiar = tk.Button(root, text="Limpiar", command=limpiar_campos)
btn_limpiar.grid(row=5, column=3)

# Tabla de productos
columnas = ("ID", "Nombre", "Marca", "Precio", "Stock", "Proveedor")
tabla = ttk.Treeview(root, columns=columnas, show="headings")
for col in columnas:
    tabla.heading(col, text=col)
tabla.grid(row=6, column=0, columnspan=4)
tabla.bind("<<TreeviewSelect>>", seleccionar_producto)

# Cargar productos al iniciar
cargar_productos()

# Ejecutar la aplicación
root.mainloop()
