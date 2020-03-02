from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('help', views.help, name='help'),
    path('proteins', views.list_proteins, name='protein_list'),
]