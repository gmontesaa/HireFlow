from django.db.models import Avg, Count, Sum, Max
from django.db.models.functions import TruncMonth
from django.utils import timezone
from ..models import Campaign, CampaignInfluencer, Review, Influencer

class CampaignService:
    @staticmethod
    def get_campaign_stats(campaign):
        """
        Obtiene estadísticas de una campaña.
        """
        total_influencers = campaign.influencers.count()
        completed_influencers = CampaignInfluencer.objects.filter(
            campaign=campaign,
            status='completed'
        ).count()
        
        return {
            'total_influencers': total_influencers,
            'completed_influencers': completed_influencers,
            'completion_rate': (completed_influencers / total_influencers * 100) if total_influencers > 0 else 0,
            'total_spent': campaign.total_spent,
            'average_rating': Review.objects.filter(
                campaign=campaign
            ).aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0,
            'days_remaining': (campaign.end_date - timezone.now().date()).days,
            'status': campaign.status,
            'budget': float(campaign.budget),
            'start_date': campaign.start_date,
            'end_date': campaign.end_date
        }

    @staticmethod
    def get_company_campaigns(company):
        """
        Obtiene todas las campañas de una empresa.
        """
        return Campaign.objects.filter(company=company).order_by('-created_at')

    @staticmethod
    def get_active_campaigns():
        """
        Obtiene todas las campañas activas.
        """
        return Campaign.objects.filter(status='active')

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