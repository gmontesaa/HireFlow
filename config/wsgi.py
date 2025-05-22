"""
Configuración WSGI para el proyecto AdsInfluencers.

Este archivo contiene la configuración WSGI (Web Server Gateway Interface) que
actúa como punto de entrada para servidores web compatibles con WSGI.

Funcionalidades principales:
1. Configuración del entorno de Django
2. Configuración de variables de entorno
3. Inicialización de la aplicación WSGI

Notas importantes:
- Este archivo es utilizado por servidores web como Gunicorn, uWSGI, etc.
- En producción, asegúrese de que DEBUG = False en settings.py
- Las variables de entorno deben estar configuradas en el servidor
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Importar la aplicación WSGI de Django
from django.core.wsgi import get_wsgi_application

# Configuración del entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Inicialización de la aplicación WSGI
application = get_wsgi_application() 