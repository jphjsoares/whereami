from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import StartNewGame
from .models import Game, Players
from map.models import Map
import random
import json



def singleplayer(request):
    """ Creates singleplayer instance and handles homepage visit"""
     
    if request.method == 'POST':
        form = StartNewGame(request.POST)
        if form.is_valid():

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
            errors = json.loads(form.errors.as_json())  # validation errors from forms.py
            messages.error(request, errors["map_id"][0]["message"])
            return redirect("/game/singleplayer")

    return render(request, "game/singleplayer-home.html")

def singleplayer_random(request):
    """Gets all the maps and creates a game with a random map"""

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
    """Handles singleplayer game instance
    
    This function handles the game instance hash, returning a new game
    if all validations are correct
    
    Parameters
    ---------
    hash : 
        Game instance hash to be validaded
    
    Returns :
    -------
        View with the all the map locations shuffled

    Validates :
    ---------
        Hash does not belong to any game
        Game has been deleted
        Game has ended (was played)
    """
    

    # ------- Check if a game with that hash even exists ------- 
    try:
        current_game_instance = Game.objects.get(game_hash=hash)
    except Game.DoesNotExist:
        messages.error(request, "There's no available game with this id!")
        return redirect("/game/singleplayer")

    # ------- Check if game has not been deleted -------     
    try:
        map_being_played = Map.objects.get(hash_id=current_game_instance.current_map_hash)
    except Map.DoesNotExist:
        current_game_instance.delete()
        messages.error(request, "The map you want to play has been deleted")
        return redirect("/game/singleplayer")
    
    # ------- Make sure game has not ended ------- 
    if current_game_instance.has_ended == True:
        messages.error(request, "This game has ended! Start a new one!")
        return redirect("/game/singleplayer")
        
    # ------- SUCCESS ------- 
    else:
        locations = map_being_played.mapillary_image_key
        random.shuffle(locations) #shuffle locations
        return render(request, "game/singleplayer-instance.html", context={'loc_array':locations})

def end_of_singleplayer_game(request, hash):
    """Ends a singleplayer game, making it unplayable
    
    This function takes a game hash and makes it unplayable
    after performing some checks

    Parameters
    ----------
    hash : 
        Game instance hash
    
    Returns
    -------
        Game summary page, showing the user their score and some custom
        messages depending on their score
    
    Validates
    ---------
        If game exists
        If map played exists (to get the max score)

    """
    
    # ------- Make sure the game you are trying to end exists ------- 
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

        # ------- SUCCESS -------
        max_points = current_map.num_of_locations * 2250
        return render(request, "game/end-of-game.html", {'score': score, 'max_possible_score': max_points, 'map_hash': current_map.hash_id})
    
    except Game.DoesNotExist:
        messages.error(request, "Game instance could not be deleted. Probably already deleted, not a problem!")
        return redirect("/game/singleplayer")

def update_singleplayer_score(request, hash, final_score):
    """Update player score

    This function updates the player score, so that we can display 
    it (on the game summary) after playing the game

    Parameters
    ----------
    hash : 
        Game instance hash played by the user
    final_score :
        Score the user was able to achieve
    
    Returns
    -------
    HttpResponse : 
        'UPDATED' if the score was successfuly updated
        'No active game' if a validation failed

    Validates
    ---------
        If game exists
    """
     
    try:
        current_game_instance = Game.objects.get(game_hash=hash)
    except Game.DoesNotExist:
        return HttpResponse("No active game")
    
    # ------- Update single player score ------- 
    current_player = Players.objects.get(current_game_id=current_game_instance)
    current_player.score = final_score
    current_player.save()
    
    return HttpResponse('UPDATED')
