from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'map/index.html')

def create_custom(request):
    return render(request, 'map/create-custom.html')

def create_by_region(request):
    return render(request, 'map/create-by-region.html')

def create_world(request):
    return render(request, 'map/create-world.html')