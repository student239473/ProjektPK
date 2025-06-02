from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Category, Thread, Post
from .forms import ThreadForm, PostForm

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'forum/category_list.html', {'categories': categories})

def thread_list(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    threads = category.threads.all().order_by('-created_at')
    return render(request, 'forum/thread_list.html', {'category': category, 'threads': threads})

def post_list(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    posts = thread.posts.all().order_by('created_at')
    return render(request, 'forum/post_list.html', {'thread': thread, 'posts': posts})

@login_required
def create_thread(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.category = category
            thread.author = request.user
            thread.save()
            messages.success(request, "Wątek został utworzony!")
            return redirect('forum:post_list', thread_id=thread.id)
    else:
        form = ThreadForm()
    return render(request, 'forum/create_thread.html', {'form': form, 'category': category})

@login_required
def create_post(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread
            post.author = request.user
            post.save()
            messages.success(request, "Odpowiedź została dodana!")
            return redirect('forum:post_list', thread_id=thread.id)
    else:
        form = PostForm()
    return render(request, 'forum/create_post.html', {'form': form, 'thread': thread})

def can_delete_content(user, obj_author):
    return user == obj_author or user.is_staff

@login_required
def delete_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    if not can_delete_content(request.user, thread.author):
        messages.error(request, "Nie masz uprawnień do usunięcia tego wątku.")
        return redirect('forum:post_list', thread_id=thread.id)

    if request.method == 'POST':
        thread.delete()
        messages.success(request, "Wątek został usunięty.")
        return redirect('forum:thread_list', category_id=thread.category.id)

    return render(request, 'forum/confirm_delete.html', {'object': thread, 'type': 'wątek'})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if not can_delete_content(request.user, post.author):
        messages.error(request, "Nie masz uprawnień do usunięcia tego posta.")
        return redirect('forum:post_list', thread_id=post.thread.id)

    if request.method == 'POST':
        thread_id = post.thread.id
        post.delete()
        messages.success(request, "Post został usunięty.")
        return redirect('forum:post_list', thread_id=thread_id)

    return render(request, 'forum/confirm_delete.html', {'object': post, 'type': 'post'})
