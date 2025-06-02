from django import forms
from .models import Car, Profile
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

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'bio', 'avatar']
        labels = {
            'phone_number': 'Numer telefonu',
            'bio':'Opis',
            'avatar':'zdjęcie'
        }