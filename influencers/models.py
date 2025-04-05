from django.db import models
from django.contrib.auth.models import User

class Influencer(models.Model):
    CATEGORY_CHOICES = [
        ('lifestyle', 'Lifestyle'),
        ('business', 'Business'),
        ('motivation', 'Motivation'),
    ]

    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
    ]

    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='instagram')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='lifestyle')
    followers = models.IntegerField()
    engagement_rate = models.FloatField()
    description = models.TextField()
    price_per_post = models.DecimalField(max_digits=10, decimal_places=2)
    contact_email = models.EmailField()
    instagram_url = models.URLField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (@{self.username})"

class Campaign(models.Model):
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CampaignInfluencer(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    influencer = models.ForeignKey(Influencer, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pendiente'),
        ('accepted', 'Aceptado'),
        ('rejected', 'Rechazado'),
        ('completed', 'Completado'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('campaign', 'influencer')

    def __str__(self):
        return f"{self.campaign.name} - {self.influencer.name}"
