from django.contrib import admin
from .models import Game, Players

# Register models for use on dev
admin.site.register(Game)
admin.site.register(Players)