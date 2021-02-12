from django.db import models

class Game(models.Model):
    #game_name
    #game_hash
    #current_map
    #current_guess_timer


#delete the player after playing the map
class Players(models.Model):
    #username - charfield (assign a default when using singleplayer)
    #current_game_id - fk to Game
    #guessed_trigger - boolean
    #current_guess_coordinates - arrayfield
    #score - integerfield


