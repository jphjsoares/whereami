from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def singleplayer(request):
    return HttpResponse("singleplayer")

def multiplayer(request):
	return HttpResponse("multiplayer")