# config.py
import os
from pathlib import Path

# Rutas de directorios
BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = os.path.join(BASE_DIR, "imagenes")

# Configuración de la base de datos
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",
    "database": "gestionbebidas"
}

# Colores de la interfaz
UI_COLORS = {
    "FONDO_PRINCIPAL": "#1A1A2E",
    "FONDO_SECUNDARIO": "#16213E",
    "ACENTO": "#0F3460",
    "RESALTE": "#E94560",
    "TEXTO_CLARO": "#FFFFFF",
    "TEXTO_OSCURO": "#1A1A2E", 
    "BOTON": "#0F3460",
    "BOTON_HOVER": "#E94560",
    "BORDES": "#533483"
}

# Configuración de la aplicación
APP_CONFIG = {
    "NOMBRE": "Sistema de Gestión de Bebidas - LOS TIOS",
    "VERSION": "1.0.0",
    "VENTANA_PRINCIPAL_SIZE": "800x600",
    "ICON_PATH": os.path.join(BASE_DIR, "imagen", "icon.ico")
}

# Sistema de logging
LOG_CONFIG = {
    "LOG_FILE": os.path.join(BASE_DIR, "logs", "app.log"),
    "LOG_LEVEL": "INFO"
}