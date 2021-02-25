from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def clean_numoflocations(value):
        if value > 100:
            raise ValidationError(_("Too many locations."))
        if value < 5:
            raise ValidationError(_("You need at least 5 locations"))
        return value

def clean_locations(locations):
    locs_split = locations.splitlines()
    if len(locs_split) != 10:
        raise ValidationError(_("Something went wrong"))
    return locations

def clean_locationscustom(locations):
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
    