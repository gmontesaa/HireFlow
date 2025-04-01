from django.db import models

class influencers(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='influencers/images')
    url = models.URLField(blank=True)
