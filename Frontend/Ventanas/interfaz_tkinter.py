import tkinter as tk
from tkinter import ttk
from Ventanas.producto import filtrar_productos  


def abrir_ventana():
    ventana = tk.Toplevel()
    ventana.title("Ventana Secundaria")
    ventana.geometry("400x300")
    
    # Botón "Volver"
    boton_volver = tk.Button(ventana, text="← Volver", font=("Segoe UI", 10, "bold"), bg="#7289DA", fg="white",
                             command=ventana.destroy)
    boton_volver.pack(padx=10, pady=10, anchor="nw")  # Arriba a la izquierda


def aplicar_filtro():
    nombre = entry_nombre.get()
    marca = entry_marca.get()
    try:
        precio_min = float(entry_precio_min.get()) if entry_precio_min.get() else None
    except ValueError:
        precio_min = None
    try:
        precio_max = float(entry_precio_max.get()) if entry_precio_max.get() else None
    except ValueError:
        precio_max = None
    try:
        stock_min = int(entry_stock_min.get()) if entry_stock_min.get() else None
    except ValueError:
        stock_min = None

    productos = filtrar_productos(nombre, marca, precio_min, precio_max, stock_min)
    actualizar_tabla(productos)

def actualizar_tabla(productos):
    for fila in tabla.get_children():
        tabla.delete(fila)
    for producto in productos:
        tabla.insert("", tk.END, values=producto)

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Gestión de Productos - Filtrado")
ventana.geometry("900x500")
ventana.configure(bg="#2b2b2b")

# Frame de filtros
filtro_frame = tk.Frame(ventana, bg="#2b2b2b")
filtro_frame.pack(pady=10)

tk.Label(filtro_frame, text="Nombre", fg="white", bg="#2b2b2b").grid(row=0, column=0)
entry_nombre = tk.Entry(filtro_frame)
entry_nombre.grid(row=0, column=1)

tk.Label(filtro_frame, text="Marca", fg="white", bg="#2b2b2b").grid(row=0, column=2)
entry_marca = tk.Entry(filtro_frame)
entry_marca.grid(row=0, column=3)

tk.Label(filtro_frame, text="Precio Min", fg="white", bg="#2b2b2b").grid(row=1, column=0)
entry_precio_min = tk.Entry(filtro_frame)
entry_precio_min.grid(row=1, column=1)

tk.Label(filtro_frame, text="Precio Max", fg="white", bg="#2b2b2b").grid(row=1, column=2)
entry_precio_max = tk.Entry(filtro_frame)
entry_precio_max.grid(row=1, column=3)

tk.Label(filtro_frame, text="Stock Min", fg="white", bg="#2b2b2b").grid(row=2, column=0)
entry_stock_min = tk.Entry(filtro_frame)
entry_stock_min.grid(row=2, column=1)

boton_filtrar = tk.Button(filtro_frame, text="Aplicar Filtro", command=aplicar_filtro)
boton_filtrar.grid(row=2, column=3, pady=5)

# Tabla de productos
columnas = ("ID", "Nombre", "Marca", "Precio", "Stock", "Litros", "Imagen")
tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=15)
for col in columnas:
    tabla.heading(col, text=col)
    tabla.column(col, anchor=tk.CENTER, width=100)

tabla.pack(pady=20)

ventana.mainloop()
