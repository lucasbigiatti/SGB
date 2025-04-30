# fuerza la carga de los mensajes en inglés
from mysql.connector.locales.eng import client_error



import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import mysql.connector
import traceback  # Para obtener información detallada de errores

# Conexión a la base de datos
try:
    conexion = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="gestionbebidas"
    )
    print("Conexión a la base de datos exitosa")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
    messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {e}")
    sys.exit(1)  # Salir si no hay conexión

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



# Historial de navegación
historial_navegacion = []

# Variables globales
foco_actual = None  # Widget que debe tener el foco
contador_intentos_foco = 0  # Contador de intentos

# Verificar stock bajo
def verificar_stock_bajo():
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, stock, stock_minimo FROM productos WHERE stock <= stock_minimo")
    productos_bajo_stock = cursor.fetchall()

    if productos_bajo_stock:
        mensaje = "¡Atención! Los siguientes productos tienen bajo stock:\n\n"
        for nombre, stock, minimo in productos_bajo_stock:
            mensaje += f"- {nombre}: {stock} unidades (mínimo: {minimo})\n"
        messagebox.showwarning("Stock Bajo", mensaje)

# Función para forzar el foco
def forzar_foco():
    global foco_actual, contador_intentos_foco
    if foco_actual:
        try:
            foco_actual.focus_force()
            print(f"Intento de forzar foco #{contador_intentos_foco}")
            contador_intentos_foco += 1
            
            # Después de 10 intentos, detenemos
            if contador_intentos_foco < 10:
                # Programar otro intento en 100ms
                root.after(100, forzar_foco)
            else:
                contador_intentos_foco = 0
        except Exception as e:
            print(f"Error al forzar foco: {e}")
            contador_intentos_foco = 0

# Clase principal de la aplicación
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Bebidas - LOS TIOS")
        self.root.geometry("800x600")
        self.root.configure(bg=COLOR_FONDO_PRINCIPAL)

        # Configurar estilo
        self.configurar_estilo()
        
        # Crear frame contenedor principal
        self.contenedor_principal = tk.Frame(self.root, bg=COLOR_FONDO_PRINCIPAL)
        self.contenedor_principal.pack(fill="both", expand=True)
        
        # Importar módulos después de inicializar la aplicación
        try:
            # Agregar la ruta al path
            ruta_ventanas = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            print(f"Añadiendo ruta al path: {ruta_ventanas}")
            sys.path.append(ruta_ventanas)
            
            # Importar módulos
            print("Importando módulos...")
            
            # Producto
            try:
                from Ventanas.producto import GestionProductos
                print("Módulo de productos importado correctamente")
                self.GestionProductos = GestionProductos
            except Exception as e:
                print(f"Error al importar módulo de productos: {e}")
                print(traceback.format_exc())
                self.GestionProductos = None
            
            # Dashboard/Estadísticas
            try:
                from Ventanas.dashboard import Estadisticas
                print("Módulo de estadísticas importado correctamente")
                self.Estadisticas = Estadisticas
            except Exception as e:
                print(f"Error al importar módulo de estadísticas: {e}")
                print(traceback.format_exc())
                self.Estadisticas = None
            
            # Ventas
            try:
                from Ventanas.ventas import GestionVentas
                print("Módulo de ventas importado correctamente")
                self.GestionVentas = GestionVentas
            except Exception as e:
                print(f"Error al importar módulo de ventas: {e}")
                print(traceback.format_exc())
                self.GestionVentas = None
            
            # Promociones
            try:
                from Ventanas.promocion import GestionPromociones
                print("Módulo de promociones importado correctamente")
                self.GestionPromociones = GestionPromociones
            except Exception as e:
                print(f"Error al importar módulo de promociones: {e}")
                print(traceback.format_exc())
                self.GestionPromociones = None
                
        except Exception as e:
            print(f"Error general al importar módulos: {e}")
            print(traceback.format_exc())
        
        # Iniciar en la pantalla principal después de cargar los módulos
        self.mostrar_pantalla_principal()

    def configurar_estilo(self):
        estilo = ttk.Style()
        estilo.theme_use("default")
        estilo.configure("TButton",
                         background=COLOR_BOTON_HOVER,
                         foreground=COLOR_TEXTO_CLARO,
                         font=("Segoe UI", 12),
                         padding=10)
        estilo.map("TButton",
                   background=[("active", COLOR_BOTON_HOVER)])
                   
        # Estilo para el botón de volver
        estilo.configure("Volver.TButton",
                         background="#FF6B6B",
                         foreground=COLOR_TEXTO_CLARO,
                         font=("Segoe UI", 10),
                         padding=5)
        estilo.map("Volver.TButton",
                   background=[("active", "#FF8888")])

    def limpiar_pantalla(self):
        # Eliminar todos los widgets del contenedor principal
        for widget in self.contenedor_principal.winfo_children():
            widget.destroy()

    def volver_atras(self):
        if historial_navegacion:
            # Obtener la última pantalla visitada
            ultima_pantalla = historial_navegacion.pop()
            # Llamar a la función correspondiente sin añadir al historial
            ultima_pantalla(agregar_historial=False)

    def mostrar_pantalla_principal(self, agregar_historial=True):
        if agregar_historial and (not historial_navegacion or historial_navegacion[-1] != self.mostrar_pantalla_principal):
            historial_navegacion.append(self.mostrar_pantalla_principal)
            
        self.limpiar_pantalla()
        
        # Título
        titulo = tk.Label(self.contenedor_principal, text="Sistema de Gestión de Bebidas", 
                         font=("Segoe UI", 18, "bold"), bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_CLARO)
        titulo.pack(pady=30)
        
        # Botones
        boton_productos = ttk.Button(self.contenedor_principal, text="Gestionar Productos", 
                                   command=self.abrir_gestion_productos)
        boton_productos.pack(pady=10)
        
        boton_estadisticas = ttk.Button(self.contenedor_principal, text="Estadísticas", 
                                     command=self.mostrar_estadisticas)
        boton_estadisticas.pack(pady=10)
        
        boton_ventas = ttk.Button(self.contenedor_principal, text="Registrar Ventas", 
                               command=self.abrir_gestion_ventas)
        boton_ventas.pack(pady=10)
        
        boton_promociones = ttk.Button(self.contenedor_principal, text="Gestionar Promociones", 
                                    command=self.abrir_gestion_promociones)
        boton_promociones.pack(pady=10)
        
        # Enfocar el primer botón
        global foco_actual
        foco_actual = boton_productos
        self.root.after(100, forzar_foco)
        
        # Marca de agua
        marca_agua = tk.Label(self.contenedor_principal, text="Desarrollado por Lucas Bigiatti",
                             font=("Segoe UI", 8), bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_CLARO)
        marca_agua.place(relx=0.01, rely=0.98, anchor="sw")

    def abrir_gestion_productos(self):
        print("Abriendo gestión de productos...")
        historial_navegacion.append(self.mostrar_pantalla_principal)
        self.limpiar_pantalla()
        
        # Agregar botón para volver
        boton_volver = ttk.Button(self.contenedor_principal, text="← Volver", 
                               command=self.volver_atras, style="Volver.TButton")
        boton_volver.pack(anchor="nw", padx=10, pady=10)
        
        # Inicializar la gestión de productos dentro del contenedor principal
        frame_productos = tk.Frame(self.contenedor_principal, bg=COLOR_FONDO_PRINCIPAL)
        frame_productos.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Verificar si la clase está disponible
        if self.GestionProductos:
            try:
                gestion_productos = self.GestionProductos(frame_productos, conexion)
                print("Gestión de productos inicializada correctamente")
                
                # Forzar foco después de renderizar
                global foco_actual, contador_intentos_foco
                if hasattr(gestion_productos, 'entries') and gestion_productos.entries:
                    foco_actual = gestion_productos.entries[0]
                    contador_intentos_foco = 0
                    self.root.after(200, forzar_foco)
                
            except Exception as e:
                print(f"Error al inicializar gestión de productos: {e}")
                print(traceback.format_exc())
                tk.Label(frame_productos, text=f"Error al cargar el módulo: {e}", 
                        bg=COLOR_FONDO_PRINCIPAL, fg="red", font=("Segoe UI", 12)).pack(pady=20)
        else:
            tk.Label(frame_productos, text="Módulo de Gestión de Productos no disponible", 
                    bg=COLOR_FONDO_PRINCIPAL, fg="red", font=("Segoe UI", 12)).pack(pady=20)

    def mostrar_estadisticas(self):
        print("Abriendo estadísticas...")
        historial_navegacion.append(self.mostrar_pantalla_principal)
        self.limpiar_pantalla()
        
        # Agregar botón para volver
        boton_volver = ttk.Button(self.contenedor_principal, text="← Volver", 
                               command=self.volver_atras, style="Volver.TButton")
        boton_volver.pack(anchor="nw", padx=10, pady=10)
        
        # Inicializar estadísticas dentro del contenedor principal
        frame_estadisticas = tk.Frame(self.contenedor_principal, bg=COLOR_FONDO_PRINCIPAL)
        frame_estadisticas.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Verificar si la clase está disponible
        if self.Estadisticas:
            try:
                estadisticas = self.Estadisticas(frame_estadisticas, conexion)
                print("Estadísticas inicializadas correctamente")
                
                # Forzar foco después de renderizar
                global foco_actual, contador_intentos_foco
                if hasattr(estadisticas, 'boton_grafico'):
                    foco_actual = estadisticas.boton_grafico
                    contador_intentos_foco = 0
                    self.root.after(200, forzar_foco)
                
            except Exception as e:
                print(f"Error al inicializar estadísticas: {e}")
                print(traceback.format_exc())
                tk.Label(frame_estadisticas, text=f"Error al cargar el módulo: {e}", 
                        bg=COLOR_FONDO_PRINCIPAL, fg="red", font=("Segoe UI", 12)).pack(pady=20)
        else:
            tk.Label(frame_estadisticas, text="Módulo de Estadísticas no disponible", 
                    bg=COLOR_FONDO_PRINCIPAL, fg="red", font=("Segoe UI", 12)).pack(pady=20)

    def abrir_gestion_ventas(self):
        print("Abriendo gestión de ventas...")
        historial_navegacion.append(self.mostrar_pantalla_principal)
        self.limpiar_pantalla()
        
        # Agregar botón para volver
        boton_volver = ttk.Button(self.contenedor_principal, text="← Volver", 
                               command=self.volver_atras, style="Volver.TButton")
        boton_volver.pack(anchor="nw", padx=10, pady=10)
        
        # Inicializar ventas dentro del contenedor principal
        frame_ventas = tk.Frame(self.contenedor_principal, bg=COLOR_FONDO_PRINCIPAL)
        frame_ventas.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Verificar si la clase está disponible
        if self.GestionVentas:
            try:
                gestion_ventas = self.GestionVentas(frame_ventas, conexion)
                print("Gestión de ventas inicializada correctamente")
                
                # Forzar foco después de renderizar
                global foco_actual, contador_intentos_foco
                if hasattr(gestion_ventas, 'entry_cliente'):
                    foco_actual = gestion_ventas.entry_cliente
                    contador_intentos_foco = 0
                    self.root.after(200, forzar_foco)
                
            except Exception as e:
                print(f"Error al inicializar gestión de ventas: {e}")
                print(traceback.format_exc())
                tk.Label(frame_ventas, text=f"Error al cargar el módulo: {e}", 
                        bg=COLOR_FONDO_PRINCIPAL, fg="red", font=("Segoe UI", 12)).pack(pady=20)
        else:
            tk.Label(frame_ventas, text="Módulo de Gestión de Ventas no disponible", 
                    bg=COLOR_FONDO_PRINCIPAL, fg="red", font=("Segoe UI", 12)).pack(pady=20)

    def abrir_gestion_promociones(self):
        print("Abriendo gestión de promociones...")
        historial_navegacion.append(self.mostrar_pantalla_principal)
        self.limpiar_pantalla()
        
        # Agregar botón para volver
        boton_volver = ttk.Button(self.contenedor_principal, text="← Volver", 
                               command=self.volver_atras, style="Volver.TButton")
        boton_volver.pack(anchor="nw", padx=10, pady=10)
        
        # Inicializar promociones dentro del contenedor principal
        frame_promociones = tk.Frame(self.contenedor_principal, bg=COLOR_FONDO_PRINCIPAL)
        frame_promociones.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Verificar si la clase está disponible
        if self.GestionPromociones:
            try:
                gestion_promociones = self.GestionPromociones(frame_promociones, conexion)
                print("Gestión de promociones inicializada correctamente")
                
                # Forzar foco después de renderizar
                global foco_actual, contador_intentos_foco
                if hasattr(gestion_promociones, 'entry_nombre'):
                    foco_actual = gestion_promociones.entry_nombre
                    contador_intentos_foco = 0
                    self.root.after(200, forzar_foco)
                
            except Exception as e:
                print(f"Error al inicializar gestión de promociones: {e}")
                print(traceback.format_exc())
                tk.Label(frame_promociones, text=f"Error al cargar el módulo: {e}", 
                        bg=COLOR_FONDO_PRINCIPAL, fg="red", font=("Segoe UI", 12)).pack(pady=20)
        else:
            tk.Label(frame_promociones, text="Módulo de Gestión de Promociones no disponible", 
                    bg=COLOR_FONDO_PRINCIPAL, fg="red", font=("Segoe UI", 12)).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    try:
        verificar_stock_bajo()  # Verificar stock bajo antes de iniciar
    except Exception as e:
        print(f"Error al verificar stock bajo: {e}")
    root.mainloop()


def verificar_mysql_xampp():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("127.0.0.1", 3306))
        s.close()
        return True
    except:
        return False

# Al inicio de tu aplicación
if not verificar_mysql_xampp():
    respuesta = messagebox.askquestion("MySQL no disponible", 
                                    "MySQL no está en ejecución. ¿Deseas intentar iniciar XAMPP automáticamente?")
    if respuesta == 'yes':
        try:
            import subprocess
            # Ruta típica a XAMPP, ajusta según tu instalación
            xampp_control = r"C:\xampp\xampp-control.exe"
            subprocess.Popen(xampp_control)
            messagebox.showinfo("Iniciando XAMPP", 
                              "Por favor inicia MySQL desde el panel de control de XAMPP y luego reinicia esta aplicación.")
        except:
            messagebox.showerror("Error", 
                                "No se pudo iniciar XAMPP automáticamente. Por favor inicia MySQL manualmente.")
    sys.exit(1)


    