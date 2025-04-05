from django.contrib import admin
from .models import Influencer, Campaign, CampaignInfluencer

@admin.register(Influencer)
class InfluencerAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'platform', 'category', 'followers', 'engagement_rate', 'is_available')
    list_filter = ('category', 'platform', 'is_available')
    search_fields = ('name', 'username', 'description')

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'budget', 'start_date', 'end_date', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'description')

@admin.register(CampaignInfluencer)
class CampaignInfluencerAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'influencer', 'status')
    list_filter = ('status',)
