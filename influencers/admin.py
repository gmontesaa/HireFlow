from django.contrib import admin
from .models import Influencer, Campaign, CampaignInfluencer, Review, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Influencer)
class InfluencerAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'platform', 'followers', 'engagement_rate', 'price_per_post', 'is_available')
    list_filter = ('platform', 'is_available', 'categories')
    search_fields = ('name', 'username', 'description')
    filter_horizontal = ('categories',)

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'budget', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('name', 'description')

@admin.register(CampaignInfluencer)
class CampaignInfluencerAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'influencer', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('campaign__name', 'influencer__name')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'influencer', 'company', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('campaign__name', 'influencer__name', 'company__username', 'comment')
