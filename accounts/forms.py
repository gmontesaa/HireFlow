from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CompanyRegistrationForm(UserCreationForm):
    company_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    industry = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('username', 'company_name', 'email', 'phone', 'industry', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user 