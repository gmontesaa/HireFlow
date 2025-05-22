"""
Configuración principal del proyecto AdsInfluencers.

Este archivo contiene todas las configuraciones necesarias para el funcionamiento
del proyecto, incluyendo:

1. Configuración de la base de datos:
   - Conexión a la base de datos
   - Validación de contraseñas
   - Configuración de modelos

2. Configuración de seguridad:
   - Clave secreta
   - Configuración de SSL/TLS
   - Protección contra ataques comunes
   - Configuración de cookies seguras

3. Configuración de aplicaciones:
   - Aplicaciones de Django core
   - Aplicaciones de terceros
   - Aplicaciones locales del proyecto

4. Configuración de archivos:
   - Archivos estáticos (CSS, JS, imágenes)
   - Archivos de medios (subidos por usuarios)
   - Configuración de templates

5. Configuración de email:
   - Servidor SMTP
   - Credenciales
   - Configuración de TLS

6. Integraciones externas:
   - N8N para automatización
   - Instagram API para scraping
   - Celery para tareas asíncronas

7. Configuración de logging:
   - Niveles de log
   - Formato de mensajes
   - Destinos de log (consola y archivo)

8. Configuración de internacionalización:
   - Idioma
   - Zona horaria
   - Formato de fechas y números

Nota: Las variables sensibles se cargan desde el archivo .env
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-default-key-for-development')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

# Lista de hosts permitidos
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    # Django core apps - Aplicaciones esenciales de Django
    'django.contrib.admin',  # Panel de administración
    'django.contrib.auth',   # Sistema de autenticación
    'django.contrib.contenttypes',  # Framework de tipos de contenido
    'django.contrib.sessions',  # Framework de sesiones
    'django.contrib.messages',  # Framework de mensajes
    'django.contrib.staticfiles',  # Gestión de archivos estáticos
    'django.contrib.humanize',  # Filtros para formateo de números y fechas
    
    # Third party apps - Aplicaciones de terceros
    'crispy_forms',  # Mejora la presentación de formularios
    'crispy_bootstrap5',  # Tema Bootstrap 5 para crispy forms
    'django_celery_beat',  # Programación de tareas periódicas
    'django_celery_results',  # Almacenamiento de resultados de tareas
    
    # Local apps - Aplicaciones del proyecto
    'accounts',  # Gestión de usuarios y autenticación
    'influencers',  # Gestión de influencers y campañas
]

# Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL Configuration
ROOT_URLCONF = 'config.urls'

# Template Configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI Configuration
WSGI_APPLICATION = 'config.wsgi.application'

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms Configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Login/Logout URLs
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

# Email Configuration
# Configuración del servidor de correo electrónico para envío de notificaciones
# y comunicación con usuarios
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')  # Servidor SMTP
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))  # Puerto SMTP
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'  # Usar TLS
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')  # Usuario SMTP
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')  # Contraseña SMTP
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@adsinfluencers.com')  # Email por defecto

# Security settings
# Configuraciones de seguridad que se activan en producción
if not DEBUG:
    SECURE_SSL_REDIRECT = True  # Redirigir todo el tráfico a HTTPS
    SESSION_COOKIE_SECURE = True  # Cookies de sesión solo por HTTPS
    CSRF_COOKIE_SECURE = True  # Cookies CSRF solo por HTTPS
    SECURE_BROWSER_XSS_FILTER = True  # Filtro XSS del navegador
    SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevenir sniffing de tipo de contenido
    X_FRAME_OPTIONS = 'DENY'  # Prevenir clickjacking
    SECURE_HSTS_SECONDS = 31536000  # HSTS por 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Incluir subdominios en HSTS
    SECURE_HSTS_PRELOAD = True  # Precargar HSTS

# N8N Integration Configuration
# Configuración para la integración con N8N para automatización de flujos de trabajo
N8N_BASE_URL = os.getenv('N8N_BASE_URL', 'http://localhost:5678')  # URL base de N8N
N8N_API_KEY = os.getenv('N8N_API_KEY')  # Clave API de N8N
N8N_CAMPAIGN_MESSAGE_WORKFLOW_ID = os.getenv('N8N_CAMPAIGN_MESSAGE_WORKFLOW_ID')  # ID del flujo de mensajes
N8N_INFLUENCER_DATA_WORKFLOW_ID = os.getenv('N8N_INFLUENCER_DATA_WORKFLOW_ID')  # ID del flujo de datos
N8N_HIREFLOW_REVIEW_WORKFLOW_ID = os.getenv('N8N_HIREFLOW_REVIEW_WORKFLOW_ID')  # ID del flujo de revisiones

# Instagram API Configuration
# Credenciales para la API de Instagram (usadas en scraping)
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')  # Usuario de Instagram
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')  # Contraseña de Instagram

# Logging Configuration
# Configuración del sistema de logging para seguimiento de errores y eventos
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {  # Log en consola
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {  # Log en archivo
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/debug.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {  # Logs de Django
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'influencers': {  # Logs de la app influencers
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Celery Configuration
CELERY_BROKER_URL = 'django://'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler' 