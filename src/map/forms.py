from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def clean_numoflocations(value):
        if value > 100:
            raise ValidationError(_("Too many locations."))
        if value < 5:
            raise ValidationError(_("You need at least 5 locations"))
        return value

class GenerateRandomWorld(forms.Form):
    numoflocations = forms.IntegerField(min_value=5, max_value=100, validators=[clean_numoflocations, ])

    