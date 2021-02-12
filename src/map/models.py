from django.db import models
from django.contrib.postgres.fields import ArrayField

def make_hash_id():
    import random, string
    allowed_chars = ''.join((string.ascii_letters, string.digits))
    return ''.join(random.choices(allowed_chars, k=12))


class Map(models.Model):
    # ID field is added automatically
    hash_id = models.CharField(max_length=13, default=make_hash_id)
    #1 - custom
    #2 - region
    #3 - world
    map_type = models.IntegerField(default=1)
    name = models.CharField(max_length=50)
    creator = models.CharField(max_length=40)
    num_of_locations = models.IntegerField(default=0)
    
    #Deleted datefield because I dont find it really useful and might be a pain to debug
    
    #We will be using ArrayField(models.Charfield()) and store the key instead of coordinates
    #Mainly for ease of development
    mapillary_image_key = ArrayField(models.CharField(max_length=25))
    
    # [ [lat, lng],[lat, lng],[lat, lng],[lat, lng] ] -> locations = ArrayField(ArrayField(models.FloatField()))
    #users_who_played = HStoreField() will be implemented after users app creation probably will be a fk!
    
    times_played = models.IntegerField(default=0)

    def __str__(self):
        return '%s, %s, %s' % (self.name, self.creator, self.mapillary_image_key)


