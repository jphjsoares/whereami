from django.urls import path
from . import views

urlpatterns = [
    path('singleplayer', views.singleplayer, name="singleplayer"),
    path('singleplayer/random', views.singleplayer_random, name="singplayer-random"),
    path('multiplayer', views.multiplayer, name="multiplayer"),
    path('<slug:hash>/', views.singleplayer_game_instance, name='singleplayer_game_instance'),
    path('eg/<slug:hash>', views.end_of_singleplayer_game, name='end_of_singleplayer_game'),
    path('ps/<slug:hash>/<int:final_score>', views.update_singleplayer_score, name='update_player_score')
]