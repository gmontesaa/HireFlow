from django.db.models import Q, Avg, Count
from django.core.exceptions import ValidationError
from ..models import Influencer, Category, Review
from django.utils.text import slugify

class InfluencerService:
    """
    Servicio que maneja la lógica de negocio relacionada con los influencers.
    """
    @staticmethod
    def search_influencers(query=None, category=None, min_followers=None, max_followers=None,
                          min_engagement=None, max_engagement=None, min_price=None, max_price=None,
                          location=None, platform=None, sort_by=None):
        """
        Busca influencers según los criterios especificados.
        
        Args:
            query (str): Término de búsqueda para nombre, username o descripción
            category (int): ID de la categoría
            min_followers (int): Mínimo número de seguidores
            max_followers (int): Máximo número de seguidores
            min_engagement (float): Mínima tasa de engagement
            max_engagement (float): Máxima tasa de engagement
            min_price (float): Precio mínimo por publicación
            max_price (float): Precio máximo por publicación
            location (str): Ubicación del influencer
            platform (str): Plataforma social
            sort_by (str): Campo por el cual ordenar los resultados
            
        Returns:
            QuerySet: Conjunto de influencers que cumplen con los criterios
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

        if platform:
            queryset = queryset.filter(platform=platform)

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

        if sort_by:
            valid_sort_fields = ['followers', 'engagement_rate', 'price_per_post', 'created_at']
            if sort_by in valid_sort_fields:
                queryset = queryset.order_by(f'-{sort_by}')

        return queryset.distinct()

    @staticmethod
    def get_top_influencers(limit=5, category=None):
        """
        Obtiene los influencers con mejor engagement.
        
        Args:
            limit (int): Número máximo de influencers a retornar
            category (int): ID de la categoría para filtrar
            
        Returns:
            QuerySet: Conjunto de influencers ordenados por engagement
        """
        queryset = Influencer.objects.filter(is_available=True)
        if category:
            queryset = queryset.filter(categories__id=category)
        return queryset.order_by('-engagement_rate')[:limit]

    @staticmethod
    def get_influencer_stats(influencer_id):
        """
        Obtiene estadísticas detalladas de un influencer.
        
        Args:
            influencer_id (int): ID del influencer
            
        Returns:
            dict: Diccionario con estadísticas del influencer
        """
        influencer = Influencer.objects.get(id=influencer_id)
        reviews = Review.objects.filter(influencer=influencer)
        
        return {
            'average_rating': reviews.aggregate(Avg('rating'))['rating__avg'] or 0,
            'total_reviews': reviews.count(),
            'positive_reviews': reviews.filter(rating__gte=4).count(),
            'negative_reviews': reviews.filter(rating__lte=2).count(),
            'engagement_score': influencer.engagement_score,
            'total_campaigns': influencer.campaigninfluencer_set.count(),
            'completed_campaigns': influencer.campaigninfluencer_set.filter(status='completed').count(),
        }

    @staticmethod
    def create_influencer(data):
        """
        Crea un nuevo influencer.
        
        Args:
            data (dict): Datos del influencer
            
        Returns:
            Influencer: Instancia del influencer creado
            
        Raises:
            ValidationError: Si los datos no son válidos
        """
        try:
            # Generar el slug si no se proporciona
            if 'slug' not in data and 'username' in data:
                base_slug = slugify(data['username'])
                slug = base_slug
                counter = 1
                while Influencer.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                data['slug'] = slug

            influencer = Influencer(**data)
            influencer.full_clean()
            influencer.save()
            return influencer
        except Exception as e:
            raise ValidationError(f"Error al crear el influencer: {str(e)}")

    @staticmethod
    def update_influencer(influencer_id, data):
        """
        Actualiza un influencer existente.
        
        Args:
            influencer_id (int): ID del influencer
            data (dict): Datos a actualizar
            
        Returns:
            Influencer: Instancia del influencer actualizado
            
        Raises:
            ValidationError: Si los datos no son válidos
        """
        try:
            influencer = Influencer.objects.get(id=influencer_id)
            for key, value in data.items():
                setattr(influencer, key, value)
            influencer.full_clean()
            influencer.save()
            return influencer
        except Exception as e:
            raise ValidationError(f"Error al actualizar el influencer: {str(e)}")

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