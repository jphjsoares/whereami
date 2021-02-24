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
            try:
                map_being_played = Map.objects.get(hash_id=request.POST["map_id"])
            except Map.DoesNotExist:
                messages.error(request, "This map is not available anymore.")
                return redirect("/game/singleplayer")

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
    random_map = random.choice(all_maps) #Get random map

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
    
    ### Check if there's an available game with that hash
    try:
        current_game_instance = Game.objects.get(game_hash=hash)
    except Game.DoesNotExist:
        messages.error(request, "There's no available game with this id!")
        return redirect("/game/singleplayer")

    
    map_being_played = Map.objects.get(hash_id=current_game_instance.current_map_hash)
    
    #Make sure game is not active
    if current_game_instance.is_active == False:
        messages.error(request, "This game exists, but is expired. Create a new game!")
        return redirect("/game/singleplayer")
    
    else:
        locations = map_being_played.mapillary_image_key
        random.shuffle(locations) #shuffle locations
        return render(request, "game/singleplayer-instance.html", context={'loc_array':locations})

def end_of_singleplayer_game(request, hash, final_score):
    
    #make sure the game actually exists
    try:
        current_game_instance = Game.objects.get(game_hash=hash)
        current_player = Players.objects.get(current_game_id=current_game_instance)
        
        try:
            current_map = Map.objects.get(hash_id=current_game_instance.current_map_hash)
        except Map.DoesNotExist:
            messages.error(request, "Something went wrong when trying to get your game summary. Don't worry though, your game instance was deleted!")
            return redirect("/game/singleplayer")

        max_points = current_map.num_of_locations * 2250
        current_game_instance.delete()

        return render(request, "game/end-of-game.html", {'score': final_score, 'max_possible_score': max_points})
    
    except Game.DoesNotExist:
        print("Oops. Looks like there's no game with that id. Probably already deleted!")
        messages.error(request, "Game instance could not be deleted. Probably already deleted, not a problem!")
        return redirect("/game/singleplayer")


def multiplayer(request):
   return HttpResponse("Multiplayer is still being developed!")
