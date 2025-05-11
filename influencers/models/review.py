from django.db import models
from django.contrib.auth.models import User
from .base import BaseModel
from .campaign import Campaign
from .influencer import Influencer

class Review(BaseModel):
    RATING_CHOICES = [
        (1, '1 estrella'),
        (2, '2 estrellas'),
        (3, '3 estrellas'),
        (4, '4 estrellas'),
        (5, '5 estrellas'),
    ]

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='reviews')
    influencer = models.ForeignKey(Influencer, on_delete=models.CASCADE, related_name='reviews')
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()

    def __str__(self):
        return f"Reseña de {self.company.username} para {self.influencer.name}"

    @property
    def is_positive(self):
        """Verifica si la reseña es positiva (4 o 5 estrellas)."""
        return self.rating >= 4

    @property
    def is_negative(self):
        """Verifica si la reseña es negativa (1 o 2 estrellas)."""
        return self.rating <= 2

    def get_rating_display(self):
        """Retorna el nombre legible de la calificación."""
        return dict(self.RATING_CHOICES).get(self.rating, str(self.rating))

    class Meta:
        unique_together = ('campaign', 'influencer', 'company')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['rating']),
            models.Index(fields=['created_at']),
        ] 