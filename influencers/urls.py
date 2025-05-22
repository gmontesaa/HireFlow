from django.urls import path
from . import views

app_name = 'influencers'

urlpatterns = [
    # URLs públicas
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('influencer/<slug:slug>/', views.influencer_detail, name='influencer_detail'),
    path('search/', views.advanced_search, name='advanced_search'),
    
    # URLs de campañas (requieren autenticación)
    path('campaigns/', views.campaign_list, name='campaign_list'),
    path('campaigns/create/', views.campaign_create, name='campaign_create'),
    path('campaigns/<int:campaign_id>/', views.campaign_detail, name='campaign_detail'),
    path('campaigns/<int:campaign_id>/edit/', views.campaign_edit, name='campaign_edit'),
    path('campaigns/analytics/', views.campaign_analytics, name='campaign_analytics'),
    path(
        'campaigns/<int:campaign_id>/add-influencer/',
        views.add_influencer_to_campaign,
        name='add_influencer_to_campaign'
    ),
    
    # URLs de reseñas (requieren autenticación)
    path(
        'campaigns/<int:campaign_id>/influencer/<int:influencer_id>/review/',
        views.create_review,
        name='create_review'
    ),
    
    # URLs de mensajes (requieren autenticación)
    path(
        'campaign-influencer/<int:campaign_influencer_id>/send-message/',
        views.send_message,
        name='send_message'
    ),
    
    # URLs de scraping (requieren autenticación)
    path('scrape/', views.scrape_influencer, name='scrape_influencer'),
] 