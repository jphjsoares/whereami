from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import StartNewGame
from .models import Game, Players
from map.models import Map
import random

# Create your views here.
def singleplayer(request):
    if request.method == 'POST':
        form = StartNewGame(request.POST)

        if form.is_valid():
            
            game_instance_to_create = Game(
                    current_map_hash=request.POST["map_id"],
                    is_active=True
                )

            game_instance_to_create.save()
            
            user_to_create = Players(
                    username="single",
                    current_game_id=game_instance_to_create,
                    current_guess_coordinates=[],
                    score=0
                )

            user_to_create.save()
            
            url_of_game = "/game/" + game_instance_to_create.game_hash
            
            return redirect(url_of_game)
    return render(request, "game/singleplayer-home.html")

def singleplayer_random(request):
    all_maps = Map.objects.all()
    random_map = random.choice(all_maps)
    print("Creating random map with id of: " + random_map.hash_id)
    game_instance_to_create = Game(
            current_map_hash=random_map.hash_id,
            is_active=True
        )

    game_instance_to_create.save()
    
    user_to_create = Players(
            username="single-random",
            current_game_id=game_instance_to_create,
            current_guess_coordinates=[],
            score=0
        )

    user_to_create.save()
    
    url_of_game = "/game/" + game_instance_to_create.game_hash
    return redirect(url_of_game)
    

def singleplayer_game_instance(request, hash):
    
    ### Check if there's an available game with that has
    try:
        current_game_instance = Game.objects.get(game_hash=hash)
    except Game.DoesNotExist:
        messages.error(request, "There's no available game with this id!")
        return redirect("/game/singleplayer")


    map_being_played = Map.objects.get(hash_id=current_game_instance.current_map_hash)
    
    if current_game_instance.is_active == False:
        messages.error(request, "This game exists, but is expired. Create a new game!")
        return redirect("/game/singleplayer")
    
    else:
        locations = map_being_played.mapillary_image_key
        return render(request, "game/singleplayer-instance.html", context={'loc_array':locations})

def end_of_singleplayer_game(request, hash):
    try:
        current_game_instance = Game.objects.get(game_hash=hash)
        current_game_instance.delete()
        return redirect("/")
    except Game.DoesNotExist:
        print("Oops. Looks like there's no game with that id. Probably already deleted!")
        messages.error(request, "Instance could not be deleted")
        return redirect("/game/singleplayer")


def multiplayer(request):
   return HttpResponse("Multiplayer is still being developed!")
