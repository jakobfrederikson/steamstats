from django.urls import path
from . import views

urlpatterns = [
     path('', views.index, name='index'),
     path('detail/<str:steam_id>', views.detail, name='detail'),
     path('database/', views.database, name='database'),
     path('findsteamid/', views.find_steam_id, name='find_steam_id'),
     path('about/', views.about, name='about'),
]
