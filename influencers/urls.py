from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('influencer/<int:pk>/', views.influencer_detail, name='influencer_detail'),
    path('campaign/create/', views.create_campaign, name='create_campaign'),
    path('campaign/<int:pk>/', views.campaign_detail, name='campaign_detail'),
    path('campaign/<int:campaign_pk>/add-influencer/<int:influencer_pk>/', 
         views.add_influencer_to_campaign, name='add_influencer_to_campaign'),
    path('analytics/campaigns/', views.campaign_analytics, name='campaign_analytics'),
    path('analytics/overall/', views.overall_analytics, name='overall_analytics'),
    path('about/', views.about, name='about'),
    path('campaign/<int:campaign_id>/influencer/<int:influencer_id>/send-message/',
         views.send_message,
         name='send_message'),
] 