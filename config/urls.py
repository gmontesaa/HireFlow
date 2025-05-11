from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from influencers import views as influencers_views
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', influencers_views.home, name='home'),
    path('about/', influencers_views.about, name='about'),
    path('influencer/<int:pk>/', influencers_views.influencer_detail, name='influencer_detail'),
    path('influencer/create/', influencers_views.create_influencer, name='create_influencer'),
    path('influencer/add/', influencers_views.add_influencer, name='add_influencer'),
    path('campaign/create/', influencers_views.create_campaign, name='create_campaign'),
    path('campaign/<int:pk>/', influencers_views.campaign_detail, name='campaign_detail'),
    path('campaign/<int:campaign_pk>/add-influencer/<int:influencer_pk>/', influencers_views.add_influencer_to_campaign, name='add_influencer_to_campaign'),
    path('campaign/analytics/', influencers_views.campaign_analytics, name='campaign_analytics'),
    path('analytics/', influencers_views.overall_analytics, name='overall_analytics'),
    path('campaign/<int:campaign_id>/influencer/<int:influencer_id>/review/', influencers_views.add_review, name='add_review'),
    path('search/', influencers_views.advanced_search, name='advanced_search'),
    path('support/', influencers_views.support, name='support'),
    path('faq/', influencers_views.faq, name='faq'),
    path('api/hireflow/review/', influencers_views.process_hireflow_review, name='process_hireflow_review'),
    path('api/scrape-influencer/', influencers_views.scrape_influencer_data, name='scrape_influencer_data'),
    
    # URLs de autenticación
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', accounts_views.register, name='register'),
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 