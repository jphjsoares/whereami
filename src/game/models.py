from django.db import models
from django.contrib.postgres.fields import ArrayField

def make_hash_id():
    import random, string
    base_name = "single"
    allowed_chars = ''.join((string.ascii_letters, string.digits))
    return ''.join(random.choices(allowed_chars, k=16))



class Game(models.Model):
    game_hash = models.CharField(max_length=17, default=make_hash_id)    
    current_map_hash = models.CharField(max_length=13)


#delete the player after playing the map

class Players(models.Model):
    #when playing singleplayer, a username will be automatically created by the view
    username = models.CharField(max_length=20, blank=False)
    current_game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    guessed_trigger = models.BooleanField() #make default or blank
    current_guess_coordinates = ArrayField(models.FloatField()) #make blank
    score = models.PositiveIntegerField()


