# Ventanas/ventas.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime
import os

# Colores personalizados
COLOR_FONDO = "#2C2F33"
COLOR_BOTON = "#7289DA"
COLOR_TEXTO = "#FFFFFF"
COLOR_BOTON_HOVER = "#99AAB5"

class GestionVentas:
    def __init__(self, frame_padre, conexion):
        self.frame_padre = frame_padre
        self.conexion = conexion
        self.lista_productos = []  # Lista para el carrito
        
        # Configurar el frame principal
        self.frame_principal = tk.Frame(frame_padre, bg=COLOR_FONDO)
        self.frame_principal.pack(fill="both", expand=True)
        
        # Título
        tk.Label(self.frame_principal, text="Gestión de Ventas", 
                font=("Segoe UI", 16, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=10)
        
        # Crear frame superior para datos de cliente
        self.crear_frame_superior()
        
        # Crear frame para productos
        self.frame_productos = tk.Frame(self.frame_principal, bg=COLOR_FONDO)
        self.frame_productos.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Etiqueta para total
        self.label_total = tk.Label(self.frame_principal, text="Total: $0.00", 
                                  font=("Segoe UI", 14, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO)
        self.label_total.pack(pady=5)
        
        # Cargar productos
        self.cargar_productos()
        
        # Botón para registrar venta
        ttk.Button(self.frame_principal, text="Registrar Venta", 
                  command=self.registrar_venta).pack(pady=10)
        
        # Establecer el foco en el campo de cliente
        self.entry_cliente.focus_set()
    
    def crear_frame_superior(self):
        """Crea el frame superior con datos del cliente y método de pago"""
        frame_superior = tk.Frame(self.frame_principal, bg=COLOR_FONDO)
        frame_superior.pack(pady=10, padx=20, fill="x")
        
        tk.Label(frame_superior, text="Cliente:", bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_cliente = ttk.Entry(frame_superior, font=("Arial", 12))
        self.entry_cliente.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_superior, text="Método de Pago:", bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.metodo_pago = ttk.Combobox(frame_superior, values=["Efectivo", "Tarjeta", "Transferencia"], font=("Arial", 12))
        self.metodo_pago.grid(row=1, column=1, padx=5, pady=5)
        
        # Variable para el checkbox de descuento
        self.descuento_var = tk.BooleanVar(value=False)
        
        # Checkbox para activar/desactivar el descuento
        chk_descuento = ttk.Checkbutton(frame_superior, text="Aplicar Descuento", variable=self.descuento_var)
        chk_descuento.grid(row=1, column=2, padx=5, pady=5)
        
        # Vincular eventos
        self.metodo_pago.bind("<<ComboboxSelected>>", lambda e: self.aplicar_descuento())
        chk_descuento.config(command=self.aplicar_descuento)
    
    def cargar_productos(self):
        """Carga los productos desde la base de datos y los muestra en la interfaz"""
        # Limpiar los productos anteriores
        for widget in self.frame_productos.winfo_children():
            widget.destroy()
        
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT id_producto, nombre, precio, imagen FROM Productos")
            productos = cursor.fetchall()
            
            for producto in productos:
                id_producto, nombre, precio, imagen_path = producto
                
                # Crear un frame para el producto
                frame_card = tk.Frame(self.frame_productos, bg="#2E2E2E", bd=2, relief="ridge")
                frame_card.pack(side="left", padx=10, pady=5)
                
                # Cargar la imagen del producto
                try:
                    img = Image.open(imagen_path)
                    img = img.resize((100, 100), Image.Resampling.LANCZOS)
                    img = ImageTk.PhotoImage(img)
                except:
                    img = Image.new("RGB", (100, 100), (255, 255, 255))
                    img = ImageTk.PhotoImage(img)
                
                label_img = tk.Label(frame_card, image=img, bg="#2E2E2E")
                label_img.image = img  # Necesario para evitar que la imagen se pierda
                label_img.pack(pady=5)
                
                # Nombre del producto
                label_nombre = tk.Label(frame_card, text=nombre, bg="#2E2E2E", fg="white", font=("Arial", 10))
                label_nombre.pack()
                
                # Precio del producto
                label_precio = tk.Label(frame_card, text=f"${precio}", bg="#2E2E2E", fg="lightgreen", font=("Arial", 10, "bold"))
                label_precio.pack()
                
                # Botón para agregar al carrito
                btn_agregar = ttk.Button(frame_card, text="Agregar", 
                                       command=lambda p=producto: self.agregar_al_carrito(p))
                btn_agregar.pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los productos: {e}")
    
    def agregar_al_carrito(self, producto):
        """Agrega un producto al carrito de compras"""
        id_producto, nombre, precio, _ = producto
        encontrado = False
        
        # Verificar si el producto ya está en el carrito
        for item in self.lista_productos:
            if item["id"] == id_producto:
                item["cantidad"] += 1
                encontrado = True
                break
        
        if not encontrado:
            self.lista_productos.append({"id": id_producto, "nombre": nombre, "precio": precio, "cantidad": 1})
        
        self.actualizar_total()
    
    def aplicar_descuento(self):
        """Aplica un descuento del 10% si el método de pago es en efectivo y el checkbox está activado"""
        self.actualizar_total()
    
    def actualizar_total(self):
        """Calcula el total y actualiza la etiqueta con o sin descuento"""
        total = sum(float(item["precio"]) * item["cantidad"] for item in self.lista_productos)
        
        # Aplicar descuento si corresponde
        if self.metodo_pago.get() == "Efectivo" and self.descuento_var.get():
            total *= 0.9  # Aplica el 10% de descuento
        
        self.label_total.config(text=f"Total: ${total:.2f}")
    
    def registrar_venta(self):
        """Registra la venta en la base de datos"""
        cliente = self.entry_cliente.get().strip()
        metodo_pago = self.metodo_pago.get()
        
        if not cliente or not metodo_pago or not self.lista_productos:
            messagebox.showerror("Error", "Todos los campos son obligatorios y debe haber al menos un producto seleccionado.")
            return
        
        # Calcular el total y el descuento
        total = sum(float(item["precio"]) * item["cantidad"] for item in self.lista_productos)
        descuento = 0.0
        
        if metodo_pago == "Efectivo" and self.descuento_var.get():
            descuento = total * 0.1  # 10% de descuento
            total *= 0.9  # Aplica descuento
        
        # Generar el pedido como texto concatenado
        pedido_cliente = ", ".join(f"{item['cantidad']} {item['nombre']}" for item in self.lista_productos)
        
        try:
            cursor = self.conexion.cursor()
            
            # Verificar si el cliente ya existe en la base de datos
            cursor.execute("SELECT id_cliente FROM Clientes WHERE nombre = %s", (cliente,))
            resultado = cursor.fetchone()
            
            if not resultado:
                cursor.execute("INSERT INTO Clientes (nombre) VALUES (%s)", (cliente,))
                self.conexion.commit()
                id_cliente = cursor.lastrowid
            else:
                id_cliente = resultado[0]
            
            fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("""
                INSERT INTO Ventas (id_cliente, fecha, total, metodo_pago, descuento_eft, pedido_cliente)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (id_cliente, fecha, total, metodo_pago, descuento if metodo_pago == "Efectivo" and self.descuento_var.get() else None, pedido_cliente))
            
            id_venta = cursor.lastrowid
            
            # Insertar los productos vendidos
            for item in self.lista_productos:
                cursor.execute("""
                    INSERT INTO Detalle_Ventas (id_venta, id_producto, cantidad, precio_unitario)
                    VALUES (%s, %s, %s, %s)
                """, (id_venta, item["id"], item["cantidad"], float(item["precio"])))
            
            self.conexion.commit()
            
            # Mostrar mensaje de éxito y limpiar el carrito
            messagebox.showinfo("Éxito", "Venta registrada correctamente.")
            self.lista_productos.clear()
            self.actualizar_total()
            self.entry_cliente.delete(0, tk.END)
            self.metodo_pago.set("")
            self.descuento_var.set(False)
            
            # Volver a enfocar el campo de cliente después de completar la venta
            self.entry_cliente.focus_set()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la venta: {e}")

# Función de compatibilidad para código antiguo (no se usará con la nueva estructura)
def abrir_gestion_ventas():
    import mysql.connector
    
    ventana = tk.Toplevel()
    ventana.title("Gestión de Ventas")
    ventana.geometry("900x600")
    ventana.configure(bg="#1E1E1E")
    
    # Conectar a la base de datos
    conexion = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="gestionbebidas"
    )
    
    # Inicializar gestión de ventas
    GestionVentas(ventana, conexion)