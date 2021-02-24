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
    
    #Make sure game has not ended
    if current_game_instance.has_ended == True:
        messages.error(request, "This game has ended! Start a new one!")
        return redirect("/game/singleplayer")
    
    else:
        locations = map_being_played.mapillary_image_key
        random.shuffle(locations) #shuffle locations
        return render(request, "game/singleplayer-instance.html", context={'loc_array':locations})

def end_of_singleplayer_game(request, hash):
    
    #make sure the game actually exists
    try:
        current_game_instance = Game.objects.get(game_hash=hash)
        current_player = Players.objects.get(current_game_id=current_game_instance)
        score = current_player.score

        #This will make the game unplayable, but will preserve the end game link
        current_game_instance.has_ended = True 
        current_game_instance.save()

        try:
            current_map = Map.objects.get(hash_id=current_game_instance.current_map_hash)
        except Map.DoesNotExist:
            messages.error(request, "Something went wrong when trying to get your game summary. Don't worry though, your game instance was deleted!")
            return redirect("/game/singleplayer")

        max_points = current_map.num_of_locations * 2250

        return render(request, "game/end-of-game.html", {'score': score, 'max_possible_score': max_points, 'map_hash': current_map.hash_id})
    
    except Game.DoesNotExist:
        messages.error(request, "Game instance could not be deleted. Probably already deleted, not a problem!")
        return redirect("/game/singleplayer")

def update_singleplayer_score(request, hash, final_score):
    try:
        current_game_instance = Game.objects.get(game_hash=hash)
    except Game.DoesNotExist:
        return HttpResponse("No such active game")
    
    current_player = Players.objects.get(current_game_id=current_game_instance)
    current_player.score = final_score
    current_player.save()
    return HttpResponse('UPDATED')


def multiplayer(request):
   return HttpResponse("Multiplayer is still being developed!")
