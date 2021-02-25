from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import StartNewGame
from .models import Game, Players
from map.models import Map
import random
import json


# ------- Main page and game by map id creator -------  
def singleplayer(request):
    if request.method == 'POST':
        form = StartNewGame(request.POST)
        if form.is_valid():

            # ------- Check if the map exists ------- 
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
        else:
            # errors gets the validation errors in forms.py
            errors = json.loads(form.errors.as_json())
            messages.error(request, errors["map_id"][0]["message"])
            return redirect("/game/singleplayer")

    return render(request, "game/singleplayer-home.html")

# ------- Create a game with a random map ------- 
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
    
# ------- Game instance view ------- 
def singleplayer_game_instance(request, hash):
    
    # ------- Check if a game with that hash even exists ------- 
    try:
        current_game_instance = Game.objects.get(game_hash=hash)
    except Game.DoesNotExist:
        messages.error(request, "There's no available game with this id!")
        return redirect("/game/singleplayer")

    map_being_played = Map.objects.get(hash_id=current_game_instance.current_map_hash)
    
    # ------- Make sure game has not ended ------- 
    if current_game_instance.has_ended == True:
        messages.error(request, "This game has ended! Start a new one!")
        return redirect("/game/singleplayer")
        
    # ------- If request game has not ended and exists, start it by giving the locations ------- 
    else:
        locations = map_being_played.mapillary_image_key
        random.shuffle(locations) #shuffle locations
        return render(request, "game/singleplayer-instance.html", context={'loc_array':locations})

# ------- End the game ------- 
def end_of_singleplayer_game(request, hash):
    
    # ------- Make sure the game you are trying to end exists ------- 
    #Probably check if if you are even authorized to end
    try:
        current_game_instance = Game.objects.get(game_hash=hash)
        current_player = Players.objects.get(current_game_id=current_game_instance)
        score = current_player.score
        
        # ------- Make game unplayable forever ------- 
        current_game_instance.has_ended = True 
        current_game_instance.save()

        # ------- Try to get the map hash that was played ------- 
        try:
            current_map = Map.objects.get(hash_id=current_game_instance.current_map_hash)
        except Map.DoesNotExist:
            messages.error(request, "Something went wrong when trying to get the map you played. Don't worry though, your game instance was deleted!")
            return redirect("/game/singleplayer")

        max_points = current_map.num_of_locations * 2250
        return render(request, "game/end-of-game.html", {'score': score, 'max_possible_score': max_points, 'map_hash': current_map.hash_id})
    
    except Game.DoesNotExist:
        messages.error(request, "Game instance could not be deleted. Probably already deleted, not a problem!")
        return redirect("/game/singleplayer")

# ------- Update singleplayer score ------- 
def update_singleplayer_score(request, hash, final_score):
    # ------- First we need to make sure there's a game active ------- 
    try:
        current_game_instance = Game.objects.get(game_hash=hash)
    except Game.DoesNotExist:
        return HttpResponse("No active game")
    
    # ------- Update single player score ------- 
    current_player = Players.objects.get(current_game_id=current_game_instance)
    current_player.score = final_score
    current_player.save()
    
    return HttpResponse('UPDATED')


def multiplayer(request):
   return HttpResponse("Multiplayer is still being developed!")
