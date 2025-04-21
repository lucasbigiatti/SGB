import tkinter as tk
from tkinter import ttk, messagebox

def abrir_ventana():
    ventana = tk.Toplevel()
    ventana.title("Ventana Secundaria")
    ventana.geometry("400x300")
    
    # Botón "Volver"
    boton_volver = tk.Button(ventana, text="← Volver", font=("Segoe UI", 10, "bold"), bg="#7289DA", fg="white",
                             command=ventana.destroy)
    boton_volver.pack(padx=10, pady=10, anchor="nw")  # Arriba a la izquierda



def abrir_gestion_clientes():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Clientes")
    ventana.geometry("500x400")
    ventana.configure(bg="#2C2F33")

    tk.Label(ventana, text="Gestión de Clientes", font=("Segoe UI", 16, "bold"), bg="#2C2F33", fg="#FFFFFF").pack(pady=10)
    ttk.Button(ventana, text="Agregar Cliente", command=lambda: messagebox.showinfo("Clientes", "Agregar Cliente")) .pack(pady=5)
    ttk.Button(ventana, text="Editar Cliente", command=lambda: messagebox.showinfo("Clientes", "Editar Cliente")) .pack(pady=5)
    ttk.Button(ventana, text="Eliminar Cliente", command=lambda: messagebox.showinfo("Clientes", "Eliminar Cliente")) .pack(pady=5)