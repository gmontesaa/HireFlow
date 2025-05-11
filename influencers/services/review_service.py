from django.db.models import Avg
from ..models import Review, Campaign, Influencer

class ReviewService:
    @staticmethod
    def get_campaign_reviews(campaign):
        """Obtiene todas las reseñas de una campaña."""
        return Review.objects.filter(campaign=campaign).select_related('influencer', 'company')
    
    @staticmethod
    def get_influencer_reviews(influencer):
        """Obtiene todas las reseñas de un influencer."""
        return Review.objects.filter(influencer=influencer).select_related('campaign', 'company')
    
    @staticmethod
    def get_influencer_rating(influencer):
        """Calcula el rating promedio de un influencer."""
        return Review.objects.filter(influencer=influencer).aggregate(
            avg_rating=Avg('rating')
        )['avg_rating'] or 0
    
    @staticmethod
    def create_review(campaign, influencer, company, rating, comment):
        """Crea una nueva reseña."""
        return Review.objects.create(
            campaign=campaign,
            influencer=influencer,
            company=company,
            rating=rating,
            comment=comment
        )
    
    @staticmethod
    def get_top_rated_influencers(limit=5):
        """Obtiene los influencers mejor calificados."""
        return Influencer.objects.annotate(
            avg_rating=Avg('reviews__rating')
        ).filter(
            avg_rating__isnull=False
        ).order_by('-avg_rating')[:limit]
    
    @staticmethod
    def get_campaign_rating(campaign):
        """Calcula el rating promedio de una campaña."""
        return Review.objects.filter(campaign=campaign).aggregate(
            avg_rating=Avg('rating')
        )['avg_rating'] or 0 