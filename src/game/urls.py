from django.urls import path
from . import views

urlpatterns = [
    path('singleplayer', views.singleplayer, name="singleplayer"),
    path('multiplayer', views.multiplayer, name="multiplayer")
]