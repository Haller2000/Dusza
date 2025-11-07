from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Player

class PlayerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'email@pelda.hu'
    }))
    role = forms.ChoiceField(choices=Player.ROLE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    
    class Meta:
        model = Player
        fields = ['email', 'username', 'role', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Becenév'}),
        }
    
        def save(self, commit=True):
            user = super().save(commit=False)
            user.email = self.cleaned_data['email']
            user.role = self.cleaned_data['role']
            if commit:
                user.save()
            return user
    
class PlayerLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'email@pelda.hu'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Jelszó'
    }))
    role = forms.ChoiceField(choices=Player.ROLE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'
    }))