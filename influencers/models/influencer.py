from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from .base import BaseModel
from .category import Category

class Influencer(BaseModel):
    """
    Modelo que representa a un influencer en la plataforma.
    """
    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
        ('twitter', 'Twitter'),
    ]

    name = models.CharField(max_length=100, verbose_name='Nombre')
    username = models.CharField(max_length=50, unique=True, verbose_name='Nombre de usuario')
    platform = models.CharField(
        max_length=20,
        choices=PLATFORM_CHOICES,
        default='instagram',
        verbose_name='Plataforma'
    )
    categories = models.ManyToManyField(Category, related_name='influencers', verbose_name='Categorías')
    followers = models.PositiveIntegerField(default=0, verbose_name='Seguidores')
    engagement_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.0,
        verbose_name='Tasa de engagement'
    )
    description = models.TextField(blank=True, null=True, verbose_name='Descripción')
    price_per_post = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.0,
        verbose_name='Precio por publicación'
    )
    contact_email = models.EmailField(blank=True, null=True, verbose_name='Email de contacto')
    instagram_url = models.URLField(blank=True, null=True, verbose_name='URL de Instagram')
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ubicación')
    is_available = models.BooleanField(default=True, verbose_name='Disponible')
    slug = models.SlugField(
        max_length=100, 
        unique=True, 
        default='', 
        verbose_name='Slug'
    )
    is_verified = models.BooleanField(default=False, verbose_name='Verificado')
    is_active = models.BooleanField(default=True, verbose_name='Activo')

    def __str__(self):
        return f"{self.name} (@{self.username})"

    def save(self, *args, **kwargs):
        """Sobrescribe el método save para generar el slug automáticamente."""
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    @property
    def engagement_score(self):
        """Calcula el puntaje de engagement basado en seguidores y tasa de engagement."""
        return (self.followers * self.engagement_rate) / 100

    def get_platform_display(self):
        """Retorna el nombre legible de la plataforma."""
        return dict(self.PLATFORM_CHOICES).get(self.platform, self.platform)

    def is_affordable(self, budget):
        """Verifica si el influencer es asequible para un presupuesto dado."""
        return self.price_per_post <= budget

    def get_absolute_url(self):
        """Retorna la URL absoluta del influencer."""
        from django.urls import reverse
        return reverse('influencer_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-followers']
        verbose_name = 'Influencer'
        verbose_name_plural = 'Influencers'
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['platform']),
            models.Index(fields=['is_available']),
            models.Index(fields=['followers']),
            models.Index(fields=['engagement_rate']),
        ] 