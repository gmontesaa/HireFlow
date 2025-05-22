"""
Configuración de Celery para el proyecto AdsInfluencers.

Este archivo contiene la configuración de Celery, un sistema de colas de tareas
distribuidas que permite ejecutar tareas asíncronas y programadas.

Funcionalidades principales:
1. Configuración del broker de mensajes (Redis)
2. Configuración del backend de resultados
3. Configuración de tareas periódicas
4. Configuración de timeouts y reintentos

Tareas programadas:
- Actualización diaria de métricas de influencers
- Envío de notificaciones
- Limpieza de datos temporales
- Sincronización con APIs externas

Notas importantes:
- Requiere Redis como broker de mensajes
- Las tareas asíncronas mejoran el rendimiento de la aplicación
- Las tareas programadas se ejecutan según la configuración en settings.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Cargar variables de entorno desde el archivo .env
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Establecer la variable de entorno predeterminada de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Crear la instancia de la aplicación Celery
app = Celery('adsinfluencersproject')

# Cargar la configuración desde el archivo settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Cargar tareas de todas las aplicaciones registradas
app.autodiscover_tasks()

# Configuración de tareas periódicas
app.conf.beat_schedule = {
    'actualizar-metricas-diarias': {
        'task': 'influencers.tasks.actualizar_metricas_influencers',
        'schedule': crontab(hour=0, minute=0),  # Ejecutar a medianoche
    },
    'enviar-notificaciones': {
        'task': 'influencers.tasks.enviar_notificaciones_pendientes',
        'schedule': crontab(minute='*/30'),  # Ejecutar cada 30 minutos
    },
    'limpiar-datos-temporales': {
        'task': 'influencers.tasks.limpiar_datos_temporales',
        'schedule': crontab(hour=3, minute=0),  # Ejecutar a las 3 AM
    },
    'sincronizar-apis': {
        'task': 'influencers.tasks.sincronizar_apis_externas',
        'schedule': crontab(hour='*/4'),  # Ejecutar cada 4 horas
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """
    Tarea de depuración para verificar que Celery está funcionando correctamente.
    """
    print(f'Request: {self.request!r}') 