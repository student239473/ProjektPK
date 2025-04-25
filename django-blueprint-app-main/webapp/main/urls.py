from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('cars/', views.cars, name='cars'),
    path('reservation/', views.reservation, name='reservation'),  # Ta linia zapewnia, że 'reservation' jest powiązane z widokiem reservation
    path('confirmation/', views.confirmation, name='confirmation'), 
]