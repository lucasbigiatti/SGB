import tkinter as tk
from tkinter import ttk
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Ventanas.producto import abrir_gestion_productos

root = tk.Tk()
root.title("Gestión de Bebidas")
root.geometry("600x400")
root.configure(bg="#2C2F33")  # Color gris oscuro

# Botón para gestionar productos
btn_productos = ttk.Button(root, text="Gestionar Productos", command=abrir_gestion_productos)
btn_productos.pack(pady=10)

root.mainloop()


