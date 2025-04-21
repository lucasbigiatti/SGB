# Ventanas/producto.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import os
from shutil import copyfile
from PIL import Image, ImageTk
from datetime import datetime

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

class GestionProductos:
    def __init__(self, frame_padre, conexion):
        self.frame_padre = frame_padre
        self.conexion = conexion
        
        # Configurar el frame principal con mejor apariencia
        self.frame_principal = tk.Frame(frame_padre, bg=COLOR_FONDO_PRINCIPAL)
        self.frame_principal.pack(fill="both", expand=True)
        
        # Título con separador
        frame_titulo = tk.Frame(self.frame_principal, bg=COLOR_FONDO_PRINCIPAL)
        frame_titulo.pack(fill="x", pady=(0, 15))
        
        tk.Label(frame_titulo, text="Gestión de Productos", 
                font=("Segoe UI", 18, "bold"), bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_CLARO).pack(pady=(0, 5))
        
        # Separador decorativo
        ttk.Separator(frame_titulo, orient="horizontal").pack(fill="x", pady=(0, 10))
        
        # Layout de dos columnas
        self.panel_izquierdo = tk.Frame(self.frame_principal, bg=COLOR_FONDO_PRINCIPAL)
        self.panel_izquierdo.pack(side=tk.LEFT, fill="both", expand=True, padx=(20, 10), pady=10)
        
        self.panel_derecho = tk.Frame(self.frame_principal, bg=COLOR_FONDO_PRINCIPAL)
        self.panel_derecho.pack(side=tk.RIGHT, fill="both", expand=True, padx=(10, 20), pady=10)
        
        # Panel de formulario
        self.crear_panel_formulario()
        
        # Panel de tabla y filtro
        self.crear_panel_tabla()
        
        # Actualizar tabla con datos iniciales
        self.actualizar_tabla()
        
        # Establecer el foco en el primer campo de entrada
        self.entries[0].focus_set()
    
    def crear_panel_formulario(self):
        """Crea el panel de formulario con mejor estilo"""
        # Título de sección
        tk.Label(self.panel_izquierdo, text="Datos del Producto", 
                font=("Segoe UI", 14, "bold"), bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_CLARO).pack(anchor="w", pady=(0, 10))
        
        # Marco para el formulario con estilo mejorado
        frame_form = tk.Frame(self.panel_izquierdo, bg=COLOR_FONDO_SECUNDARIO, 
                            padx=15, pady=15, bd=1, relief=tk.GROOVE)
        frame_form.pack(fill="both", expand=True)
        
        # Inicializar campos del formulario
        self.inicializar_formulario(frame_form)
        
        # Frame para botones con mejor estilo
        self.frame_botones = tk.Frame(self.panel_izquierdo, bg=COLOR_FONDO_PRINCIPAL)
        self.frame_botones.pack(pady=15, fill="x")
        
        # Botones principales
        ttk.Button(self.frame_botones, text="Agregar Producto", 
                  command=self.agregar_producto, style="Accion.TButton").pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        ttk.Button(self.frame_botones, text="Eliminar", 
                  command=self.eliminar_producto).pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        ttk.Button(self.frame_botones, text="Modificar", 
                  command=self.cargar_datos).pack(side=tk.LEFT, padx=5, fill="x", expand=True)
    
    def crear_panel_tabla(self):
        """Crea el panel de tabla y filtro con mejor estilo"""
        # Título de sección
        tk.Label(self.panel_derecho, text="Inventario de Productos", 
                font=("Segoe UI", 14, "bold"), bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_CLARO).pack(anchor="w", pady=(0, 10))
        
        # Panel de filtro mejorado
        frame_filtro = tk.Frame(self.panel_derecho, bg=COLOR_FONDO_SECUNDARIO, padx=10, pady=5, bd=1, relief=tk.GROOVE)
        frame_filtro.pack(fill="x", pady=(0, 10))
        
        tk.Label(frame_filtro, text="Filtrar por nombre o marca:", 
                bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TEXTO_CLARO).pack(side=tk.LEFT, padx=5)
        
        self.entry_filtro = ttk.Entry(frame_filtro, width=25)
        self.entry_filtro.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_filtro, text="Buscar", 
                  command=self.filtrar_productos).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_filtro, text="Mostrar Todo", 
                  command=self.actualizar_tabla).pack(side=tk.LEFT, padx=5)
        
        # Permitir filtrar al presionar Enter
        self.entry_filtro.bind('<Return>', lambda event: self.filtrar_productos())
        
        # Marco para la tabla con estilo mejorado
        self.frame_tabla = tk.Frame(self.panel_derecho, bg=COLOR_FONDO_SECUNDARIO, 
                                  padx=10, pady=10, bd=1, relief=tk.GROOVE)
        self.frame_tabla.pack(fill="both", expand=True)
        
        # Crear tabla mejorada
        self.crear_tabla()
        
        # Añadir información de estado
        self.label_estado = tk.Label(self.panel_derecho, text="Mostrando todos los productos", 
                                   bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_CLARO, font=("Segoe UI", 8))
        self.label_estado.pack(anchor="w", pady=(5, 0))
        
        # Añadir la fecha actual
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        self.label_fecha = tk.Label(self.panel_derecho, text=f"Fecha actual: {fecha_actual}", 
                                  bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_CLARO, font=("Segoe UI", 8))
        self.label_fecha.pack(anchor="e", pady=(5, 0))
    
    def inicializar_formulario(self, frame_parent):
        """Inicializa los campos del formulario con mejor estilo"""
        # Uso de grid para alinear mejor los elementos
        ancho_etiqueta = 12  # Ancho fijo para etiquetas
        ancho_entrada = 25   # Ancho para entradas
        
        labels = ["Nombre", "Marca", "Precio", "Stock", "Litros"]
        self.entries = []
        
        for i, texto in enumerate(labels):
            tk.Label(frame_parent, text=f"{texto}:", bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TEXTO_CLARO,
                    font=("Segoe UI", 10, "bold"), width=ancho_etiqueta, anchor="w").grid(row=i, column=0, padx=5, pady=8, sticky='w')
            
            entry = ttk.Entry(frame_parent, width=ancho_entrada)
            entry.grid(row=i, column=1, padx=5, pady=8, sticky='ew')
            self.entries.append(entry)
        
        # Sección para la imagen
        frame_imagen = tk.Frame(frame_parent, bg=COLOR_FONDO_SECUNDARIO)
        frame_imagen.grid(row=6, column=0, columnspan=2, pady=10)
        
        tk.Label(frame_imagen, text="Imagen del Producto:", bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TEXTO_CLARO,
                font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))
        
        self.label_imagen = tk.Label(frame_imagen, text="No se ha seleccionado imagen", 
                                   bg=COLOR_ACENTO, fg=COLOR_TEXTO_CLARO, padx=10, pady=5,
                                   font=("Segoe UI", 9), width=40, bd=1, relief=tk.SUNKEN)
        self.label_imagen.pack(fill="x", pady=(0, 10))
        
        # Frame para la previsualización con borde
        frame_preview = tk.Frame(frame_imagen, bg=COLOR_FONDO_SECUNDARIO, bd=2, relief=tk.SUNKEN)
        frame_preview.pack(pady=5)
        
        self.imagen_preview = tk.Label(frame_preview, bg=COLOR_ACENTO, width=20, height=10)
        self.imagen_preview.pack()
        
        # Botón para seleccionar imagen
        ttk.Button(frame_imagen, text="Seleccionar Imagen", 
                  command=self.seleccionar_imagen).pack(pady=10, fill="x")
    
    def crear_tabla(self):
        """Crea la tabla con mejor estilo"""
        columnas = ("ID", "Nombre", "Marca", "Precio", "Stock", "Litros", "Imagen")
        self.tabla_productos = ttk.Treeview(self.frame_tabla, 
                                          columns=columnas, 
                                          show="headings", 
                                          style="Treeview")
        
        # Configurar columnas
        for col in columnas:
            self.tabla_productos.heading(col, text=col)
            # Ajustar ancho de columnas
            if col == "ID":
                self.tabla_productos.column(col, width=50, anchor="center")
            elif col == "Nombre" or col == "Marca":
                self.tabla_productos.column(col, width=150, anchor="w")
            elif col == "Imagen":
                self.tabla_productos.column(col, width=200, anchor="w")
            else:
                self.tabla_productos.column(col, width=80, anchor="center")
        
        # Agregar scrollbars
        scrollbar_y = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla_productos.yview)
        scrollbar_x = ttk.Scrollbar(self.frame_tabla, orient="horizontal", command=self.tabla_productos.xview)
        self.tabla_productos.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Empaquetado con mejor organización
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tabla_productos.pack(side="left", fill="both", expand=True)
        
        # Evento de selección para mostrar detalles al hacer clic
        self.tabla_productos.bind('<<TreeviewSelect>>', self.mostrar_detalles_seleccion)
    
    def mostrar_detalles_seleccion(self, event):
        """Muestra detalles del producto seleccionado en el estado"""
        seleccion = self.tabla_productos.selection()
        if seleccion:
            producto = self.tabla_productos.item(seleccion)['values']
            self.label_estado.config(text=f"Seleccionado: {producto[1]} - {producto[2]}")
    
    def seleccionar_imagen(self):
        """Abre un diálogo para seleccionar una imagen con mejor experiencia de usuario"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar Imagen del Producto",
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("Todos los archivos", "*.*")
            ]
        )
        if archivo:
            self.label_imagen.config(text=archivo)
            self.mostrar_vista_previa(archivo)
    
    def mostrar_vista_previa(self, imagen_path):
        """Muestra una vista previa de la imagen seleccionada"""
        try:
            imagen = Image.open(imagen_path)
            
            # Mantener proporción de aspecto al redimensionar
            width, height = imagen.size
            max_size = 150
            ratio = min(max_size/width, max_size/height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            
            imagen = imagen.resize((new_width, new_height))
            imagen_tk = ImageTk.PhotoImage(imagen)
            self.imagen_preview.config(image=imagen_tk)
            self.imagen_preview.image = imagen_tk
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la vista previa de la imagen: {e}")
    
    def actualizar_tabla(self):
        """Actualiza los datos de la tabla y el estado"""
        # Limpiar tabla
        for row in self.tabla_productos.get_children():
            self.tabla_productos.delete(row)
        
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT id_producto, nombre, marca, precio, stock, litros, imagen FROM Productos")
            productos = cursor.fetchall()
            
            for producto in productos:
                self.tabla_productos.insert("", "end", values=producto)
                
            # Actualizar estado
            self.label_estado.config(text=f"Mostrando todos los productos ({len(productos)} encontrados)")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la tabla: {e}")
    
    def filtrar_productos(self):
        """Filtra productos por nombre o marca con mejor feedback"""
        filtro = self.entry_filtro.get().strip()
        if not filtro:
            self.actualizar_tabla()
            return
            
        # Limpiar tabla
        for row in self.tabla_productos.get_children():
            self.tabla_productos.delete(row)
        
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                SELECT id_producto, nombre, marca, precio, stock, litros, imagen 
                FROM Productos 
                WHERE nombre LIKE %s OR marca LIKE %s
            """, (f"%{filtro}%", f"%{filtro}%"))
            productos = cursor.fetchall()
            
            for producto in productos:
                self.tabla_productos.insert("", "end", values=producto)
                
            # Actualizar estado
            self.label_estado.config(text=f"Mostrando {len(productos)} resultados para '{filtro}'")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo filtrar: {e}")
    
    def agregar_producto(self):
        """Agrega un nuevo producto con mejor validación y feedback"""
        nombre = self.entries[0].get().strip()
        marca = self.entries[1].get().strip()
        precio = self.entries[2].get().strip()
        stock = self.entries[3].get().strip()
        litros = self.entries[4].get().strip()
        imagen_path = self.label_imagen.cget("text")
        
        # Validar campos con mensajes más específicos
        if not nombre or not marca:
            messagebox.showerror("Error", "Los campos Nombre y Marca son obligatorios")
            return
            
        if not precio or not precio.replace('.', '', 1).isdigit():
            messagebox.showerror("Error", "Debe ingresar un precio válido")
            return
            
        if not stock or not stock.isdigit():
            messagebox.showerror("Error", "Debe ingresar una cantidad de stock válida")
            return
            
        if not litros or not litros.replace('.', '', 1).isdigit():
            messagebox.showerror("Error", "Debe ingresar una cantidad de litros válida")
            return
            
        if imagen_path == "No se ha seleccionado imagen":
            messagebox.showerror("Error", "Debe seleccionar una imagen para el producto")
            return
        
        # Guardar imagen con mejor manejo de errores
        imagen_destino = os.path.join("imagenes", os.path.basename(imagen_path))
        try:
            if not os.path.exists("imagenes"):
                os.makedirs("imagenes")
            copyfile(imagen_path, imagen_destino)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la imagen: {e}")
            return
        
        # Guardar producto en la base de datos
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                INSERT INTO Productos (nombre, marca, precio, stock, litros, imagen) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nombre, marca, precio, stock, litros, imagen_destino))
            self.conexion.commit()
            
            # Mostrar confirmación visual
            frame_confirmacion = tk.Frame(self.frame_principal, bg=COLOR_ACENTO, bd=2, relief=tk.RAISED,
                                       padx=20, pady=20)
            frame_confirmacion.place(relx=0.5, rely=0.5, anchor="center")
            
            tk.Label(frame_confirmacion, text="¡Producto Agregado con Éxito!",
                   font=("Segoe UI", 14, "bold"), bg=COLOR_ACENTO, fg=COLOR_TEXTO_CLARO).pack(pady=(0, 15))
                   
            tk.Label(frame_confirmacion, text=f"{nombre} - {marca}",
                   font=("Segoe UI", 12), bg=COLOR_ACENTO, fg=COLOR_TEXTO_CLARO).pack(pady=2)
                   
            tk.Label(frame_confirmacion, text=f"Precio: ${precio}",
                   font=("Segoe UI", 12), bg=COLOR_ACENTO, fg=COLOR_TEXTO_CLARO).pack(pady=2)
                   
            # Botón para cerrar la confirmación
            ttk.Button(frame_confirmacion, text="Aceptar", 
                     command=lambda: frame_confirmacion.destroy()).pack(pady=15)
            
            # Limpiar formulario
            self.limpiar_campos()
            
            # Actualizar tabla
            self.actualizar_tabla()
            
            # Volver a enfocar el primer campo
            self.entries[0].focus_set()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el producto: {e}")
    
    def eliminar_producto(self):
        """Elimina el producto seleccionado con confirmación mejorada"""
        seleccion = self.tabla_productos.selection()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona un producto para eliminar")
            return
        
        producto = self.tabla_productos.item(seleccion)['values']
        
        # Confirmar eliminación con mejor interfaz
        frame_confirmar = tk.Frame(self.frame_principal, bg=COLOR_FONDO_SECUNDARIO, bd=2, relief=tk.RAISED,
                                padx=20, pady=20)
        frame_confirmar.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(frame_confirmar, text="¿Eliminar este producto?",
               font=("Segoe UI", 14, "bold"), bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TEXTO_CLARO).pack(pady=(0, 15))
               
        tk.Label(frame_confirmar, text=f"{producto[1]} - {producto[2]}",
               font=("Segoe UI", 12), bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_RESALTE).pack(pady=2)
               
        tk.Label(frame_confirmar, text=f"Precio: ${producto[3]} | Stock: {producto[4]}",
               font=("Segoe UI", 12), bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TEXTO_CLARO).pack(pady=2)
               
        frame_botones_confirm = tk.Frame(frame_confirmar, bg=COLOR_FONDO_SECUNDARIO)
        frame_botones_confirm.pack(pady=15)
        
        # Botones de confirmación
        ttk.Button(frame_botones_confirm, text="Sí, Eliminar", 
                 command=lambda: self.confirmar_eliminacion(producto[0], frame_confirmar)).pack(side=tk.LEFT, padx=10)
                 
        ttk.Button(frame_botones_confirm, text="Cancelar", 
                 command=lambda: frame_confirmar.destroy()).pack(side=tk.LEFT, padx=10)
    
    def confirmar_eliminacion(self, producto_id, frame_confirmar):
        """Procesa la eliminación después de confirmar"""
        frame_confirmar.destroy()
        
        try:
            cursor = self.conexion.cursor()
            cursor.execute("DELETE FROM Productos WHERE id_producto = %s", (producto_id,))
            self.conexion.commit()
            
            # Mostrar confirmación de eliminación
            self.label_estado.config(text="Producto eliminado correctamente")
            
            # Actualizar tabla
            self.actualizar_tabla()
            
            # Volver a enfocar el primer campo
            self.entries[0].focus_set()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el producto: {e}")
    
    def cargar_datos(self):
        """Carga los datos del producto seleccionado en el formulario"""
        seleccion = self.tabla_productos.selection()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona un producto para modificar")
            return
        
        producto = self.tabla_productos.item(seleccion)['values']
        
        # Limpiar campos
        self.limpiar_campos()
        
        # Cargar datos en formulario
        self.entries[0].insert(0, producto[1])  # Nombre
        self.entries[1].insert(0, producto[2])  # Marca
        self.entries[2].insert(0, producto[3])  # Precio
        self.entries[3].insert(0, producto[4])  # Stock
        self.entries[4].insert(0, producto[5])  # Litros
        
        self.label_imagen.config(text=producto[6])  # Ruta imagen
        self.mostrar_vista_previa(producto[6])
        
        # Cambiar botones con mejor estilo
        for widget in self.frame_botones.winfo_children():
            widget.destroy()
        
        ttk.Button(self.frame_botones, text="Guardar Cambios", 
                  command=self.modificar_producto, style="Accion.TButton").pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        ttk.Button(self.frame_botones, text="Cancelar", 
                  command=self.cancelar_modificacion).pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        # Actualizar estado
        self.label_estado.config(text=f"Editando: {producto[1]}")
        
        # Enfocar el primer campo
        self.entries[0].focus_set()
    
    def modificar_producto(self):
        """Modifica el producto seleccionado con mejor validación y feedback"""
        seleccion = self.tabla_productos.selection()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona un producto para modificar")
            return
        
        producto_id = self.tabla_productos.item(seleccion)['values'][0]
        nombre = self.entries[0].get().strip()
        marca = self.entries[1].get().strip()
        precio = self.entries[2].get().strip()
        stock = self.entries[3].get().strip()
        litros = self.entries[4].get().strip()
        imagen_path = self.label_imagen.cget("text")
        
        # Validar campos con mensajes más específicos
        if not nombre or not marca:
            messagebox.showerror("Error", "Los campos Nombre y Marca son obligatorios")
            return
            
        if not precio or not precio.replace('.', '', 1).isdigit():
            messagebox.showerror("Error", "Debe ingresar un precio válido")
            return
            
        if not stock or not stock.isdigit():
            messagebox.showerror("Error", "Debe ingresar una cantidad de stock válida")
            return
            
        if not litros or not litros.replace('.', '', 1).isdigit():
            messagebox.showerror("Error", "Debe ingresar una cantidad de litros válida")
            return
        
        # Verificar si se cambió la imagen
        if imagen_path != "No se ha seleccionado imagen" and not imagen_path.startswith("imagenes"):
            imagen_destino = os.path.join("imagenes", os.path.basename(imagen_path))
            try:
                if not os.path.exists("imagenes"):
                    os.makedirs("imagenes")
                copyfile(imagen_path, imagen_destino)
                imagen_path = imagen_destino
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar la imagen: {e}")
                return
        
        # Actualizar producto en la base de datos
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                UPDATE Productos 
                SET nombre=%s, marca=%s, precio=%s, stock=%s, litros=%s, imagen=%s 
                WHERE id_producto=%s
            """, (nombre, marca, precio, stock, litros, imagen_path, producto_id))
            self.conexion.commit()
            
            # Mostrar confirmación visual
            frame_confirmacion = tk.Frame(self.frame_principal, bg=COLOR_ACENTO, bd=2, relief=tk.RAISED,
                                       padx=20, pady=20)
            frame_confirmacion.place(relx=0.5, rely=0.5, anchor="center")
            
            tk.Label(frame_confirmacion, text="¡Producto Modificado con Éxito!",
                   font=("Segoe UI", 14, "bold"), bg=COLOR_ACENTO, fg=COLOR_TEXTO_CLARO).pack(pady=(0, 15))
                   
            tk.Label(frame_confirmacion, text=f"{nombre} - {marca}",
                   font=("Segoe UI", 12), bg=COLOR_ACENTO, fg=COLOR_TEXTO_CLARO).pack(pady=2)
                   
            # Botón para cerrar la confirmación
            ttk.Button(frame_confirmacion, text="Aceptar", 
                     command=lambda: frame_confirmacion.destroy()).pack(pady=15)
            
            # Restaurar botones originales
            self.cancelar_modificacion()
            
            # Actualizar tabla
            self.actualizar_tabla()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar el producto: {e}")
    
    def cancelar_modificacion(self):
        """Cancela la modificación y restaura los botones originales"""
        # Limpiar campos
        self.limpiar_campos()
        
        # Restaurar botones originales
        for widget in self.frame_botones.winfo_children():
            widget.destroy()
        
        ttk.Button(self.frame_botones, text="Agregar Producto", 
                  command=self.agregar_producto, style="Accion.TButton").pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        ttk.Button(self.frame_botones, text="Eliminar", 
                  command=self.eliminar_producto).pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        ttk.Button(self.frame_botones, text="Modificar", 
                  command=self.cargar_datos).pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        # Actualizar estado
        self.label_estado.config(text="Mostrando todos los productos")
        
        # Volver a enfocar el primer campo
        self.entries[0].focus_set()
    
    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        for entry in self.entries:
            entry.delete(0, tk.END)
        
        self.label_imagen.config(text="No se ha seleccionado imagen")
        self.imagen_preview.config(image="")

# Función de compatibilidad para código antiguo
def abrir_gestion_productos():
    import mysql.connector
    
    ventana = tk.Toplevel()
    ventana.title("Gestión de Productos")
    ventana.geometry("900x700")
    ventana.configure(bg=COLOR_FONDO_PRINCIPAL)
    
    # Conectar a la base de datos
    conexion = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="gestionbebidas"
    )
    
    # Inicializar gestión de productos
    GestionProductos(ventana, conexion)