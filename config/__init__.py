"""
Configuración del proyecto AdsInfluencers.

Este archivo inicializa la configuración del proyecto y configura Celery
de manera opcional para evitar errores durante el desarrollo.
"""

# Configuración de Celery (opcional)
try:
    from .celery import app as celery_app
    __all__ = ('celery_app',)
except ImportError:
    # Si Celery no está instalado, no hacemos nada
    pass 