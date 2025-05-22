from django.db.models import Avg, Count
from django.core.exceptions import ValidationError
from ..models import Review, Campaign, Influencer

class ReviewService:
    """
    Servicio que maneja la lógica de negocio relacionada con las reseñas.
    """
    @staticmethod
    def create_review(company, campaign_id, influencer_id, data):
        """
        Crea una nueva reseña.
        
        Args:
            company (User): Usuario que crea la reseña
            campaign_id (int): ID de la campaña
            influencer_id (int): ID del influencer
            data (dict): Datos de la reseña
            
        Returns:
            Review: Instancia de la reseña creada
            
        Raises:
            ValidationError: Si los datos no son válidos o ya existe una reseña
        """
        try:
            campaign = Campaign.objects.get(id=campaign_id)
            influencer = Influencer.objects.get(id=influencer_id)
            
            # Verificar si ya existe una reseña
            if Review.objects.filter(
                campaign=campaign,
                influencer=influencer,
                company=company
            ).exists():
                raise ValidationError("Ya existe una reseña para esta campaña e influencer")
            
            review = Review(
                company=company,
                campaign=campaign,
                influencer=influencer,
                **data
            )
            review.full_clean()
            review.save()
            return review
        except Exception as e:
            raise ValidationError(f"Error al crear la reseña: {str(e)}")

    @staticmethod
    def update_review(review_id, data):
        """
        Actualiza una reseña existente.
        
        Args:
            review_id (int): ID de la reseña
            data (dict): Datos a actualizar
            
        Returns:
            Review: Instancia de la reseña actualizada
            
        Raises:
            ValidationError: Si los datos no son válidos
        """
        try:
            review = Review.objects.get(id=review_id)
            for key, value in data.items():
                setattr(review, key, value)
            review.full_clean()
            review.save()
            return review
        except Exception as e:
            raise ValidationError(f"Error al actualizar la reseña: {str(e)}")

    @staticmethod
    def get_influencer_reviews(influencer_id):
        """
        Obtiene todas las reseñas de un influencer.
        
        Args:
            influencer_id (int): ID del influencer
            
        Returns:
            QuerySet: Conjunto de reseñas del influencer
        """
        return Review.objects.filter(influencer_id=influencer_id).order_by('-created_at')

    @staticmethod
    def get_influencer_rating_stats(influencer_id):
        """
        Obtiene estadísticas de calificaciones de un influencer.
        
        Args:
            influencer_id (int): ID del influencer
            
        Returns:
            dict: Diccionario con estadísticas de calificaciones
        """
        reviews = Review.objects.filter(influencer_id=influencer_id)
        
        return {
            'average_rating': reviews.aggregate(Avg('rating'))['rating__avg'] or 0,
            'total_reviews': reviews.count(),
            'rating_distribution': reviews.values('rating').annotate(
                count=Count('id')
            ).order_by('rating'),
            'positive_reviews': reviews.filter(rating__gte=4).count(),
            'negative_reviews': reviews.filter(rating__lte=2).count(),
        }

    @staticmethod
    def get_campaign_reviews(campaign_id):
        """
        Obtiene todas las reseñas de una campaña.
        
        Args:
            campaign_id (int): ID de la campaña
            
        Returns:
            QuerySet: Conjunto de reseñas de la campaña
        """
        return Review.objects.filter(campaign_id=campaign_id).order_by('-created_at')

    @staticmethod
    def get_company_reviews(company_id):
        """
        Obtiene todas las reseñas realizadas por una empresa.
        
        Args:
            company_id (int): ID de la empresa
            
        Returns:
            QuerySet: Conjunto de reseñas de la empresa
        """
        return Review.objects.filter(company_id=company_id).order_by('-created_at')

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