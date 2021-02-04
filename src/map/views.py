from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Map

#Main page of the map/ app
def index(request):
    return render(request, 'map/index.html')

#Let the user choose what places to add to a new map, by clicking
def create_custom(request):
    #TODO: Only allow POST requests if the user is signed in
    if request.method == 'POST':
        #TODO: check if the user submits 5 or more locations 
                
        input = request.POST["locations"].splitlines()
        locations_to_submit_final = []
        
        #gets lng and lat separated, ready for storing
        for submitted_location in input:
            locations_to_submit_final.append(submitted_location.split(','))


        # Create and save the new map!
        map_to_submit = Map(name="testCustom",
            creator="tester",
            num_of_locations=len(locations_to_submit_final),
            locations=locations_to_submit_final,
            times_played=123
        )

        map_to_submit.save()
        
        return HttpResponse("Success!")
    else:
        return render(request, 'map/create-custom.html')

#Let the user draw a polygon on the map, creating the "perimter"
#Give random coordinates, that are inside the polygon
def create_by_region(request):                                      
    return render(request, 'map/create-by-region.html')

#By defining how many locations to set (or infinite),
#Give random locations around the world
def create_world(request):
    return render(request, 'map/create-world.html')