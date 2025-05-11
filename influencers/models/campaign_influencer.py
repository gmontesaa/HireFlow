from django.db import models
from .base import BaseModel
from .campaign import Campaign
from .influencer import Influencer

class CampaignInfluencer(BaseModel):
    STATUS_CHOICES = [
        ('pending_review', 'Pendiente de Revisión'),
        ('review_approved', 'Revisión Aprobada'),
        ('review_rejected', 'Revisión Rechazada'),
        ('message_sent', 'Mensaje Enviado'),
        ('accepted', 'Aceptado'),
        ('rejected', 'Rechazado'),
        ('completed', 'Completado'),
    ]

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    influencer = models.ForeignKey(Influencer, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_review')
    review_notes = models.TextField(blank=True, null=True)
    message_sent_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.campaign.name} - {self.influencer.name}"

    @property
    def is_pending_review(self):
        """Verifica si está pendiente de revisión."""
        return self.status == 'pending_review'

    @property
    def is_approved(self):
        """Verifica si está aprobado."""
        return self.status == 'review_approved'

    @property
    def is_completed(self):
        """Verifica si está completado."""
        return self.status == 'completed'

    def approve_review(self, notes=''):
        """Aprueba la revisión del influencer."""
        self.status = 'review_approved'
        self.review_notes = notes
        self.save()

    def reject_review(self, notes=''):
        """Rechaza la revisión del influencer."""
        self.status = 'review_rejected'
        self.review_notes = notes
        self.save()

    def mark_message_sent(self):
        """Marca el mensaje como enviado."""
        from django.utils import timezone
        self.status = 'message_sent'
        self.message_sent_date = timezone.now()
        self.save()

    class Meta:
        unique_together = ('campaign', 'influencer')
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['message_sent_date']),
        ] 