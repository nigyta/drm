from django.urls import path

from . import views
app_name = 'drm'
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('help', views.help, name='help'),
    path('proteins', views.list_proteins, name='protein_list'),
    path('proteins/<str:ref_id>/', views.ref_detail, name='detail'),
]
