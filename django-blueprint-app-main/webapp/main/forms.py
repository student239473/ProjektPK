from django import forms
from .models import Car
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['car', 'year', 'color', 'price', 'image']

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']