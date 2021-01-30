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
    create_date = models.DateField(auto_now=True)
    num_of_locations = models.IntegerField(default=0)
    
    # [ [lat, lng],[lat, lng],[lat, lng],[lat, lng] ]
    locations = ArrayField(ArrayField(models.FloatField()))
    users_who_played = HStoreField()
    times_played = models.IntegerField(default=0)

    def __str__(self):
        return self.name, self.locations

