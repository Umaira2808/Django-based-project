from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('home/', views.home, name='home'),
    path('submit/', views.submit, name='submit'),
    path('save_translations/', views.save_translations, name='save_translations'),
    path('display/', views.display, name='display'),
]
