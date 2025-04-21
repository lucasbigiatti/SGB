# main.py
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import logging
import importlib.util
from pathlib import Path

# Importar configuraciones
from config import APP_CONFIG, UI_COLORS, IMAGES_DIR, LOG_CONFIG
from database import DatabaseManager

# Configurar logging
def setup_logging():
    log_dir = os.path.dirname(LOG_CONFIG["LOG_FILE"])
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    logging.basicConfig(
        filename=LOG_CONFIG["LOG_FILE"],
        level=getattr(logging, LOG_CONFIG["LOG_LEVEL"]),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    # También mostrar en consola
    console = logging.StreamHandler()
    console.setLevel(getattr(logging, LOG_CONFIG["LOG_LEVEL"]))
    logging.getLogger('').addHandler(console)

def verificar_directorios():
    """Verifica y crea los directorios necesarios"""
    directorios = [IMAGES_DIR, os.path.dirname(LOG_CONFIG["LOG_FILE"])]
    for directorio in directorios:
        if not os.path.exists(directorio):
            os.makedirs(directorio)
            logging.info(f"Directorio creado: {directorio}")

def importar_modulo(nombre_archivo):
    """Importa un módulo de forma dinámica y segura"""
    try:
        # Buscar el archivo en diferentes ubicaciones
        posibles_rutas = [
            f"{nombre_archivo}.py",
            f"Ventanas/{nombre_archivo}.py",
            f"Frontend/Ventanas/{nombre_archivo}.py"
        ]
        
        ruta_modulo = None
        for ruta in posibles_rutas:
            if os.path.exists(ruta):
                ruta_modulo = ruta
                break
                
        if ruta_modulo:
            logging.info(f"Importando módulo: {ruta_modulo}")
            spec = importlib.util.spec_from_file_location(nombre_archivo, ruta_modulo)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)
            return modulo
        else:
            logging.error(f"No se encontró el archivo {nombre_archivo}.py")
            return None
    except Exception as e:
        logging.error(f"Error al importar {nombre_archivo}: {e}")
        return None

def abrir_app_frontend():
    """Abre la aplicación principal unificada con navegación interna"""
    modulo = importar_modulo("app_frontend")
    if modulo:
        try:
            return True
        except Exception as e:
            logging.error(f"Error al iniciar app_frontend: {e}")
            return False
    else:
        logging.error("No se pudo cargar el módulo app_frontend")
        return False

def main():
    """Función principal mejorada"""
    try:
        # Configurar logging
        setup_logging()
        logging.info("Iniciando aplicación")
        
        # Verificar directorios necesarios
        verificar_directorios()
        
        # Inicializar pool de conexiones
        db_manager = DatabaseManager.get_instance()
        if not db_manager.get_connection():
            messagebox.showerror("Error de conexión", "No se pudo conectar a la base de datos.")
            sys.exit(1)
        
        # Intentar abrir la aplicación principal unificada
        if not abrir_app_frontend():
            messagebox.showerror("Error", "No se pudo iniciar la aplicación principal.")
            sys.exit(1)
            
    except Exception as e:
        logging.critical(f"Error crítico al iniciar: {e}")
        messagebox.showerror("Error", f"Error al iniciar la aplicación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()