from django import forms
from django.contrib.postgres.forms import SplitArrayField

def clean_numoflocations(value):
    	if value > 1000:
    		raise forms.ValidationError("Too many locations.")
    	if value < 5:
    		raise forms.ValidationError("You need at least 5 locations")
    	if value < 0:
    		raise forms.ValidationError("Number of locations can't be negative")
    	if value == 0:
    		raise forms.ValidationError("Locations can't be 0")
    	return value

class GenerateRandomWorld(forms.Form):
    numoflocations = forms.IntegerField(min_value=5, max_value=1000, validators=[clean_numoflocations, ])

    