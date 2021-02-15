from django import forms
from map.models import Map
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

 #TODO: show form errors somehow
def clean_map_id(value):
    if len(value) < 12 or len(value) > 12:
        raise ValidationError(_('Something wrong with that hash length!'), code="invalid hash (length)")
    
    try:
        map_submitted = Map.objects.get(hash_id=value)
    except Map.DoesNotExist:
        raise ValidationError(_('Something wrong with that map hash!'), code="no map found")        
    
    #TODO: Check if it's only numbers
    return value

class StartNewGame(forms.Form):
    map_id = forms.CharField(label="Map id", max_length=13, validators=[clean_map_id])
    


