# Ventanas/dashboard.py
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import decimal  # Importamos para manejar el tipo decimal

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

class Estadisticas:
    def __init__(self, frame_padre, conexion):
        self.frame_padre = frame_padre
        self.conexion = conexion
        
        # Configurar el frame principal con mejor apariencia
        self.frame_principal = tk.Frame(frame_padre, bg=COLOR_FONDO_PRINCIPAL)
        self.frame_principal.pack(fill="both", expand=True)
        
        # Título con separador
        frame_titulo = tk.Frame(self.frame_principal, bg=COLOR_FONDO_PRINCIPAL)
        frame_titulo.pack(fill="x", pady=(0, 15))
        
        tk.Label(frame_titulo, text="Estadísticas del Mes", 
                font=("Segoe UI", 18, "bold"), bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_CLARO).pack(pady=(0, 5))
        
        # Separador decorativo
        ttk.Separator(frame_titulo, orient="horizontal").pack(fill="x", pady=(0, 10))
        
        # Obtener estadísticas
        self.estadisticas = self.obtener_estadisticas()
        
        if self.estadisticas:
            # Mostrar información
            self.mostrar_informacion()
            
            # Botón para ver gráficos con mejor estilo
            self.boton_grafico = ttk.Button(self.frame_principal, text="Ver Gráfico de Ventas", 
                      command=self.mostrar_grafico, style="Accion.TButton")
            self.boton_grafico.pack(pady=20)
            
            # Establecer foco en el botón de gráfico para interacción inmediata
            self.boton_grafico.focus_set()
    
    def obtener_estadisticas(self):
        """Consulta la base de datos para obtener estadísticas de ventas."""
        try:
            cursor = self.conexion.cursor()

            # Obtener ventas del mes actual
            mes_actual = datetime.now().strftime("%Y-%m")
            cursor.execute("SELECT COUNT(*) FROM Ventas WHERE DATE_FORMAT(fecha, '%Y-%m') = %s", (mes_actual,))
            total_ventas = cursor.fetchone()[0]

            # Obtener la ganancia total del mes
            cursor.execute("SELECT COALESCE(SUM(total), 0) FROM Ventas WHERE DATE_FORMAT(fecha, '%Y-%m') = %s", (mes_actual,))
            ganancia_total = cursor.fetchone()[0]  

            # Obtener el producto más vendido
            cursor.execute("""
                SELECT P.nombre, COALESCE(SUM(DV.cantidad), 0) AS total_vendido
                FROM detalle_ventas DV
                JOIN Productos P ON DV.id_producto = P.id_producto
                JOIN Ventas V ON DV.id_venta = V.id_venta
                WHERE DATE_FORMAT(V.fecha, '%Y-%m') = %s
                GROUP BY P.nombre
                ORDER BY total_vendido DESC
                LIMIT 1;
            """, (mes_actual,))
            producto_mas_vendido = cursor.fetchone()

            return {
                "total_ventas": total_ventas,
                "ganancia_total": ganancia_total,
                "producto_mas_vendido": producto_mas_vendido[0] if producto_mas_vendido else "Ninguno",
                "cantidad_vendida": producto_mas_vendido[1] if producto_mas_vendido else 0
            }
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron obtener las estadísticas: {e}")
            return None
    
    def mostrar_informacion(self):
        """Muestra la información de estadísticas en la interfaz."""
        # Frame con estilo mejorado para resaltar las estadísticas
        frame_info = tk.Frame(self.frame_principal, bg=COLOR_FONDO_SECUNDARIO, 
                           padx=20, pady=20, bd=1, relief=tk.GROOVE)
        frame_info.pack(pady=15, padx=20, fill="x")
        
        # Título de sección
        tk.Label(frame_info, text="Resumen del Mes Actual", 
               font=("Segoe UI", 14, "bold"), bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_RESALTE).pack(pady=(0, 15))
        
        # Diseño de tarjetas para las estadísticas
        frame_stats = tk.Frame(frame_info, bg=COLOR_FONDO_SECUNDARIO)
        frame_stats.pack(fill="x")
        
        # Tarjeta 1: Total de Ventas
        frame_ventas = tk.Frame(frame_stats, bg=COLOR_ACENTO, padx=15, pady=15, bd=0)
        frame_ventas.pack(side=tk.LEFT, expand=True, fill="x", padx=5)
        
        tk.Label(frame_ventas, text="Total de Ventas", 
               font=("Segoe UI", 10), bg=COLOR_ACENTO, fg=COLOR_TEXTO_CLARO).pack()
        
        tk.Label(frame_ventas, text=f"{self.estadisticas['total_ventas']}", 
               font=("Segoe UI", 22, "bold"), bg=COLOR_ACENTO, fg=COLOR_TEXTO_CLARO).pack(pady=5)
        
        # Tarjeta 2: Ganancia Total
        frame_ganancia = tk.Frame(frame_stats, bg=COLOR_ACENTO, padx=15, pady=15, bd=0)
        frame_ganancia.pack(side=tk.LEFT, expand=True, fill="x", padx=5)
        
        tk.Label(frame_ganancia, text="Ganancia Total", 
               font=("Segoe UI", 10), bg=COLOR_ACENTO, fg=COLOR_TEXTO_CLARO).pack()
        
        # Convertir a float para asegurar un formato consistente
        ganancia = float(self.estadisticas['ganancia_total']) if self.estadisticas['ganancia_total'] else 0.0
        
        tk.Label(frame_ganancia, text=f"${ganancia:.2f}", 
               font=("Segoe UI", 22, "bold"), bg=COLOR_ACENTO, fg=COLOR_TEXTO_CLARO).pack(pady=5)
        
        # Tarjeta 3: Producto más vendido
        frame_producto = tk.Frame(frame_info, bg=COLOR_ACENTO, padx=15, pady=15, bd=0)
        frame_producto.pack(fill="x", pady=10, padx=5)
        
        tk.Label(frame_producto, text="Producto Más Vendido", 
               font=("Segoe UI", 10), bg=COLOR_ACENTO, fg=COLOR_TEXTO_CLARO).pack(anchor="w")
        
        tk.Label(frame_producto, 
                text=f"{self.estadisticas['producto_mas_vendido']} ({self.estadisticas['cantidad_vendida']} unidades)",
                font=("Segoe UI", 14, "bold"), bg=COLOR_ACENTO, fg=COLOR_TEXTO_CLARO).pack(anchor="w", pady=5)
    
    def mostrar_grafico(self):
        """Muestra un gráfico de ventas por producto."""
        try:
            cursor = self.conexion.cursor()

            cursor.execute("""
                SELECT P.nombre, SUM(DV.cantidad) 
                FROM detalle_ventas DV
                JOIN Productos P ON DV.id_producto = P.id_producto
                GROUP BY P.nombre
                ORDER BY SUM(DV.cantidad) DESC;
            """)

            datos = cursor.fetchall()

            if not datos:
                messagebox.showinfo("Información", "No hay datos para mostrar en el gráfico.")
                return

            # Extraer datos y convertir cantidades a float para evitar problemas de tipos
            productos = []
            cantidades = []
            
            for nombre, cantidad in datos:
                productos.append(nombre)
                # Convertir explícitamente a float para evitar problemas con Decimal
                if isinstance(cantidad, decimal.Decimal):
                    cantidades.append(float(cantidad))
                else:
                    cantidades.append(float(cantidad))

            # Personalización del estilo de la gráfica para que combine con la interfaz
            plt.style.use('dark_background')
            plt.rcParams['text.color'] = COLOR_TEXTO_CLARO
            plt.rcParams['axes.labelcolor'] = COLOR_TEXTO_CLARO
            plt.rcParams['xtick.color'] = COLOR_TEXTO_CLARO
            plt.rcParams['ytick.color'] = COLOR_TEXTO_CLARO
            plt.rcParams['axes.edgecolor'] = COLOR_TEXTO_CLARO
            plt.rcParams['axes.facecolor'] = COLOR_FONDO_SECUNDARIO
            plt.rcParams['figure.facecolor'] = COLOR_FONDO_PRINCIPAL
            
            # Crear gráfico
            plt.figure(figsize=(10, 6))
            barras = plt.barh(productos, cantidades, color=COLOR_RESALTE)
            
            # Personalización adicional
            plt.xlabel("Cantidad Vendida", fontsize=12)
            plt.ylabel("Productos", fontsize=12)
            plt.title("Ventas por Producto - Mes Actual", fontsize=16, color=COLOR_TEXTO_CLARO)
            plt.gca().invert_yaxis()
            plt.grid(axis='x', linestyle='--', alpha=0.3)
            
            # Añadir valores en las barras
            for i, v in enumerate(cantidades):
                plt.text(v + 0.1, i, str(int(v)), va='center', color=COLOR_TEXTO_CLARO)
                
            plt.tight_layout()
            plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el gráfico: {e}")
            # Mostrar más detalles del error para depuración
            import traceback
            print(f"Error al generar gráfico: {e}")
            print(traceback.format_exc())

# Función de compatibilidad para código antiguo (no se usará con la nueva estructura)
def mostrar_estadisticas():
    import mysql.connector
    
    ventana = tk.Toplevel()
    ventana.title("Dashboard de Estadísticas")
    ventana.geometry("500x400")
    ventana.configure(bg=COLOR_FONDO_PRINCIPAL)
    
    # Conectar a la base de datos
    conexion = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="gestionbebidas"
    )
    
    # Inicializar estadísticas
    Estadisticas(ventana, conexion)