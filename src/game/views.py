from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import StartNewGame
from .models import Game, Players

# Create your views here.
def singleplayer(request):
    if request.method == 'POST':
        form = StartNewGame(request.POST)

        if form.is_valid():
            
            game_instance_to_create = Game(
                    current_map_hash=request.POST["map_id"]
                )

            game_instance_to_create.save()
            
            user_to_create = Players(
                    username="single",
                    current_game_id=game_instance_to_create,
                    guessed_trigger=False,
                    current_guess_coordinates=[0.0,0.0],
                    score=0
                )
            user_to_create.save()
            url_of_game = "/game/singleplayer/" + game_instance_to_create.game_hash
            return redirect(url_of_game)
    return render(request, "game/singleplayer-home.html")

def singleplayer_game_instance(request, hash):

    return render(request, "game/singleplayer-instance.html")

def multiplayer(request):
   return HttpResponse("multiplayer")
