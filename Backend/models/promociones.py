# Ventanas/promocion.py
import tkinter as tk
from tkinter import ttk, messagebox

# Colores personalizados
COLOR_FONDO = "#2C2F33"
COLOR_BOTON = "#7289DA"
COLOR_TEXTO = "#FFFFFF"
COLOR_BOTON_HOVER = "#99AAB5"

class GestionPromociones:
    def __init__(self, frame_padre, conexion):
        self.frame_padre = frame_padre
        self.conexion = conexion
        
        # Configurar el frame principal
        self.frame_principal = tk.Frame(frame_padre, bg=COLOR_FONDO)
        self.frame_principal.pack(fill="both", expand=True)
        
        # Título
        tk.Label(self.frame_principal, text="Gestión de Promociones", 
                font=("Segoe UI", 16, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=10)
        
        # Frame para formulario
        self.frame_formulario = tk.Frame(self.frame_principal, bg=COLOR_FONDO)
        self.frame_formulario.pack(pady=10)
        
        # Inicializar formulario
        self.inicializar_formulario()
        
        # Frame para tabla
        self.frame_tabla = tk.Frame(self.frame_principal, bg=COLOR_FONDO)
        self.frame_tabla.pack(pady=10, fill="both", expand=True)
        
        # Crear tabla
        self.crear_tabla()
        
        # Frame para botones
        self.frame_botones = tk.Frame(self.frame_principal, bg=COLOR_FONDO)
        self.frame_botones.pack(pady=10)
        
        # Botones
        ttk.Button(self.frame_botones, text="Agregar Promoción", 
                  command=self.agregar_promocion).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.frame_botones, text="Eliminar Promoción", 
                  command=self.eliminar_promocion).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.frame_botones, text="Modificar Promoción", 
                  command=self.cargar_datos_promocion).pack(side=tk.LEFT, padx=5)
        
        # Cargar datos iniciales
        self.actualizar_tabla()
    
    def inicializar_formulario(self):
        """Inicializa los campos del formulario"""
        # Nombre de la promoción
        tk.Label(self.frame_formulario, text="Nombre:", bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_nombre = ttk.Entry(self.frame_formulario)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)
        
        # Precio de la promoción
        tk.Label(self.frame_formulario, text="Precio:", bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.entry_precio = ttk.Entry(self.frame_formulario)
        self.entry_precio.grid(row=1, column=1, padx=5, pady=5)
        
        # Fecha de Inicio
        tk.Label(self.frame_formulario, text="Fecha Inicio:", bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.entry_fecha_inicio = ttk.Entry(self.frame_formulario)
        self.entry_fecha_inicio.grid(row=2, column=1, padx=5, pady=5)
        
        # Fecha de Fin
        tk.Label(self.frame_formulario, text="Fecha Fin:", bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.entry_fecha_fin = ttk.Entry(self.frame_formulario)
        self.entry_fecha_fin.grid(row=3, column=1, padx=5, pady=5)
        
        # Descripción
        tk.Label(self.frame_formulario, text="Descripción:", bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.entry_descripcion = tk.Text(self.frame_formulario, height=3, width=30)
        self.entry_descripcion.grid(row=4, column=1, padx=5, pady=5)
    
    def crear_tabla(self):
        """Crea la tabla para mostrar las promociones"""
        columnas = ("ID", "Nombre", "Precio", "Fecha Inicio", "Fecha Fin", "Descripción")
        self.tabla = ttk.Treeview(self.frame_tabla, columns=columnas, show='headings')
        
        for col in columnas:
            self.tabla.heading(col, text=col)
            # Ajustar ancho de columnas
            if col == "ID":
                self.tabla.column(col, width=50, anchor="center")
            elif col == "Descripción":
                self.tabla.column(col, width=200, anchor="w")
            else:
                self.tabla.column(col, width=120, anchor="center")
        
        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
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
            messagebox.showinfo("Éxito", "Promoción agregada correctamente")
            
            # Limpiar campos
            self.limpiar_campos()
            
            # Actualizar tabla
            self.actualizar_tabla()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la promoción: {e}")
    
    def eliminar_promocion(self):
        """Elimina la promoción seleccionada"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona una promoción para eliminar")
            return
        
        # Confirmar eliminación
        respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta promoción?")
        if not respuesta:
            return
        
        # Eliminar promoción
        promo_id = self.tabla.item(seleccion)['values'][0]
        try:
            cursor = self.conexion.cursor()
            cursor.execute("DELETE FROM Promociones WHERE id_promocion = %s", (promo_id,))
            self.conexion.commit()
            messagebox.showinfo("Éxito", "Promoción eliminada correctamente")
            
            # Actualizar tabla
            self.actualizar_tabla()
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
        self.entry_fecha_inicio.insert(0, promo[3])  # Fecha Inicio
        self.entry_fecha_fin.insert(0, promo[4])  # Fecha Fin
        self.entry_descripcion.insert("1.0", promo[5] if promo[5] else "")  # Descripción
        
        # Cambiar botones
        for widget in self.frame_botones.winfo_children():
            widget.destroy()
        
        ttk.Button(self.frame_botones, text="Guardar Cambios", 
                  command=self.modificar_promocion).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.frame_botones, text="Cancelar", 
                  command=self.cancelar_modificacion).pack(side=tk.LEFT, padx=5)
    
    def modificar_promocion(self):
        """Modifica la promoción seleccionada con los nuevos datos"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona una promoción para modificar")
            return
        
        promo_id = self.tabla.item(seleccion)['values'][0]
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
            cursor.execute("UPDATE Promociones SET nombre=%s, precio=%s, fecha_inicio=%s, fecha_fin=%s, descripcion=%s WHERE id_promocion=%s",
                        (nombre, precio, fecha_inicio, fecha_fin, descripcion, promo_id))
            self.conexion.commit()
            messagebox.showinfo("Éxito", "Promoción modificada correctamente")
            
            # Restaurar botones originales
            self.cancelar_modificacion()
            
            # Actualizar tabla
            self.actualizar_tabla()
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
                  command=self.agregar_promocion).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.frame_botones, text="Eliminar Promoción", 
                  command=self.eliminar_promocion).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.frame_botones, text="Modificar Promoción", 
                  command=self.cargar_datos_promocion).pack(side=tk.LEFT, padx=5)
    
    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        self.entry_nombre.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_fecha_inicio.delete(0, tk.END)
        self.entry_fecha_fin.delete(0, tk.END)
        self.entry_descripcion.delete("1.0", tk.END)

# Función de compatibilidad para código antiguo (no se usará con la nueva estructura)
def abrir_gestion_promociones():
    import mysql.connector
    
    ventana = tk.Toplevel()
    ventana.title("Gestión de Promociones")
    ventana.geometry("750x500")
    ventana.configure(bg="#2C2F33")
    
    # Conectar a la base de datos
    conexion = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="gestionbebidas"
    )
    
    # Inicializar gestión de promociones
    GestionPromociones(ventana, conexion)