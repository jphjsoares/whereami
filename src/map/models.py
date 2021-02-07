from django.db import models
from django.contrib.postgres.fields import ArrayField, HStoreField

"""
id [integer]
name [charfield]
creator [charfield]
createDate [DateTimeField]
numOfLocation [integer]
locations [arrayfield(arrayfield)]
usersWHoPlayed[user][topScore] [HStorefield]
timesPlayed [integer]
"""

class Map(models.Model):
    # ID field is added automatically
    name = models.CharField(max_length=50)
    creator = models.CharField(max_length=40)
    num_of_locations = models.IntegerField(default=0)
    #Deleted datefield because I dont find it really useful,
    #and might be a pain to debug
    #We will be using ArrayField(models.Charfield()) and store the key instead of coordinates
    #Mainly for ease of development
    mapillary_image_key = ArrayField(models.CharField(max_length=25))
    # [ [lat, lng],[lat, lng],[lat, lng],[lat, lng] ]
    #locations = ArrayField(ArrayField(models.FloatField()))
    # { "asd":213, "asd":3213, ...}
    #users_who_played = HStoreField() will be implemented after users app creation
    #probably will be a fk!
    times_played = models.IntegerField(default=0)

    def __str__(self):
        return '%s, %s, %s' % (self.name, self.creator, self.mapillary_image_key)

