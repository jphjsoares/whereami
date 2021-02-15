from django import forms
from map.models import Map

 #TODO: show form errors somehow
def clean_map_id(value):
    if len(value) < 12 or len(value) > 12:
        raise forms.ValidationError('Something wrong with that hash!')
    
    try:
        map_submitted = Map.objects.get(hash_id=value)
    except Map.DoesNotExist:
        raise forms.ValidationError('Something wrong with that map hash!')        
    #TODO: Check if it's only numbers
    return value

class StartNewGame(forms.Form):
    map_id = forms.CharField(label="Map id", max_length=13, validators=[clean_map_id])
    


