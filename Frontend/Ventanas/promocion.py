# Ventanas/promocion.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry  # Si está disponible, facilita la entrada de fechas

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

class GestionPromociones:
    def __init__(self, frame_padre, conexion):
        self.frame_padre = frame_padre
        self.conexion = conexion
        
        # Configurar el frame principal con mejor apariencia
        self.frame_principal = tk.Frame(frame_padre, bg=COLOR_FONDO_PRINCIPAL)
        self.frame_principal.pack(fill="both", expand=True)
        
        # Título con separador
        frame_titulo = tk.Frame(self.frame_principal, bg=COLOR_FONDO_PRINCIPAL)
        frame_titulo.pack(fill="x", pady=(0, 15))
        
        tk.Label(frame_titulo, text="Gestión de Promociones", 
                font=("Segoe UI", 18, "bold"), bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_CLARO).pack(pady=(0, 5))
        
        # Separador decorativo
        ttk.Separator(frame_titulo, orient="horizontal").pack(fill="x", pady=(0, 10))
        
        # Layout de dos columnas
        self.panel_izquierdo = tk.Frame(self.frame_principal, bg=COLOR_FONDO_PRINCIPAL)
        self.panel_izquierdo.pack(side=tk.LEFT, fill="both", expand=True, padx=(20, 10), pady=10)
        
        self.panel_derecho = tk.Frame(self.frame_principal, bg=COLOR_FONDO_PRINCIPAL)
        self.panel_derecho.pack(side=tk.RIGHT, fill="both", expand=True, padx=(10, 20), pady=10)
        
        # Frame para formulario con estilo mejorado
        self.crear_formulario()
        
        # Frame para tabla con estilo mejorado
        self.crear_vista_tabla()
        
        # Cargar datos iniciales
        self.actualizar_tabla()
        
        # Establecer el foco en el campo de nombre
        self.entry_nombre.focus_set()
    
    def crear_formulario(self):
        """Crea el formulario con mejor estilo"""
        # Título de sección
        tk.Label(self.panel_izquierdo, text="Datos de la Promoción", 
                font=("Segoe UI", 14, "bold"), bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_CLARO).pack(anchor="w", pady=(0, 10))
        
        # Marco para el formulario con estilo mejorado
        frame_form = tk.Frame(self.panel_izquierdo, bg=COLOR_FONDO_SECUNDARIO, 
                            padx=15, pady=15, bd=1, relief=tk.GROOVE)
        frame_form.pack(fill="both", pady=10)
        
        # Contenidos del formulario
        self.inicializar_formulario(frame_form)
        
        # Botones con mejor estilo
        self.frame_botones = tk.Frame(self.panel_izquierdo, bg=COLOR_FONDO_PRINCIPAL)
        self.frame_botones.pack(pady=15, fill="x")
        
        # Botones principales
        ttk.Button(self.frame_botones, text="Agregar Promoción", 
                  command=self.agregar_promocion, style="Accion.TButton").pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        ttk.Button(self.frame_botones, text="Eliminar", 
                  command=self.eliminar_promocion).pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        ttk.Button(self.frame_botones, text="Modificar", 
                  command=self.cargar_datos_promocion).pack(side=tk.LEFT, padx=5, fill="x", expand=True)
    
    def crear_vista_tabla(self):
        """Crea la visualización de la tabla con mejor estilo"""
        # Título de sección
        tk.Label(self.panel_derecho, text="Promociones Activas", 
                font=("Segoe UI", 14, "bold"), bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_CLARO).pack(anchor="w", pady=(0, 10))
        
        # Panel de filtro
        frame_filtro = tk.Frame(self.panel_derecho, bg=COLOR_FONDO_SECUNDARIO, padx=10, pady=5, bd=1, relief=tk.GROOVE)
        frame_filtro.pack(fill="x", pady=(0, 10))
        
        tk.Label(frame_filtro, text="Buscar:", bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TEXTO_CLARO).pack(side=tk.LEFT, padx=5)
        
        self.entry_filtro = ttk.Entry(frame_filtro, width=25)
        self.entry_filtro.pack(side=tk.LEFT, padx=5)
        self.entry_filtro.bind("<Return>", lambda e: self.filtrar_promociones())
        
        ttk.Button(frame_filtro, text="Buscar", command=self.filtrar_promociones).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_filtro, text="Mostrar Todo", command=self.actualizar_tabla).pack(side=tk.LEFT, padx=5)
        
        # Marco para la tabla con estilo mejorado
        self.frame_tabla = tk.Frame(self.panel_derecho, bg=COLOR_FONDO_SECUNDARIO, 
                                 padx=10, pady=10, bd=1, relief=tk.GROOVE)
        self.frame_tabla.pack(fill="both", expand=True)
        
        # Crear tabla
        self.crear_tabla()
        
        # Añadir información de estado
        self.label_estado = tk.Label(self.panel_derecho, text="Mostrando todas las promociones", 
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
        ancho_etiqueta = 15  # Ancho fijo para etiquetas
        ancho_entrada = 25   # Ancho para entradas
        
        # Nombre de la promoción
        tk.Label(frame_parent, text="Nombre:", bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TEXTO_CLARO,
                font=("Segoe UI", 10, "bold"), width=ancho_etiqueta, anchor="w").grid(row=0, column=0, padx=5, pady=8, sticky='w')
        
        self.entry_nombre = ttk.Entry(frame_parent, width=ancho_entrada)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=8, sticky='ew')
        
        # Precio de la promoción
        tk.Label(frame_parent, text="Precio:", bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TEXTO_CLARO,
                font=("Segoe UI", 10, "bold"), width=ancho_etiqueta, anchor="w").grid(row=1, column=0, padx=5, pady=8, sticky='w')
        
        self.entry_precio = ttk.Entry(frame_parent, width=ancho_entrada)
        self.entry_precio.grid(row=1, column=1, padx=5, pady=8, sticky='ew')
        
        # Fecha de Inicio
        tk.Label(frame_parent, text="Fecha Inicio:", bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TEXTO_CLARO,
                font=("Segoe UI", 10, "bold"), width=ancho_etiqueta, anchor="w").grid(row=2, column=0, padx=5, pady=8, sticky='w')
        
        # Si tkcalendar está disponible, usar DateEntry, de lo contrario usar Entry normal
        try:
            self.entry_fecha_inicio = DateEntry(frame_parent, width=ancho_entrada-3, background=COLOR_ACENTO,
                                               foreground=COLOR_TEXTO_CLARO, borderwidth=2, date_pattern='yyyy-mm-dd')
            self.entry_fecha_inicio.grid(row=2, column=1, padx=5, pady=8, sticky='ew')
        except:
            self.entry_fecha_inicio = ttk.Entry(frame_parent, width=ancho_entrada)
            self.entry_fecha_inicio.grid(row=2, column=1, padx=5, pady=8, sticky='ew')
            tk.Label(frame_parent, text="Formato: AAAA-MM-DD", bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TEXTO_CLARO,
                    font=("Segoe UI", 7)).grid(row=2, column=2, padx=5, pady=8, sticky='w')
        
        # Fecha de Fin
        tk.Label(frame_parent, text="Fecha Fin:", bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TEXTO_CLARO,
                font=("Segoe UI", 10, "bold"), width=ancho_etiqueta, anchor="w").grid(row=3, column=0, padx=5, pady=8, sticky='w')
        
        try:
            self.entry_fecha_fin = DateEntry(frame_parent, width=ancho_entrada-3, background=COLOR_ACENTO,
                                           foreground=COLOR_TEXTO_CLARO, borderwidth=2, date_pattern='yyyy-mm-dd')
            self.entry_fecha_fin.grid(row=3, column=1, padx=5, pady=8, sticky='ew')
        except:
            self.entry_fecha_fin = ttk.Entry(frame_parent, width=ancho_entrada)
            self.entry_fecha_fin.grid(row=3, column=1, padx=5, pady=8, sticky='ew')
            tk.Label(frame_parent, text="Formato: AAAA-MM-DD", bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TEXTO_CLARO,
                    font=("Segoe UI", 7)).grid(row=3, column=2, padx=5, pady=8, sticky='w')
        
        # Descripción
        tk.Label(frame_parent, text="Descripción:", bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TEXTO_CLARO,
                font=("Segoe UI", 10, "bold"), width=ancho_etiqueta, anchor="w").grid(row=4, column=0, padx=5, pady=8, sticky='nw')
        
        self.entry_descripcion = tk.Text(frame_parent, height=4, width=ancho_entrada, bg=COLOR_ACENTO, fg=COLOR_TEXTO_CLARO,
                                       font=("Segoe UI", 10), bd=1, relief=tk.SUNKEN)
        self.entry_descripcion.grid(row=4, column=1, padx=5, pady=8, sticky='ew')
    
    def crear_tabla(self):
        """Crea la tabla para mostrar las promociones con mejor estilo"""
        columnas = ("ID", "Nombre", "Precio", "Fecha Inicio", "Fecha Fin", "Descripción")
        self.tabla = ttk.Treeview(self.frame_tabla, columns=columnas, show='headings', style='Treeview')
        
        for col in columnas:
            self.tabla.heading(col, text=col)
            # Ajustar ancho de columnas
            if col == "ID":
                self.tabla.column(col, width=50, anchor="center")
            elif col == "Nombre":
                self.tabla.column(col, width=150, anchor="w")
            elif col == "Descripción":
                self.tabla.column(col, width=200, anchor="w")
            else:
                self.tabla.column(col, width=100, anchor="center")
        
        # Agregar scrollbars
        scrollbar_y = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla.yview)
        scrollbar_x = ttk.Scrollbar(self.frame_tabla, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Empaquetado con mejor organización
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tabla.pack(side="left", fill="both", expand=True)
        
        # Evento de selección para mostrar detalles al hacer clic
        self.tabla.bind('<<TreeviewSelect>>', self.mostrar_detalles_seleccion)
    
    def mostrar_detalles_seleccion(self, event):
        """Muestra detalles de la promoción seleccionada en el estado"""
        seleccion = self.tabla.selection()
        if seleccion:
            promo = self.tabla.item(seleccion)['values']
            self.label_estado.config(text=f"Seleccionada: {promo[1]} - ${promo[2]}")
    
    def filtrar_promociones(self):
        """Filtra promociones por nombre o descripción"""
        texto_busqueda = self.entry_filtro.get().strip().lower()
        if not texto_busqueda:
            self.actualizar_tabla()
            return
            
        # Limpiar tabla
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                SELECT id_promocion, nombre, precio, fecha_inicio, fecha_fin, descripcion 
                FROM Promociones 
                WHERE LOWER(nombre) LIKE %s OR LOWER(descripcion) LIKE %s
            """, (f"%{texto_busqueda}%", f"%{texto_busqueda}%"))
            promociones = cursor.fetchall()
            
            for promo in promociones:
                self.tabla.insert("", "end", values=promo)
                
            # Actualizar estado
            self.label_estado.config(text=f"Mostrando {len(promociones)} resultados para '{texto_busqueda}'")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo filtrar: {e}")
    
    def actualizar_tabla(self):
        """Actualiza los datos de la tabla"""
        # Limpiar tabla
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT id_promocion, nombre, precio, fecha_inicio, fecha_fin, descripcion FROM Promociones")
            promociones = cursor.fetchall()
            
            for promo in promociones:
                self.tabla.insert("", "end", values=promo)
                
            # Actualizar estado
            self.label_estado.config(text=f"Mostrando todas las promociones ({len(promociones)} encontradas)")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la tabla: {e}")
    
    def agregar_promocion(self):
        """Agrega una nueva promoción a la base de datos"""
        nombre = self.entry_nombre.get().strip()
        precio = self.entry_precio.get().strip()
        fecha_inicio = self.entry_fecha_inicio.get().strip()
        fecha_fin = self.entry_fecha_fin.get().strip()
        descripcion = self.entry_descripcion.get("1.0", tk.END).strip()
        
        if not nombre or not precio or not fecha_inicio or not fecha_fin:
            messagebox.showerror("Error", "Los campos Nombre, Precio, Fecha Inicio y Fecha Fin son obligatorios")
            return
        
        try:
            cursor = self.conexion.cursor()
            
            cursor.execute("INSERT INTO Promociones (nombre, precio, fecha_inicio, fecha_fin, descripcion) VALUES (%s, %s, %s, %s, %s)", 
                        (nombre, precio, fecha_inicio, fecha_fin, descripcion))
            self.conexion.commit()
            
            # Mostrar confirmación visual
            frame_confirmacion = tk.Frame(self.frame_principal, bg=COLOR_ACENTO, bd=2, relief=tk.RAISED,
                                      padx=20, pady=20)
            frame_confirmacion.place(relx=0.5, rely=0.5, anchor="center")
            
            tk.Label(frame_confirmacion, text="¡Promoción Agregada con Éxito!",
                   font=("Segoe UI", 14, "bold"), bg=COLOR_ACENTO, fg=COLOR_TEXTO_CLARO).pack(pady=(0, 15))
                   
            tk.Label(frame_confirmacion, text=nombre,
                   font=("Segoe UI", 12), bg=COLOR_ACENTO, fg=COLOR_TEXTO_CLARO).pack(pady=2)
                   
            tk.Label(frame_confirmacion, text=f"Precio: ${precio}",
                   font=("Segoe UI", 12), bg=COLOR_ACENTO, fg=COLOR_TEXTO_CLARO).pack(pady=2)
                   
            # Botón para cerrar la confirmación
            ttk.Button(frame_confirmacion, text="Aceptar", 
                     command=lambda: frame_confirmacion.destroy()).pack(pady=15)
            
            # Limpiar campos
            self.limpiar_campos()
            
            # Actualizar tabla
            self.actualizar_tabla()
            
            # Volver a enfocar el campo de nombre
            self.entry_nombre.focus_set()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la promoción: {e}")
    
    def eliminar_promocion(self):
        """Elimina la promoción seleccionada"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona una promoción para eliminar")
            return
        
        promo = self.tabla.item(seleccion)['values']
        
        # Confirmar eliminación con mejor interfaz
        frame_confirmar = tk.Frame(self.frame_principal, bg=COLOR_FONDO_SECUNDARIO, bd=2, relief=tk.RAISED,
                                padx=20, pady=20)
        frame_confirmar.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(frame_confirmar, text="¿Eliminar esta promoción?",
               font=("Segoe UI", 14, "bold"), bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TEXTO_CLARO).pack(pady=(0, 15))
               
        tk.Label(frame_confirmar, text=promo[1],
               font=("Segoe UI", 12), bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_RESALTE).pack(pady=2)
               
        tk.Label(frame_confirmar, text=f"Precio: ${promo[2]}",
               font=("Segoe UI", 12), bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TEXTO_CLARO).pack(pady=2)
               
        frame_botones_confirm = tk.Frame(frame_confirmar, bg=COLOR_FONDO_SECUNDARIO)
        frame_botones_confirm.pack(pady=15)
        
        # Botones de confirmación
        ttk.Button(frame_botones_confirm, text="Sí, Eliminar", 
                 command=lambda: self.confirmar_eliminacion(promo[0], frame_confirmar)).pack(side=tk.LEFT, padx=10)
                 
        ttk.Button(frame_botones_confirm, text="Cancelar", 
                 command=lambda: frame_confirmar.destroy()).pack(side=tk.LEFT, padx=10)
    
    def confirmar_eliminacion(self, promo_id, frame_confirmar):
        """Procesa la eliminación después de confirmar"""
        frame_confirmar.destroy()
        
        try:
            cursor = self.conexion.cursor()
            cursor.execute("DELETE FROM Promociones WHERE id_promocion = %s", (promo_id,))
            self.conexion.commit()
            
            # Mostrar confirmación de eliminación
            self.label_estado.config(text="Promoción eliminada correctamente")
            
            # Actualizar tabla
            self.actualizar_tabla()
            
            # Enfocar el campo de nombre
            self.entry_nombre.focus_set()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la promoción: {e}")
    
    def cargar_datos_promocion(self):
        """Carga los datos de la promoción seleccionada en el formulario"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona una promoción para modificar")
            return
        
        promo = self.tabla.item(seleccion)['values']
        
        # Limpiar campos
        self.limpiar_campos()
        
        # Cargar datos en formulario
        self.entry_nombre.insert(0, promo[1])  # Nombre
        self.entry_precio.insert(0, promo[2])  # Precio
        
        # Para Entry normal o DateEntry
        if hasattr(self.entry_fecha_inicio, 'delete'):
            # Es un Entry normal
            self.entry_fecha_inicio.delete(0, tk.END)
            self.entry_fecha_inicio.insert(0, promo[3])
            self.entry_fecha_fin.delete(0, tk.END)
            self.entry_fecha_fin.insert(0, promo[4])
        else:
            # Es un DateEntry
            try:
                fecha_inicio = datetime.strptime(str(promo[3]), '%Y-%m-%d')
                self.entry_fecha_inicio.set_date(fecha_inicio)
                fecha_fin = datetime.strptime(str(promo[4]), '%Y-%m-%d')
                self.entry_fecha_fin.set_date(fecha_fin)
            except:
                pass
        
        self.entry_descripcion.delete("1.0", tk.END)
        self.entry_descripcion.insert("1.0", promo[5] if promo[5] else "")  # Descripción
        
        # Cambiar botones con mejor estilo
        for widget in self.frame_botones.winfo_children():
            widget.destroy()
        
        ttk.Button(self.frame_botones, text="Guardar Cambios", 
                  command=self.modificar_promocion, style="Accion.TButton").pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        ttk.Button(self.frame_botones, text="Cancelar", 
                  command=self.cancelar_modificacion).pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        # Actualizar estado
        self.label_estado.config(text=f"Editando: {promo[1]}")
        
        # Enfocar el campo de nombre para editar
        self.entry_nombre.focus_set()
    
    def modificar_promocion(self):
        """Modifica la promoción seleccionada con los nuevos datos"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona una promoción para modificar")
            return
        
        promo_id = self.tabla.item(seleccion)['values'][0]
        nombre = self.entry_nombre.get().strip()
        precio = self.entry_precio.get().strip()
        
        # Obtener fecha según el tipo de widget
        if hasattr(self.entry_fecha_inicio, 'get'):
            fecha_inicio = self.entry_fecha_inicio.get().strip()
            fecha_fin = self.entry_fecha_fin.get().strip()
        else:
            fecha_inicio = self.entry_fecha_inicio.get_date().strftime('%Y-%m-%d')
            fecha_fin = self.entry_fecha_fin.get_date().strftime('%Y-%m-%d')
            
        descripcion = self.entry_descripcion.get("1.0", tk.END).strip()
        
        if not nombre or not precio or not fecha_inicio or not fecha_fin:
            messagebox.showerror("Error", "Los campos Nombre, Precio, Fecha Inicio y Fecha Fin son obligatorios")
            return
        
        try:
            cursor = self.conexion.cursor()
            cursor.execute("UPDATE Promociones SET nombre=%s, precio=%s, fecha_inicio=%s, fecha_fin=%s, descripcion=%s WHERE id_promocion=%s",
                        (nombre, precio, fecha_inicio, fecha_fin, descripcion, promo_id))
            self.conexion.commit()
            
            # Mostrar confirmación visual
            frame_confirmacion = tk.Frame(self.frame_principal, bg=COLOR_ACENTO, bd=2, relief=tk.RAISED,
                                       padx=20, pady=20)
            frame_confirmacion.place(relx=0.5, rely=0.5, anchor="center")
            
            tk.Label(frame_confirmacion, text="¡Promoción Modificada con Éxito!",
                   font=("Segoe UI", 14, "bold"), bg=COLOR_ACENTO, fg=COLOR_TEXTO_CLARO).pack(pady=(0, 15))
                   
            tk.Label(frame_confirmacion, text=nombre,
                   font=("Segoe UI", 12), bg=COLOR_ACENTO, fg=COLOR_TEXTO_CLARO).pack(pady=2)
                   
            # Botón para cerrar la confirmación
            ttk.Button(frame_confirmacion, text="Aceptar", 
                     command=lambda: frame_confirmacion.destroy()).pack(pady=15)
            
            # Restaurar botones originales
            self.cancelar_modificacion()
            
            # Actualizar tabla
            self.actualizar_tabla()
            
            # Enfocar el campo de nombre
            self.entry_nombre.focus_set()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar la promoción: {e}")
    
    def cancelar_modificacion(self):
        """Cancela la modificación y restaura los botones originales"""
        # Limpiar campos
        self.limpiar_campos()
        
        # Restaurar botones originales
        for widget in self.frame_botones.winfo_children():
            widget.destroy()
        
        ttk.Button(self.frame_botones, text="Agregar Promoción", 
                  command=self.agregar_promocion, style="Accion.TButton").pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        ttk.Button(self.frame_botones, text="Eliminar", 
                  command=self.eliminar_promocion).pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        ttk.Button(self.frame_botones, text="Modificar", 
                  command=self.cargar_datos_promocion).pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        # Actualizar estado
        self.label_estado.config(text="Mostrando todas las promociones")
        
        # Enfocar el campo de nombre
        self.entry_nombre.focus_set()
    
    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        self.entry_nombre.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        
        # Limpiar fechas según el tipo de widget
        if hasattr(self.entry_fecha_inicio, 'delete'):
            self.entry_fecha_inicio.delete(0, tk.END)
            self.entry_fecha_fin.delete(0, tk.END)
        else:
            # DateEntry: establecer a la fecha actual
            hoy = datetime.now()
            self.entry_fecha_inicio.set_date(hoy)
            self.entry_fecha_fin.set_date(hoy)
            
        self.entry_descripcion.delete("1.0", tk.END)

# Función de compatibilidad para código antiguo (no se usará con la nueva estructura)
def abrir_gestion_promociones():
    import mysql.connector
    
    ventana = tk.Toplevel()
    ventana.title("Gestión de Promociones")
    ventana.geometry("900x600")
    ventana.configure(bg=COLOR_FONDO_PRINCIPAL)
    
    # Conectar a la base de datos
    conexion = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="gestionbebidas"
    )
    
    # Inicializar gestión de promociones
    GestionPromociones(ventana, conexion)