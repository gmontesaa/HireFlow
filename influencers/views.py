from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg, Count, Sum, Max
from django.db.models.functions import TruncMonth
from .models import Influencer, Campaign, CampaignInfluencer, Review, Category
from .forms import CampaignForm, InfluencerForm, ScrapingForm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
from .n8n_integration import N8NIntegration
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .services.influencer_service import InfluencerService
from .services.campaign_service import CampaignService
from .services.review_service import ReviewService
from .services.n8n_service import N8NService
from .services.scraping_service import ScrapingService
from .services.message_service import MessageService
from django.utils import timezone

# Create your views here.
def home(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    
    influencers = InfluencerService.search_influencers(
        query=query,
        category=category
    )
    categories = Category.objects.all()
    
    context = {
        'influencers': influencers,
        'categories': categories,
        'query': query,
        'selected_category': category,
    }
    return render(request, 'influencers/home.html', context)

def influencer_detail(request, pk):
    influencer = get_object_or_404(Influencer, pk=pk)
    reviews = ReviewService.get_influencer_reviews(influencer)
    rating = ReviewService.get_influencer_rating(influencer)
    
    context = {
        'influencer': influencer,
        'reviews': reviews,
        'rating': rating
    }
    return render(request, 'influencers/influencer_detail.html', context)

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
    campaign = get_object_or_404(Campaign, pk=pk, company=request.user)
    campaign_influencers = CampaignInfluencer.objects.filter(campaign=campaign)
    reviews = ReviewService.get_campaign_reviews(campaign)
    stats = CampaignService.get_campaign_stats(campaign)
    rating = ReviewService.get_campaign_rating(campaign)
    
    context = {
        'campaign': campaign,
        'campaign_influencers': campaign_influencers,
        'reviews': reviews,
        'stats': stats,
        'rating': rating
    }
    return render(request, 'influencers/campaign_detail.html', context)

@login_required
@require_POST
def add_influencer_to_campaign(request, campaign_pk, influencer_pk):
    campaign = get_object_or_404(Campaign, pk=campaign_pk, company=request.user)
    influencer = get_object_or_404(Influencer, pk=influencer_pk)
    
    if not CampaignService.can_add_influencer(campaign, influencer):
        messages.warning(request, 'No se puede agregar este influencer a la campaña')
        return redirect('campaign_detail', pk=campaign.pk)
    
    campaign_influencer = CampaignInfluencer.objects.create(
        campaign=campaign,
        influencer=influencer,
        status='pending_review'
    )
    
    # Enviar a revisión de Hireflow
    n8n_service = N8NService()
    review_result = n8n_service.send_to_hireflow_review(campaign_influencer)
    
    if review_result:
        messages.success(request, 'Influencer agregado a la campaña y enviado a revisión')
    else:
        messages.error(request, 'Error al enviar a revisión. Por favor, intente nuevamente')
    
    return redirect('campaign_detail', pk=campaign.pk)

@login_required
@require_POST
def process_hireflow_review(request):
    try:
        data = json.loads(request.body)
        campaign_influencer_id = data.get('campaign_influencer_id')
        is_approved = data.get('is_approved')
        review_notes = data.get('review_notes')
        
        campaign_influencer = get_object_or_404(CampaignInfluencer, id=campaign_influencer_id)
        
        if is_approved:
            campaign_influencer.status = 'review_approved'
            campaign_influencer.review_notes = review_notes
            campaign_influencer.save()
            
            # Enviar mensaje al influencer
            n8n_service = N8NService()
            message_result = n8n_service.send_message_to_influencer(campaign_influencer)
            
            if message_result:
                return JsonResponse({'status': 'success', 'message': 'Revisión aprobada y mensaje enviado'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Error al enviar mensaje al influencer'})
        else:
            campaign_influencer.status = 'review_rejected'
            campaign_influencer.review_notes = review_notes
            campaign_influencer.save()
            return JsonResponse({'status': 'success', 'message': 'Revisión rechazada'})
            
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
@require_POST
def scrape_influencer_data(request):
    """Endpoint para obtener datos de un influencer mediante scraping."""
    try:
        username = request.POST.get('username')
        platform = request.POST.get('platform')
        
        if not username or not platform:
            return JsonResponse({
                'status': 'error',
                'message': 'Se requiere username y platform'
            })
        
        if platform == 'instagram':
            data = ScrapingService.scrape_instagram_data(username)
        elif platform == 'tiktok':
            data = ScrapingService.scrape_tiktok_data(username)
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Plataforma no soportada'
            })
        
        if data:
            # Crear o actualizar influencer
            influencer, created = Influencer.objects.update_or_create(
                username=username,
                platform=platform,
                defaults={
                    'name': data['name'],
                    'description': data['bio'],
                    'followers': data['followers'],
                    'engagement_rate': data['engagement_rate'],
                    'price_per_post': data['price_per_post']
                }
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Influencer creado/actualizado exitosamente',
                'data': {
                    'id': influencer.id,
                    'name': influencer.name,
                    'username': influencer.username,
                    'platform': influencer.platform,
                    'followers': influencer.followers,
                    'engagement_rate': influencer.engagement_rate,
                    'price_per_post': influencer.price_per_post
                }
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'No se pudieron obtener los datos del influencer'
            })
            
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

def about(request):
    #return HttpResponse('<h1>Welcome To About</h1>')
    return render(request, 'about.html')

@login_required
def campaign_analytics(request):
    campaigns = CampaignService.get_company_campaigns(request.user)
    campaign_data = []
    
    for campaign in campaigns:
        stats = CampaignService.get_campaign_stats(campaign)
        campaign_data.append({
            'name': campaign.name,
            'completion_rate': (stats['completed_influencers'] / stats['total_influencers'] * 100) if stats['total_influencers'] > 0 else 0,
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
    context = CampaignService.get_campaign_analytics()
    context['title'] = 'Estadísticas Generales'
    return render(request, 'influencers/overall_analytics.html', context)

@login_required
def add_review(request, campaign_id, influencer_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    influencer = get_object_or_404(Influencer, id=influencer_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        review = ReviewService.create_review(
            campaign=campaign,
            influencer=influencer,
            company=request.user,
            rating=rating,
            comment=comment
        )
        
        messages.success(request, 'Reseña agregada exitosamente')
        return redirect('campaign_detail', pk=campaign_id)
    
    return render(request, 'influencers/add_review.html', {
        'campaign': campaign,
        'influencer': influencer
    })

@login_required
def advanced_search(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category')
    min_followers = request.GET.get('min_followers')
    max_followers = request.GET.get('max_followers')
    min_engagement = request.GET.get('min_engagement')
    max_engagement = request.GET.get('max_engagement')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    location = request.GET.get('location')
    
    influencers = InfluencerService.search_influencers(
        query=query,
        category=category,
        min_followers=min_followers,
        max_followers=max_followers,
        min_engagement=min_engagement,
        max_engagement=max_engagement,
        min_price=min_price,
        max_price=max_price,
        location=location
    )
    
    categories = Category.objects.all()
    
    context = {
        'influencers': influencers,
        'categories': categories,
        'query': query,
        'selected_category': category,
        'min_followers': min_followers,
        'max_followers': max_followers,
        'min_engagement': min_engagement,
        'max_engagement': max_engagement,
        'min_price': min_price,
        'max_price': max_price,
        'location': location
    }
    return render(request, 'influencers/advanced_search.html', context)

@login_required
def support(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        priority = request.POST.get('priority')
        
        messages.success(request, 'Tu solicitud de soporte ha sido enviada. Te contactaremos pronto.')
        return redirect('support')
    
    return render(request, 'influencers/support.html')

@login_required
def faq(request):
    faqs = [
        {
            'question': '¿Cómo puedo contratar a un influencer?',
            'answer': 'Para contratar a un influencer, primero debes crear una campaña y luego seleccionar los influencers que deseas contactar.'
        },
        {
            'question': '¿Cómo se calcula el precio por publicación?',
            'answer': 'El precio por publicación se basa en varios factores como el número de seguidores, la tasa de engagement y la categoría del influencer.'
        },
        {
            'question': '¿Qué sucede si un influencer no cumple con lo acordado?',
            'answer': 'Todas las campañas tienen términos y condiciones claros. Si hay incumplimiento, puedes reportarlo y nuestro equipo lo revisará.'
        },
        {
            'question': '¿Cómo puedo medir el éxito de mi campaña?',
            'answer': 'Puedes acceder a las métricas de tu campaña en el dashboard, donde encontrarás información sobre alcance, engagement y ROI.'
        }
    ]
    
    return render(request, 'influencers/faq.html', {'faqs': faqs})

@login_required
def create_influencer(request):
    """Vista para crear un nuevo influencer."""
    if request.method == 'POST':
        form = InfluencerForm(request.POST)
        if form.is_valid():
            influencer = form.save()
            messages.success(request, 'Influencer creado exitosamente')
            return redirect('influencer_detail', pk=influencer.pk)
    else:
        form = InfluencerForm()
    
    return render(request, 'influencers/create_influencer.html', {
        'form': form,
        'title': 'Crear Influencer'
    })

@login_required
def add_influencer(request):
    """Vista para agregar un influencer mediante scraping."""
    if request.method == 'POST':
        form = ScrapingForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            platform = form.cleaned_data['platform']
            
            if platform == 'instagram':
                data = ScrapingService.scrape_instagram_data(username)
            else:
                data = ScrapingService.scrape_tiktok_data(username)
            
            if data:
                # Crear o actualizar influencer
                influencer, created = Influencer.objects.update_or_create(
                    username=username,
                    platform=platform,
                    defaults={
                        'name': data['name'],
                        'description': data['bio'],
                        'followers': data['followers'],
                        'engagement_rate': data['engagement_rate'],
                        'price_per_post': data['price_per_post']
                    }
                )
                
                messages.success(request, 'Influencer agregado exitosamente')
                return redirect('influencer_detail', pk=influencer.pk)
            else:
                messages.error(request, 'No se pudieron obtener los datos del influencer')
    else:
        form = ScrapingForm()
    
    return render(request, 'influencers/add_influencer.html', {
        'form': form,
        'title': 'Agregar Influencer'
    })

@login_required
def send_message(request, campaign_id, influencer_id):
    """
    Vista para enviar mensajes a influencers.
    """
    campaign_influencer = get_object_or_404(
        CampaignInfluencer,
        campaign_id=campaign_id,
        influencer_id=influencer_id,
        campaign__company=request.user.company
    )
    
    if request.method == 'POST':
        # Actualizar el estado y la fecha de envío
        campaign_influencer.status = 'message_sent'
        campaign_influencer.message_sent_date = timezone.now()
        campaign_influencer.save()
        
        messages.success(request, 'Mensaje marcado como enviado correctamente.')
        return redirect('campaign_detail', campaign_id=campaign_id)
    
    # Obtener el contexto del mensaje
    context = MessageService.get_message_context(campaign_influencer)
    
    return render(request, 'influencers/send_message.html', context)