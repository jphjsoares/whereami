from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def singleplayer(request):
    return render(request, "game/singleplayer-home.html")

def multiplayer(request):
	return HttpResponse("multiplayer")