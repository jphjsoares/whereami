from django.db import models
from django.contrib.postgres.fields import ArrayField

def make_hash_id():
    import random, string
    base_name = "single"
    allowed_chars = ''.join((string.ascii_letters, string.digits))
    return ''.join(random.choices(allowed_chars, k=16))



class Game(models.Model):
    game_hash = models.CharField(max_length=17, default=make_hash_id)
    is_active = models.BooleanField(default=False)    
    current_map_hash = models.CharField(max_length=13)


#TODO: delete the player after playing the map

class Players(models.Model):
    username = models.CharField(max_length=20, blank=False)
    current_game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    guessed_trigger = models.BooleanField(default=False)
    current_guess_coordinates = ArrayField(models.FloatField(blank=True)) 
    score = models.PositiveIntegerField(default=0)


