from django import forms
from .models import Thread, Post

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'description']
        labels = {
            'title': 'Tytuł',
            'description': 'Opis wątku',
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        labels = {
            'content': 'Treść odpowiedzi',
        }