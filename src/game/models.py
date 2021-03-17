from django.db import models
from django.contrib.postgres.fields import ArrayField

def make_hash_id():
    """Creates the random game hash with letters and digits"""
    import random, string
    allowed_chars = ''.join((string.ascii_letters, string.digits))
    return ''.join(random.choices(allowed_chars, k=16))


class Game(models.Model):
    """ Game instance model

    Fields
    ----------
    game_hash : CharField
        Used to identify each game instance
    has_ended : BooleanField
        True if the game has already been played,
        so that it will be unplayable
    current_map_hash : CharField
        Chosen map id of the game
    """
    game_hash = models.CharField(max_length=17, default=make_hash_id)
    has_ended = models.BooleanField(default=False)
    current_map_hash = models.CharField(max_length=13)



class Players(models.Model):
    """ Game instance model

    Fields
    ----------
    username : CharField
        Player username
    current_game_id : ForeignKey
        Key for the game the player is playing
    guessed_trigger : BooleanField
        Will be used in multiplayer to check if the player has taken a guess
    current_guess_coordinates : ArrayField(Floatfields)
        Contains each guess coordinates the player has taken
    score : PositiveIntegerField
        Contains the score of the player
    """
    username = models.CharField(max_length=20, blank=False)
    current_game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    guessed_trigger = models.BooleanField(default=False)
    current_guess_coordinates = ArrayField(models.FloatField(blank=True)) 
    score = models.PositiveIntegerField(default=0)


