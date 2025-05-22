from django.db.models import Avg, Count, Sum, Max, Q
from django.db.models.functions import TruncMonth
from django.core.exceptions import ValidationError
from django.utils import timezone
from ..models import Campaign, CampaignInfluencer, Review, Influencer

class CampaignService:
    """
    Servicio que maneja la lógica de negocio relacionada con las campañas.
    """
    @staticmethod
    def create_campaign(company, data):
        """
        Crea una nueva campaña.
        
        Args:
            company (User): Usuario que crea la campaña
            data (dict): Datos de la campaña
            
        Returns:
            Campaign: Instancia de la campaña creada
            
        Raises:
            ValidationError: Si los datos no son válidos
        """
        try:
            campaign = Campaign(company=company, **data)
            campaign.full_clean()
            campaign.save()
            return campaign
        except Exception as e:
            raise ValidationError(f"Error al crear la campaña: {str(e)}")

    @staticmethod
    def update_campaign(campaign_id, data):
        """
        Actualiza una campaña existente.
        
        Args:
            campaign_id (int): ID de la campaña
            data (dict): Datos a actualizar
            
        Returns:
            Campaign: Instancia de la campaña actualizada
            
        Raises:
            ValidationError: Si los datos no son válidos
        """
        try:
            campaign = Campaign.objects.get(id=campaign_id)
            for key, value in data.items():
                setattr(campaign, key, value)
            campaign.full_clean()
            campaign.save()
            return campaign
        except Exception as e:
            raise ValidationError(f"Error al actualizar la campaña: {str(e)}")

    @staticmethod
    def add_influencer_to_campaign(campaign_id, influencer_id):
        """
        Agrega un influencer a una campaña.
        
        Args:
            campaign_id (int): ID de la campaña
            influencer_id (int): ID del influencer
            
        Returns:
            CampaignInfluencer: Instancia de la relación creada
            
        Raises:
            ValidationError: Si no se puede agregar el influencer
        """
        try:
            campaign = Campaign.objects.get(id=campaign_id)
            influencer = Influencer.objects.get(id=influencer_id)
            
            if not campaign.can_add_influencer(influencer):
                raise ValidationError("No se puede agregar el influencer a la campaña")
            
            campaign_influencer = CampaignInfluencer.objects.create(
                campaign=campaign,
                influencer=influencer
            )
            return campaign_influencer
        except Exception as e:
            raise ValidationError(f"Error al agregar el influencer: {str(e)}")

    @staticmethod
    def get_campaign_stats(campaign_id):
        """
        Obtiene estadísticas detalladas de una campaña.
        
        Args:
            campaign_id (int): ID de la campaña
            
        Returns:
            dict: Diccionario con estadísticas de la campaña
        """
        campaign = Campaign.objects.get(id=campaign_id)
        campaign_influencers = CampaignInfluencer.objects.filter(campaign=campaign)
        
        return {
            'total_influencers': campaign_influencers.count(),
            'completed_influencers': campaign_influencers.filter(status='completed').count(),
            'pending_influencers': campaign_influencers.filter(status='pending_review').count(),
            'total_spent': campaign_influencers.filter(status='completed').aggregate(
                total=Sum('influencer__price_per_post')
            )['total'] or 0,
            'average_engagement': campaign_influencers.filter(status='completed').aggregate(
                avg=Avg('influencer__engagement_rate')
            )['avg'] or 0,
            'days_remaining': (campaign.end_date - timezone.now().date()).days,
        }

    @staticmethod
    def search_campaigns(query=None, status=None, company=None, start_date=None, end_date=None):
        """
        Busca campañas según los criterios especificados.
        
        Args:
            query (str): Término de búsqueda para nombre o descripción
            status (str): Estado de la campaña
            company (int): ID de la empresa
            start_date (date): Fecha de inicio
            end_date (date): Fecha de fin
            
        Returns:
            QuerySet: Conjunto de campañas que cumplen con los criterios
        """
        queryset = Campaign.objects.all()

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )

        if status:
            queryset = queryset.filter(status=status)

        if company:
            queryset = queryset.filter(company_id=company)

        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)

        if end_date:
            queryset = queryset.filter(end_date__lte=end_date)

        return queryset.distinct()

    @staticmethod
    def get_active_campaigns():
        """
        Obtiene las campañas activas.
        
        Returns:
            QuerySet: Conjunto de campañas activas
        """
        return Campaign.objects.filter(
            status='active',
            start_date__lte=timezone.now().date(),
            end_date__gte=timezone.now().date()
        )

    @staticmethod
    def get_company_campaigns(company):
        """
        Obtiene todas las campañas de una empresa.
        """
        return Campaign.objects.filter(company=company).order_by('-created_at')

    @staticmethod
    def get_campaign_analytics():
        """
        Obtiene estadísticas generales de todas las campañas.
        """
        total_campaigns = Campaign.objects.count()
        active_campaigns = Campaign.objects.filter(status='active').count()
        completed_campaigns = Campaign.objects.filter(status='completed').count()
        cancelled_campaigns = Campaign.objects.filter(status='cancelled').count()
        
        total_budget = Campaign.objects.aggregate(total=Sum('budget'))['total'] or 0
        avg_budget = Campaign.objects.aggregate(avg=Avg('budget'))['avg'] or 0
        max_budget = Campaign.objects.aggregate(max=Max('budget'))['max'] or 0
        
        total_influencers = Influencer.objects.count()
        active_influencers = Influencer.objects.filter(is_available=True).count()
        avg_followers = Influencer.objects.aggregate(avg=Avg('followers'))['avg'] or 0
        avg_engagement = Influencer.objects.aggregate(avg=Avg('engagement_rate'))['avg'] or 0
        
        success_rate = (completed_campaigns / total_campaigns * 100) if total_campaigns > 0 else 0
        
        return {
            'total_campaigns': total_campaigns,
            'active_campaigns': active_campaigns,
            'completed_campaigns': completed_campaigns,
            'cancelled_campaigns': cancelled_campaigns,
            'total_budget': total_budget,
            'avg_budget': avg_budget,
            'max_budget': max_budget,
            'total_influencers': total_influencers,
            'active_influencers': active_influencers,
            'avg_followers': avg_followers,
            'avg_engagement': avg_engagement,
            'success_rate': success_rate,
            'campaigns_by_status': Campaign.objects.values('status').annotate(
                count=Count('id')
            ).order_by('status'),
            'campaigns_by_month': Campaign.objects.annotate(
                month=TruncMonth('created_at')
            ).values('month').annotate(
                count=Count('id')
            ).order_by('month'),
            'top_influencers': CampaignInfluencer.objects.values(
                'influencer__name'
            ).annotate(
                count=Count('id')
            ).order_by('-count')[:5]
        }

    @staticmethod
    def can_add_influencer(campaign, influencer):
        """
        Verifica si se puede agregar un influencer a una campaña.
        """
        if not campaign.can_add_influencer(influencer):
            return False

        if CampaignInfluencer.objects.filter(
            campaign=campaign,
            influencer=influencer
        ).exists():
            return False

        return True 