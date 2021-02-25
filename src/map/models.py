from django.db import models
from django.contrib.postgres.fields import ArrayField

def make_hash_id():
    import random, string
    allowed_chars = ''.join((string.ascii_letters, string.digits))
    return ''.join(random.choices(allowed_chars, k=12))


class Map(models.Model):
    hash_id = models.CharField(max_length=13, default=make_hash_id)
    """
    MAP TYPES:
    1 - custom
    2 - region
    3 - world
    """
    map_type = models.IntegerField(default=1)
    name = models.CharField(max_length=50)
    creator = models.CharField(max_length=40)
    num_of_locations = models.IntegerField(default=0)    
    mapillary_image_key = ArrayField(models.CharField(max_length=25))    
    times_played = models.IntegerField(default=0)

    def __str__(self):
        return '%s, %s, %s' % (self.name, self.creator, self.mapillary_image_key)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('get-map',args=[str(self.hash_id)])

class ReportedImages(models.Model):
    mapillary_image = models.CharField(max_length=25)
    """
    REPORT REASONS:
    0 - no reason given
    1 - image related
    2 - image location related
    """
    reason_is_low_quality = models.IntegerField(default=0)
    reason_is_wrong_coordinates = models.IntegerField(default=0)