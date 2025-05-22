"""
Configuración de URLs del proyecto AdsInfluencers.

Este archivo define todas las rutas URL del proyecto, organizadas en las siguientes secciones:

1. URLs del Panel de Administración:
   - /admin/ - Panel de administración de Django
   - Personalización del sitio de administración

2. URLs de Autenticación:
   - /accounts/ - Gestión de cuentas de usuario
   - /login/ - Inicio de sesión
   - /logout/ - Cierre de sesión
   - /register/ - Registro de nuevos usuarios

3. URLs de la Aplicación Principal:
   - / - Página principal
   - /influencers/ - Gestión de influencers
   - /campaigns/ - Gestión de campañas
   - /analytics/ - Análisis y estadísticas

4. URLs de Páginas Estáticas:
   - /about/ - Acerca de
   - /terms/ - Términos y condiciones
   - /privacy/ - Política de privacidad

5. URLs de Desarrollo:
   - /__debug__/ - Debug toolbar (solo en desarrollo)
   - Archivos estáticos y media (solo en desarrollo)

Nota: Las URLs sensibles están protegidas con decoradores de autenticación
y permisos apropiados.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from influencers import views as influencers_views
from accounts import views as accounts_views
from django.views.generic import TemplateView

# Definición de patrones de URL
urlpatterns = [
    # Admin URLs - Panel de administración de Django
    path('admin/', admin.site.urls),
    
    # Authentication URLs - URLs para autenticación de usuarios
    path('accounts/', include('accounts.urls')),
    
    # Main app URLs - URLs de la aplicación principal de influencers
    path('', include('influencers.urls')),
    
    # Static pages - Páginas estáticas del sitio
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('terms/', TemplateView.as_view(template_name='terms.html'), name='terms'),
    path('privacy/', TemplateView.as_view(template_name='privacy.html'), name='privacy'),
]

# Configuración para desarrollo
if settings.DEBUG:
    # Servir archivos estáticos y media en desarrollo
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Debug toolbar - Herramienta de depuración
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

# Personalización del sitio de administración
admin.site.site_header = 'AdsInfluencers Admin'
admin.site.site_title = 'AdsInfluencers Admin Portal'
admin.site.index_title = 'Bienvenido al Portal de Administración de AdsInfluencers'

# URLs de autenticación adicionales
urlpatterns += [
    # Login - Vista de inicio de sesión personalizada
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    
    # Logout - Vista de cierre de sesión con redirección a home
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Register - Vista de registro de usuarios con validación personalizada
    path('register/', accounts_views.register, name='register'),
]

# URLs de influencers
urlpatterns += [
    # Detalle de influencer - Vista detallada de un influencer específico
    path('influencer/<int:pk>/', influencers_views.influencer_detail, name='influencer_detail'),
    
    # Creación de influencer - Formulario para crear nuevo influencer
    path('influencer/create/', influencers_views.create_influencer, name='create_influencer'),
    
    # Agregar influencer mediante scraping - Integración con Instagram
    path('influencer/add/', influencers_views.add_influencer, name='add_influencer'),
    
    # Creación de campaña - Formulario para crear nueva campaña
    path('campaign/create/', influencers_views.campaign_create, name='campaign_create'),
    
    # Detalle de campaña - Vista detallada de una campaña específica
    path('campaign/<int:pk>/', influencers_views.campaign_detail, name='campaign_detail'),
    
    # Agregar influencer a campaña - Asociación de influencer con campaña
    path('campaign/<int:campaign_pk>/add-influencer/<int:influencer_pk>/', 
         influencers_views.add_influencer_to_campaign, name='add_influencer_to_campaign'),
    
    # Análisis de campañas - Estadísticas y métricas de campañas
    path('campaign/analytics/', influencers_views.campaign_analytics, name='campaign_analytics'),
    
    # Análisis general - Estadísticas globales del sistema
    path('analytics/', influencers_views.overall_analytics, name='overall_analytics'),
    
    # Agregar reseña - Formulario para calificar a un influencer
    path('campaign/<int:campaign_id>/influencer/<int:influencer_id>/review/', 
         influencers_views.add_review, name='add_review'),
    
    # Búsqueda avanzada - Filtros y búsqueda de influencers
    path('search/', influencers_views.advanced_search, name='advanced_search'),
    
    # Soporte - Página de soporte y ayuda
    path('support/', influencers_views.support, name='support'),
    
    # FAQ - Preguntas frecuentes
    path('faq/', influencers_views.faq, name='faq'),
] 