from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import CustomMapForm

#Main page of the map/ app
def index(request):
    return render(request, 'map/index.html')

#Let the user choose what places to add to a new map, by clicking
def create_custom(request):
    if request.method == 'POST':
        form = CustomMapForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/map/")
    else:
        form = CustomMapForm()
    return render(request, 'map/create-custom.html')

#Let the user draw a polygon on the map, creating the "perimter"
#Give random coordinates, that are inside the polygon
def create_by_region(request):
    return render(request, 'map/create-by-region.html')

#By defining how many locations to set (or infinite),
#Give random locations around the world
def create_world(request):
    return render(request, 'map/create-world.html')