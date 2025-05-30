from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import render

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('cars/', views.cars, name='cars'),
    path('reservation/', views.reservation, name='reservation'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('cars/delete/<int:car_id>/', views.delete_car, name='delete_car'),
    path('login/', views.login_user, name='login_user'), 
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout_user'),
    path('cars/toggle/<int:car_id>/', views.toggle_reservation, name='toggle_reservation'),
        path('profil/', views.profile_view, name='profile'),
    path('ustawienia/', views.profile_edit, name='profile_edit'),
     path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('settings/', views.settings_view, name='settings'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)