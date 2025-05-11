from django.db import models
from django.contrib.auth.models import User
from .base import BaseModel
from .influencer import Influencer

class Campaign(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('active', 'Activa'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
    ]

    company = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    influencers = models.ManyToManyField(Influencer, through='CampaignInfluencer')

    def __str__(self):
        return self.name

    @property
    def duration_days(self):
        """Calcula la duración de la campaña en días."""
        return (self.end_date - self.start_date).days

    @property
    def is_active(self):
        """Verifica si la campaña está activa."""
        return self.status == 'active'

    @property
    def total_spent(self):
        """Calcula el total gastado en la campaña."""
        return sum(
            ci.influencer.price_per_post 
            for ci in self.campaigninfluencer_set.filter(status='completed')
        )

    def can_add_influencer(self, influencer):
        """Verifica si se puede agregar un influencer a la campaña."""
        return (
            self.status in ['pending', 'active'] and
            influencer.is_available and
            influencer.price_per_post <= self.budget
        )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['start_date']),
            models.Index(fields=['end_date']),
        ] 