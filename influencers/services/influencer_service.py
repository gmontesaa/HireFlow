from django.db.models import Q
from ..models import Influencer, Category

class InfluencerService:
    @staticmethod
    def search_influencers(query=None, category=None, min_followers=None, max_followers=None,
                          min_engagement=None, max_engagement=None, min_price=None, max_price=None,
                          location=None):
        """
        Busca influencers según los criterios especificados.
        """
        queryset = Influencer.objects.filter(is_available=True)

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(username__icontains=query) |
                Q(description__icontains=query)
            )

        if category:
            queryset = queryset.filter(categories__id=category)

        if min_followers:
            queryset = queryset.filter(followers__gte=min_followers)
        if max_followers:
            queryset = queryset.filter(followers__lte=max_followers)

        if min_engagement:
            queryset = queryset.filter(engagement_rate__gte=min_engagement)
        if max_engagement:
            queryset = queryset.filter(engagement_rate__lte=max_engagement)

        if min_price:
            queryset = queryset.filter(price_per_post__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_post__lte=max_price)

        if location:
            queryset = queryset.filter(location__icontains=location)

        return queryset.distinct()

    @staticmethod
    def get_top_influencers(limit=5):
        """
        Obtiene los influencers con mejor engagement.
        """
        return Influencer.objects.filter(is_available=True).order_by('-engagement_rate')[:limit]

    @staticmethod
    def get_influencers_by_category(category_id):
        """
        Obtiene los influencers de una categoría específica.
        """
        return Influencer.objects.filter(
            categories__id=category_id,
            is_available=True
        ).distinct()

    @staticmethod
    def get_affordable_influencers(budget):
        """
        Obtiene los influencers que están dentro del presupuesto.
        """
        return Influencer.objects.filter(
            is_available=True,
            price_per_post__lte=budget
        ).order_by('price_per_post') 