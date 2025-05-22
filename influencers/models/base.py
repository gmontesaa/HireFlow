from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    """
    Modelo base abstracto que proporciona campos y funcionalidad común para todos los modelos.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        abstract = True
        ordering = ['-created_at']

    @property
    def is_recent(self):
        """Verifica si el objeto fue creado en las últimas 24 horas."""
        return (timezone.now() - self.created_at) < timezone.timedelta(days=1)

    def save(self, *args, **kwargs):
        """Sobrescribe el método save para agregar validaciones personalizadas."""
        self.full_clean()
        super().save(*args, **kwargs) 