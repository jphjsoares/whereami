from django import forms
from map.models import Map
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def clean_map_id(value):
    """Map id validator.

    This functions validades the submitted map id
    
    Parameters
    ----------
    value : 
        Submitted map id

    Raises
    -----
    ValidationError : 
        If the length is wrong
        Map does not exists  
    """

    if len(value) < 12 or len(value) > 12:
        raise ValidationError(_('Looks like that id is too small or too big.'), code="map length problem")
    

    try:
        map_submitted = Map.objects.get(hash_id=value)
    except Map.DoesNotExist:
        raise ValidationError(_('No map with that id.'), code="no map found")        
    
    return value

class StartNewGame(forms.Form):
    map_id = forms.CharField(label="Map id", max_length=13, validators=[clean_map_id])
    


