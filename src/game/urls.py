from django.urls import path
from . import views

urlpatterns = [
    path('singleplayer', views.singleplayer, name="singleplayer"),
    path('multiplayer', views.multiplayer, name="multiplayer"),
    path('singleplayer/<slug:hash>/', views.singleplayer_game_instance, name='singleplayer_game_instance'),
]