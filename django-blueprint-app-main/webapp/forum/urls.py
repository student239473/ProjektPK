from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('category/<int:category_id>/', views.thread_list, name='thread_list'),
    path('thread/<int:thread_id>/', views.post_list, name='post_list'),
    path('category/<int:category_id>/new/', views.create_thread, name='create_thread'),
    path('thread/<int:thread_id>/reply/', views.create_post, name='create_post'),
    path('thread/<int:thread_id>/delete/', views.delete_thread, name='delete_thread'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    
]