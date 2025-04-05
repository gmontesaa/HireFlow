from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg, Count
from .models import Influencer, Campaign, CampaignInfluencer
from .forms import CampaignForm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta

# Create your views here.
def home(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    
    influencers = Influencer.objects.filter(is_available=True)
    
    if query:
        influencers = influencers.filter(
            Q(name__icontains=query) |
            Q(username__icontains=query) |
            Q(description__icontains=query)
        )
    
    if category:
        influencers = influencers.filter(category=category)
    
    context = {
        'influencers': influencers,
        'query': query,
        'category': category,
    }
    return render(request, 'influencers/home.html', context)

def influencer_detail(request, pk):
    influencer = get_object_or_404(Influencer, pk=pk)
    return render(request, 'influencers/influencer_detail.html', {'influencer': influencer})

@login_required
def create_campaign(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.company = request.user
            campaign.save()
            messages.success(request, 'Campaña creada exitosamente')
            return redirect('home')
    else:
        form = CampaignForm()
    return render(request, 'influencers/create_campaign.html', {'form': form})

@login_required
def campaign_detail(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk, created_by=request.user)
    campaign_influencers = CampaignInfluencer.objects.filter(campaign=campaign)
    return render(request, 'influencers/campaign_detail.html', {
        'campaign': campaign,
        'campaign_influencers': campaign_influencers
    })

@login_required
def add_influencer_to_campaign(request, campaign_pk, influencer_pk):
    campaign = get_object_or_404(Campaign, pk=campaign_pk, created_by=request.user)
    influencer = get_object_or_404(Influencer, pk=influencer_pk)
    
    if CampaignInfluencer.objects.filter(campaign=campaign, influencer=influencer).exists():
        messages.warning(request, 'Este influencer ya está en la campaña')
    else:
        CampaignInfluencer.objects.create(campaign=campaign, influencer=influencer)
        messages.success(request, 'Influencer agregado a la campaña')
    
    return redirect('campaign_detail', pk=campaign.pk)

def scrape_influencer_data(username, platform):
    driver = webdriver.Chrome()
    try:
        if platform.lower() == 'instagram':
            driver.get(f'https://www.instagram.com/{username}/')
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span._ac2a"))
            )
            followers = driver.find_element(By.CSS_SELECTOR, "span._ac2a").text
            return {
                'followers': followers,
                'engagement_rate': 0.0  # Esto necesitaría un cálculo más complejo
            }
    finally:
        driver.quit()
    return None

def about(request):
    #return HttpResponse('<h1>Welcome To About</h1>')
    return render(request, 'about.html')

@login_required
def campaign_analytics(request):
    # Obtener las campañas del usuario actual
    campaigns = Campaign.objects.filter(company=request.user)
    
    # Datos para las gráficas
    campaign_data = []
    for campaign in campaigns:
        completed_influencers = CampaignInfluencer.objects.filter(
            campaign=campaign,
            status='completed'
        ).count()
        
        total_influencers = CampaignInfluencer.objects.filter(
            campaign=campaign
        ).count()
        
        completion_rate = (completed_influencers / total_influencers * 100) if total_influencers > 0 else 0
        
        campaign_data.append({
            'name': campaign.name,
            'completion_rate': completion_rate,
            'budget': float(campaign.budget),
            'status': campaign.status,
            'start_date': campaign.start_date,
            'end_date': campaign.end_date
        })
    
    context = {
        'campaign_data': campaign_data,
        'title': 'Análisis de Campañas'
    }
    return render(request, 'influencers/campaign_analytics.html', context)

@login_required
def overall_analytics(request):
    # Estadísticas generales de todas las campañas
    total_campaigns = Campaign.objects.count()
    active_campaigns = Campaign.objects.filter(status='active').count()
    completed_campaigns = Campaign.objects.filter(status='completed').count()
    
    # Promedio de presupuesto por campaña
    avg_budget = Campaign.objects.aggregate(avg_budget=Avg('budget'))['avg_budget'] or 0
    
    # Tasa de éxito promedio
    success_rate = CampaignInfluencer.objects.filter(status='completed').count() / \
                  CampaignInfluencer.objects.count() * 100 if CampaignInfluencer.objects.count() > 0 else 0
    
    # Distribución por categoría
    category_distribution = Influencer.objects.values('category').annotate(
        count=Count('id')
    )
    
    context = {
        'total_campaigns': total_campaigns,
        'active_campaigns': active_campaigns,
        'completed_campaigns': completed_campaigns,
        'avg_budget': avg_budget,
        'success_rate': success_rate,
        'category_distribution': category_distribution,
        'title': 'Estadísticas Generales'
    }
    return render(request, 'influencers/overall_analytics.html', context)