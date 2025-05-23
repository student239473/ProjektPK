from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, DeleteView

from .models import Articles
from .forms import ArticlesForm
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

def news_home(request):
    news = Articles.objects.all().order_by('-published_at')
    return render(request, 'news/index.html', {'news': news})

def news_create(request):
    error = ''

    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news_home')
        else:
            error = 'Submitted form contain errors'

    form = ArticlesForm()

    data = {
        'form': form,
        'error': error,
    }
    return render(request, 'news/create.html', data)

class NewsDetailView(DetailView):
    model = Articles
    template_name = 'news/show.html'
    context_object_name = 'article'

class NewsUpdateView(UpdateView):
    model = Articles
    template_name = 'news/update.html'
    form_class = ArticlesForm

class NewsDeleteView(DeleteView):
    model = Articles
    template_name = 'news/delete.html'
    success_url = '/news/'

@staff_member_required
def news_create(request):
    error = ''
    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news_home')
        else:
            error = 'Submitted form contain errors'

    form = ArticlesForm()
    return render(request, 'news/create.html', {'form': form, 'error': error})