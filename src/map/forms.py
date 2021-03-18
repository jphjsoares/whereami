from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def clean_numoflocations(value):
    """Map world validator.

    This functions validates the submitted number of locations in the 
    random map world generator
    
    Parameters
    ----------
    value : 
        Submitted number of locations

    Raises
    -----
    ValidationError : 
        If the submitted number of locations is above 100 or below 5  
    """

    if value > 100:
        raise ValidationError(_("Too many locations."))
    if value < 5:
        raise ValidationError(_("You need at least 5 locations"))
    return value

def clean_locations(locations):
    """Map region validator.

    This functions validates the submitted number of locations in the 
    random map region generator
    
    Parameters
    ----------
    locations : 
        Array containing the coordinates randomly generated

    Raises
    -----
    ValidationError : 
        If the number of locations is not exactly 10  
    """

    locs_split = locations.splitlines()
    if len(locs_split) != 10:
        raise ValidationError(_("Something went wrong"))
    return locations

def clean_locationscustom(locations):
    """Custom map validator.

    This functions validates all the custom selections submitted by a map
    creator

    Parameters
    ----------
    locations : 
        Array containing the coordinates chosen by a map creator

    Raises
    -----
    ValidationError : 
        If the number of locations is below 5 or above 100
    """    
    
    locs_split = locations.splitlines()
    if len(locs_split) < 5:
        raise ValidationError(_("Please select more than 5 locations"))
    if len(locs_split) > 100:
        raise ValidationError(_("No more than 100 locations"))
    return locs_split

class GenerateRandomWorld(forms.Form):
    numoflocations = forms.IntegerField(min_value=5, max_value=100, validators=[clean_numoflocations, ])

class GenerateMapByRegion(forms.Form):
    locations = forms.CharField(widget=forms.Textarea, validators=[clean_locations, ])

class GenerateCustomMap(forms.Form):
    locationscustom = forms.CharField(widget=forms.Textarea, validators=[clean_locationscustom, ])
    