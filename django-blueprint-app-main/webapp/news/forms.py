from .models import Articles
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea

class ArticlesForm(ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'excerpt', 'body', 'published_at']

        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'excerpt': TextInput(attrs={'class': 'form-control', 'placeholder': 'Excerpt'}),
            'body': Textarea(attrs={'class': 'form-control', 'placeholder': 'Article body'}),
    'published_at': DateTimeInput(attrs={
    'class': 'form-control',
    'type': 'datetime-local',
    'placeholder': 'Publication date and time'
}),
        }
