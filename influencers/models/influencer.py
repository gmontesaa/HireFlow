from django.db import models
from .base import BaseModel
from .category import Category

class Influencer(BaseModel):
    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
    ]

    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='instagram')
    categories = models.ManyToManyField(Category, related_name='influencers')
    followers = models.IntegerField()
    engagement_rate = models.FloatField()
    description = models.TextField()
    price_per_post = models.DecimalField(max_digits=10, decimal_places=2)
    contact_email = models.EmailField()
    instagram_url = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (@{self.username})"

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

    class Meta:
        ordering = ['-followers']
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['platform']),
            models.Index(fields=['is_available']),
        ] 