from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from .models import Campaign, Influencer, Category

class CampaignForm(forms.ModelForm):
    """
    Formulario para crear y editar campañas.
    """
    class Meta:
        model = Campaign
        fields = ['name', 'description', 'budget', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        """
        Valida que las fechas sean coherentes y que el presupuesto sea positivo.
        """
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        budget = cleaned_data.get('budget')

        if start_date and end_date:
            if start_date < timezone.now().date():
                raise forms.ValidationError(
                    'La fecha de inicio no puede ser anterior a hoy'
                )
            if end_date <= start_date:
                raise forms.ValidationError(
                    'La fecha de fin debe ser posterior a la fecha de inicio'
                )

        if budget and budget <= 0:
            raise forms.ValidationError(
                'El presupuesto debe ser mayor que cero'
            )

        return cleaned_data

class InfluencerForm(forms.ModelForm):
    """
    Formulario para crear y editar influencers.
    """
    class Meta:
        model = Influencer
        fields = [
            'name', 'username', 'platform', 'description',
            'categories', 'location', 'contact_email',
            'price_per_post', 'followers', 'engagement_rate'
        ]
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'rows': 4}),
            'engagement_rate': forms.NumberInput(attrs={'step': '0.1'}),
        }

    def clean(self):
        """
        Valida que los datos del influencer sean coherentes.
        """
        cleaned_data = super().clean()
        followers = cleaned_data.get('followers')
        engagement_rate = cleaned_data.get('engagement_rate')
        price_per_post = cleaned_data.get('price_per_post')

        if followers and followers < 0:
            raise forms.ValidationError(
                'El número de seguidores no puede ser negativo'
            )

        if engagement_rate:
            if engagement_rate < 0 or engagement_rate > 100:
                raise forms.ValidationError(
                    'La tasa de engagement debe estar entre 0 y 100'
                )

        if price_per_post and price_per_post <= 0:
            raise forms.ValidationError(
                'El precio por publicación debe ser mayor que cero'
            )

        return cleaned_data

class ScrapingForm(forms.Form):
    """
    Formulario para scrapear datos de influencers.
    """
    username = forms.CharField(
        max_length=50,
        label='Nombre de usuario',
        help_text='Ingrese el nombre de usuario del influencer en Instagram'
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Categorías'
    )

    def clean_username(self):
        """
        Valida que el nombre de usuario no exista ya en la base de datos.
        """
        username = self.cleaned_data['username']
        if Influencer.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'Ya existe un influencer con este nombre de usuario'
            )
        return username

class ReviewForm(forms.Form):
    """
    Formulario para crear reseñas.
    """
    RATING_CHOICES = [
        (1, '1 estrella'),
        (2, '2 estrellas'),
        (3, '3 estrellas'),
        (4, '4 estrellas'),
        (5, '5 estrellas'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        label='Calificación'
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        label='Comentario'
    )

    def clean_comment(self):
        """
        Valida que el comentario tenga una longitud mínima.
        """
        comment = self.cleaned_data['comment']
        if len(comment.strip()) < 10:
            raise forms.ValidationError(
                'El comentario debe tener al menos 10 caracteres'
            )
        return comment 