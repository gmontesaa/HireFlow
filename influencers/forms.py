from django import forms
from .models import Campaign, Influencer, Category

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'description', 'budget', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class InfluencerForm(forms.ModelForm):
    class Meta:
        model = Influencer
        fields = ['name', 'username', 'platform', 'description', 'categories', 'location']
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ScrapingForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario'
        })
    )
    platform = forms.ChoiceField(
        choices=[('instagram', 'Instagram'), ('tiktok', 'TikTok')],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    ) 