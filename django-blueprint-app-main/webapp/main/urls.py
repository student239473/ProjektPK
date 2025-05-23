from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('cars/', views.cars, name='cars'),
    path('reservation/', views.reservation, name='reservation'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('cars/delete/<int:car_id>/', views.delete_car, name='delete_car'),
    path('login/', views.login_user, name='login_user'),  # Ścieżka do logowania
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout_user'),
    path('cars/toggle/<int:car_id>/', views.toggle_reservation, name='toggle_reservation'),
]