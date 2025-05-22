"""
Configuración ASGI para el proyecto AdsInfluencers.

Este archivo contiene la configuración ASGI (Asynchronous Server Gateway Interface) que
actúa como punto de entrada para servidores web asíncronos.

Funcionalidades principales:
1. Configuración del entorno de Django
2. Configuración de variables de entorno
3. Inicialización de la aplicación ASGI
4. Soporte para WebSockets y aplicaciones asíncronas

Notas importantes:
- Este archivo es utilizado por servidores web como Daphne, Uvicorn, etc.
- En producción, asegúrese de que DEBUG = False en settings.py
- Las variables de entorno deben estar configuradas en el servidor
- ASGI permite manejar conexiones WebSocket y otras características asíncronas
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

# Cargar variables de entorno desde el archivo .env
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Establecer la variable de entorno para el módulo de configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Inicializar la aplicación ASGI de Django temprano para asegurar que la app esté cargada
django_asgi_app = get_asgi_application()

# Configurar el enrutador de protocolos para manejar diferentes tipos de conexiones
application = ProtocolTypeRouter({
    # Manejar conexiones HTTP estándar
    "http": django_asgi_app,
    
    # Configuración de WebSocket (comentada por ahora)
    # "websocket": AllowedHostsOriginValidator(
    #     AuthMiddlewareStack(
    #         URLRouter(
    #             # Aquí irían las rutas de websocket
    #         )
    #     )
    # ),
}) 