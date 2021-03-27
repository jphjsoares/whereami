from django.db import models
from django.contrib.postgres.fields import ArrayField

def make_hash_id():
    """Creates the random map hash with letters and digits"""
    
    import random, string
    allowed_chars = ''.join((string.ascii_letters, string.digits))
    return ''.join(random.choices(allowed_chars, k=12))


class Map(models.Model):
    """ Map model

    Fields
    ----------
    hash_id : CharField
        Used to identify each map
    map_type : IntegerField
        1- Custom
        2- Region
        3- World
    num_of_locations : IntegerField
        The number of locations a map has
    mapillary_image_key : ArrayField(CharField)
        Array containing all the keys to each image in the game
    """

    hash_id = models.CharField(max_length=13, default=make_hash_id)
    map_type = models.IntegerField(default=1)
    num_of_locations = models.IntegerField(default=0)    
    mapillary_image_key = ArrayField(models.CharField(max_length=25))    

    def __str__(self):
        return '%s, %s, %s' % (self.name, self.creator, self.mapillary_image_key)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('get-map',args=[str(self.hash_id)])

class ReportedImages(models.Model):
    """ Report system model

    Fields
    ----------
    mapillary_image : CharField
        Key of the reported image
    reason_is_low_quality : IntegerField
        Is 1 if image was reported because of low quality
    reason_is_wrong_coordinates : IntegerField
        Is 1 if image was reported because of containing the wrong coordinates
    """

    mapillary_image = models.CharField(max_length=25)
    reason_is_low_quality = models.IntegerField(default=0)
    reason_is_wrong_coordinates = models.IntegerField(default=0)