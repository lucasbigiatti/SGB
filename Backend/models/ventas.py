# Ventanas/ventas.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
from datetime import datetime
import os

# Colores personalizados
COLOR_FONDO_PRINCIPAL = "#1A1A2E"  # Azul muy oscuro para el fondo principal
COLOR_FONDO_SECUNDARIO = "#16213E"  # Azul oscuro para paneles secundarios
COLOR_ACENTO = "#0F3460"  # Azul medio para bordes y énfasis
COLOR_RESALTE = "#E94560"  # Rojo/rosa para botones importantes y acentos
COLOR_TEXTO_CLARO = "#FFFFFF"  # Blanco para texto sobre fondos oscuros
COLOR_TEXTO_OSCURO = "#1A1A2E"  # Color oscuro para texto sobre fondos claros
COLOR_BOTON = "#0F3460"  # Color para botones normales
COLOR_BOTON_HOVER = "#E94560"  # Color para botones al pasar el mouse
COLOR_BORDES = "#533483"  # Color para bordes de marcos y separadores

class GestionVentas:
    def __init__(self, frame_padre, conexion):
        self.frame_padre = frame_padre
        self.conexion = conexion
        self.lista_productos = []  # Lista para el carrito
        
        # Configurar el frame principal con mejor apariencia
        self.frame_principal = tk.Frame(frame_padre, bg=COLOR_FONDO_PRINCIPAL)
        self.frame_principal.pack(fill="both", expand=True)
        
        # Título con separador
        frame_titulo = tk.Frame(self.frame_principal, bg=COLOR_FONDO_PRINCIPAL)
        frame_titulo.pack(fill="x", pady=(0, 15))
        
        tk.Label(frame_titulo, text="Gestión de Ventas", 
                font=("Segoe UI", 18, "bold"), bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_CLARO).pack(pady=(0, 5))
        
        # Separador decorativo
        ttk.Separator(frame_titulo, orient="horizontal").pack(fill="x", pady=(0, 10))
        
        # Crear frame superior para datos de cliente con mejor estilo
        self.crear_frame_superior()
        
        # Separador entre formulario y productos
        ttk.Separator(self.frame_principal, orient="horizontal").pack(fill="x", pady=10)
        
        # Frame para resumen del carrito
        self.frame_carrito = tk.Frame(self.frame_principal, bg=COLOR_FONDO_SECUNDARIO, padx=15, pady=10, bd=1, relief=tk.GROOVE)
        self.frame_carrito.pack(side=tk.RIGHT, fill="y", padx=15, pady=10)
        
        # Título del carrito
        tk.Label(self.frame_carrito, text="Carrito de Compras", 
                font=("Segoe UI", 12, "bold"), bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TEXTO_CLARO).pack(pady=(0, 10))
        
        # Área de texto para mostrar productos en el carrito
        self.texto_carrito = scrolledtext.ScrolledText(self.frame_carrito, width=30, height=15, 
                                                    bg=COLOR_ACENTO, fg=COLOR_TEXTO_CLARO,
                                                    font=("Segoe UI", 10))
        self.texto_carrito.pack(pady=5, fill="both", expand=True)
        
        # Etiqueta para total con estilo destacado
        self.label_total = tk.Label(self.frame_carrito, text="Total: $0.00", 
                                  font=("Segoe UI", 14, "bold"), bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_RESALTE)
        self.label_total.pack(pady=10)
        
        # Botón para registrar venta con estilo destacado
        ttk.Button(self.frame_carrito, text="Registrar Venta", 
                  command=self.registrar_venta, style="Accion.TButton").pack(pady=10, fill="x")
        
        # Crear frame para catálogo de productos
        frame_catalogo = tk.Frame(self.frame_principal, bg=COLOR_FONDO_PRINCIPAL)
        frame_catalogo.pack(side=tk.LEFT, fill="both", expand=True, padx=15, pady=10)
        
        # Título de productos disponibles
        tk.Label(frame_catalogo, text="Productos Disponibles", 
                font=("Segoe UI", 14, "bold"), bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_CLARO).pack(pady=(0, 10))
        
        # Crear frame para productos con scroll (usando Canvas)
        self.canvas_productos = tk.Canvas(frame_catalogo, bg=COLOR_FONDO_PRINCIPAL, highlightthickness=0)
        self.canvas_productos.pack(side=tk.LEFT, fill="both", expand=True)
        
        # Scrollbar para el canvas
        scrollbar = ttk.Scrollbar(frame_catalogo, orient="vertical", command=self.canvas_productos.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.canvas_productos.configure(yscrollcommand=scrollbar.set)
        
        # Frame dentro del canvas para los productos
        self.frame_productos = tk.Frame(self.canvas_productos, bg=COLOR_FONDO_PRINCIPAL)
        self.canvas_productos.create_window((0, 0), window=self.frame_productos, anchor="nw")
        
        # Configurar el canvas para hacer scroll
        self.frame_productos.bind("<Configure>", lambda e: self.canvas_productos.configure(
            scrollregion=self.canvas_productos.bbox("all"),
            width=frame_catalogo.winfo_width() - scrollbar.winfo_width()
        ))
        
        # Cargar productos
        self.cargar_productos()
        
        # Establecer el foco en el campo de cliente
        self.entry_cliente.focus_set()
    
    def crear_frame_superior(self):
        """Crea el frame superior con datos del cliente y método de pago"""
        frame_superior = tk.Frame(self.frame_principal, bg=COLOR_FONDO_SECUNDARIO, padx=15, pady=15, bd=1, relief=tk.GROOVE)
        frame_superior.pack(pady=10, padx=20, fill="x")
        
        # Título de sección
        tk.Label(frame_superior, text="Datos de la Venta", 
                font=("Segoe UI", 12, "bold"), bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TEXTO_CLARO).pack(pady=(0, 10))
        
        # Frame para formulario
        frame_form = tk.Frame(frame_superior, bg=COLOR_FONDO_SECUNDARIO)
        frame_form.pack(fill="x")
        
        # Cliente - mejor organizado
        frame_cliente = tk.Frame(frame_form, bg=COLOR_FONDO_SECUNDARIO)
        frame_cliente.pack(fill="x", pady=5)
        
        tk.Label(frame_cliente, text="Cliente:", bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TEXTO_CLARO,
                font=("Segoe UI", 10, "bold"), width=15, anchor="w").pack(side=tk.LEFT, padx=5)
        
        self.entry_cliente = ttk.Entry(frame_cliente, font=("Segoe UI", 10), width=30)
        self.entry_cliente.pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        # Método de pago - mejor organizado
        frame_metodo = tk.Frame(frame_form, bg=COLOR_FONDO_SECUNDARIO)
        frame_metodo.pack(fill="x", pady=5)
        
        tk.Label(frame_metodo, text="Método de Pago:", bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TEXTO_CLARO,
                font=("Segoe UI", 10, "bold"), width=15, anchor="w").pack(side=tk.LEFT, padx=5)
        
        self.metodo_pago = ttk.Combobox(frame_metodo, values=["Efectivo", "Tarjeta", "Transferencia"], 
                                      font=("Segoe UI", 10), width=20)
        self.metodo_pago.pack(side=tk.LEFT, padx=5)
        
        # Variable para el checkbox de descuento
        self.descuento_var = tk.BooleanVar(value=False)
        
        # Checkbox para activar/desactivar el descuento - con mejor estilo
        frame_descuento = tk.Frame(frame_form, bg=COLOR_FONDO_SECUNDARIO)
        frame_descuento.pack(fill="x", pady=5)
        
        ttk.Checkbutton(frame_descuento, text="Aplicar Descuento por Efectivo (10%)", 
                      variable=self.descuento_var, style="TCheckbutton").pack(padx=5)
        
        # Mensaje informativo sobre el descuento
        tk.Label(frame_superior, text="El descuento del 10% se aplica automáticamente para pagos en efectivo", 
                font=("Segoe UI", 8), bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_RESALTE).pack(pady=(5, 0))
        
        # Vincular eventos
        self.metodo_pago.bind("<<ComboboxSelected>>", lambda e: self.aplicar_descuento())
        self.descuento_var.trace_add("write", lambda *args: self.aplicar_descuento())
    
    def cargar_productos(self):
        """Carga los productos desde la base de datos y los muestra en la interfaz"""
        # Limpiar los productos anteriores
        for widget in self.frame_productos.winfo_children():
            widget.destroy()
        
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT id_producto, nombre, precio, imagen FROM Productos")
            productos = cursor.fetchall()
            
            # Crear un grid para mostrar productos
            row, col = 0, 0
            max_cols = 3  # Número de columnas para mostrar productos
            
            for producto in productos:
                id_producto, nombre, precio, imagen_path = producto
                
                # Crear un frame para el producto con estilo mejorado
                frame_card = tk.Frame(self.frame_productos, bg=COLOR_FONDO_SECUNDARIO, 
                                    bd=1, relief=tk.RAISED, padx=10, pady=10, width=150, height=220)
                frame_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
                frame_card.grid_propagate(False)  # Mantener tamaño fijo
                
                # Cargar la imagen del producto
                try:
                    img = Image.open(imagen_path)
                    img = img.resize((120, 120), Image.Resampling.LANCZOS)
                    img = ImageTk.PhotoImage(img)
                except:
                    img = Image.new("RGB", (120, 120), (30, 30, 50))
                    img = ImageTk.PhotoImage(img)
                
                # Contendor de la imagen con borde
                frame_img = tk.Frame(frame_card, bg=COLOR_FONDO_SECUNDARIO, bd=1, relief=tk.SUNKEN)
                frame_img.pack(pady=(0, 8))
                
                label_img = tk.Label(frame_img, image=img, bg=COLOR_FONDO_SECUNDARIO)
                label_img.image = img  # Necesario para evitar que la imagen se pierda
                label_img.pack()
                
                # Nombre del producto
                label_nombre = tk.Label(frame_card, text=nombre, bg=COLOR_FONDO_SECUNDARIO, 
                                      fg=COLOR_TEXTO_CLARO, font=("Segoe UI", 10, "bold"),
                                      wraplength=130, justify="center")
                label_nombre.pack(fill="x")
                
                # Precio del producto
                label_precio = tk.Label(frame_card, text=f"${precio}", bg=COLOR_FONDO_SECUNDARIO, 
                                      fg=COLOR_RESALTE, font=("Segoe UI", 12, "bold"))
                label_precio.pack(pady=2)
                
                # Botón para agregar al carrito con mejor estilo
                btn_agregar = ttk.Button(frame_card, text="Agregar", 
                                       command=lambda p=producto: self.agregar_al_carrito(p))
                btn_agregar.pack(pady=5, fill="x")
                
                # Avanzar a la siguiente columna o fila
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
                    
            # Asegurar que el frame tiene el tamaño correcto para el scroll
            self.frame_productos.update_idletasks()
            self.canvas_productos.config(scrollregion=self.canvas_productos.bbox("all"))
            
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
        
        # Actualizar carrito y total
        self.actualizar_carrito()
        self.actualizar_total()
        
        # Mostrar confirmación discreta
        flash_label = tk.Label(self.frame_principal, text=f"¡{nombre} agregado al carrito!", 
                             font=("Segoe UI", 10), bg=COLOR_ACENTO, fg=COLOR_TEXTO_CLARO,
                             padx=10, pady=5, bd=1, relief=tk.RAISED)
        flash_label.place(relx=0.5, rely=0.9, anchor="center")
        # Auto-destruir después de 2 segundos
        self.frame_principal.after(2000, flash_label.destroy)
    
    def actualizar_carrito(self):
        """Actualiza la visualización del carrito"""
        self.texto_carrito.config(state=tk.NORMAL)
        self.texto_carrito.delete(1.0, tk.END)
        
        if not self.lista_productos:
            self.texto_carrito.insert(tk.END, "El carrito está vacío")
        else:
            # Encabezado
            self.texto_carrito.insert(tk.END, "PRODUCTOS SELECCIONADOS\n", "titulo")
            self.texto_carrito.insert(tk.END, "-" * 30 + "\n\n", "separador")
            
            # Configurar etiquetas para el texto
            self.texto_carrito.tag_configure("titulo", font=("Segoe UI", 10, "bold"), foreground=COLOR_TEXTO_CLARO)
            self.texto_carrito.tag_configure("separador", foreground=COLOR_TEXTO_CLARO)
            self.texto_carrito.tag_configure("producto", font=("Segoe UI", 9), foreground=COLOR_TEXTO_CLARO)
            self.texto_carrito.tag_configure("cantidad", font=("Segoe UI", 9, "bold"), foreground=COLOR_RESALTE)
            
            # Mostrar cada producto
            for item in self.lista_productos:
                self.texto_carrito.insert(tk.END, f"{item['nombre']}\n", "producto")
                self.texto_carrito.insert(tk.END, f"Cantidad: ", "producto")
                self.texto_carrito.insert(tk.END, f"{item['cantidad']}", "cantidad")
                self.texto_carrito.insert(tk.END, f" x ${item['precio']}\n\n", "producto")
        
        self.texto_carrito.config(state=tk.DISABLED)
    
    def aplicar_descuento(self):
        """Aplica un descuento del 10% si el método de pago es en efectivo y el checkbox está activado"""
        self.actualizar_total()
    
    def actualizar_total(self):
        """Calcula el total y actualiza la etiqueta con o sin descuento"""
        if not self.lista_productos:
            self.label_total.config(text="Total: $0.00")
            return
            
        total = sum(float(item["precio"]) * item["cantidad"] for item in self.lista_productos)
        
        # Aplicar descuento si corresponde
        if self.metodo_pago.get() == "Efectivo" and self.descuento_var.get():
            descuento = total * 0.1
            total *= 0.9  # Aplica el 10% de descuento
            self.label_total.config(text=f"Total: ${total:.2f}\nDescuento: ${descuento:.2f}")
        else:
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
            
            # Mostrar confirmación visual
            frame_confirmacion = tk.Frame(self.frame_principal, bg=COLOR_ACENTO, bd=2, relief=tk.RAISED,
                                       padx=20, pady=20)
            frame_confirmacion.place(relx=0.5, rely=0.5, anchor="center")
            
            tk.Label(frame_confirmacion, text="¡Venta Registrada con Éxito!",
                   font=("Segoe UI", 16, "bold"), bg=COLOR_ACENTO, fg=COLOR_TEXTO_CLARO).pack(pady=(0, 15))
                   
            tk.Label(frame_confirmacion, text=f"Total: ${total:.2f}",
                   font=("Segoe UI", 14), bg=COLOR_ACENTO, fg=COLOR_TEXTO_CLARO).pack(pady=5)
                   
            tk.Label(frame_confirmacion, text=f"Cliente: {cliente}",
                   font=("Segoe UI", 12), bg=COLOR_ACENTO, fg=COLOR_TEXTO_CLARO).pack(pady=5)
                   
            tk.Label(frame_confirmacion, text=f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                   font=("Segoe UI", 12), bg=COLOR_ACENTO, fg=COLOR_TEXTO_CLARO).pack(pady=5)
            
            # Botón para cerrar la confirmación
            ttk.Button(frame_confirmacion, text="Aceptar", 
                      command=lambda: (frame_confirmacion.destroy(), self.limpiar_venta())).pack(pady=15)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la venta: {e}")
    
    def limpiar_venta(self):
        """Limpia los campos después de una venta exitosa"""
        self.lista_productos.clear()
        self.actualizar_carrito()
        self.actualizar_total()
        self.entry_cliente.delete(0, tk.END)
        self.metodo_pago.set("")
        self.descuento_var.set(False)
        
        # Volver a enfocar el campo de cliente después de completar la venta
        self.entry_cliente.focus_set()

# Función de compatibilidad para código antiguo (no se usará con la nueva estructura)
def abrir_gestion_ventas():
    import mysql.connector
    
    ventana = tk.Toplevel()
    ventana.title("Gestión de Ventas")
    ventana.geometry("900x600")
    ventana.configure(bg=COLOR_FONDO_PRINCIPAL)
    
    # Conectar a la base de datos
    conexion = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="gestionbebidas"
    )
    
    # Inicializar gestión de ventas
    GestionVentas(ventana, conexion)