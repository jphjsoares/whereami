from django import forms
from django.contrib.postgres.forms import SplitArrayField

class CustomMapForm(forms.Form):
    locations = SplitArrayField(SplitArrayField(forms.IntegerField(required=True), size=2), size=1)