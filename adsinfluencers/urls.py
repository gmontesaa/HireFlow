"""
URL configuration for adsinfluencers project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from influencers import views as influencers_views
from django.contrib.auth import views as auth_views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', influencers_views.home, name='home'),
    path('about/', influencers_views.about, name='about'),
    path('influencer/<int:pk>/', influencers_views.influencer_detail, name='influencer_detail'),
    path('campaign/create/', influencers_views.create_campaign, name='create_campaign'),
    path('campaign/<int:pk>/', influencers_views.campaign_detail, name='campaign_detail'),
    path('campaign/analytics/', influencers_views.campaign_analytics, name='campaign_analytics'),
    path('analytics/', influencers_views.overall_analytics, name='overall_analytics'),
    
    # URLs de autenticación
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', influencers_views.register, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)