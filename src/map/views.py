from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Map, ReportedImages
from .forms import GenerateRandomWorld
from random import uniform
import os
import json
import urllib



#Main page of the map/ app
def index(request):
    return render(request, 'map/index.html')

#Let the user choose what places to add to a new map, by clicking
def create_custom(request):
    
    if request.method == 'POST':

        #TODO:Check if post input is null
        input = request.POST["locations"].splitlines()
        locations_to_submit_final = []

        if len(input) < 5: #Also be careful with xss and other vulns
            messages.error(request, "Oops... Please select 5 or more locations")
            return redirect("/map/createcustom")
        
        #Add all the image keys to an array for the db
        for submitted_location in input:
            locations_to_submit_final.append(submitted_location)

        
        # Create and save the new map!
        
        map_to_submit = Map(name="testCustom",
            creator="backend",
            map_type=1,
            num_of_locations=len(locations_to_submit_final),
            mapillary_image_key=locations_to_submit_final,
            times_played=0
        )

        map_to_submit.save()


        message_to_send = "Created map ID: " + str(map_to_submit.hash_id)
        messages.success(request, message_to_send)
        return redirect("/")
        
    else:
        return render(request, 'map/create-custom.html') 

#Let the user draw a polygon on the map, creating the "perimter"
#Give random coordinates, that are inside the polygon
def create_by_region(request):
    if request.method == "POST":
        
        #TODO:Check if post input is null
        input = request.POST["locations"].splitlines()
        locations_to_submit_final = []


        for random_location in input:
            locations_to_submit_final.append(random_location)
        
        map_to_submit = Map(name="testByRegion",
            creator="backend",
            map_type=2,
            num_of_locations=len(locations_to_submit_final),
            mapillary_image_key=locations_to_submit_final,
            times_played=0
        )

        map_to_submit.save()
        
        message_to_send = "Created map ID: " + str(map_to_submit.hash_id)
        messages.success(request, message_to_send)
        return redirect("/")
    else: 
        return render(request, 'map/create-by-region.html')

#By defining how many locations to set,
#Give random locations around the world
def create_world(request):

    if request.method == "POST":
        form = GenerateRandomWorld(request.POST)
        if form.is_valid():

            locations_to_submit_final = []
            submitted_number_of_locations = request.POST["numoflocations"]
            while len(locations_to_submit_final) < int(submitted_number_of_locations):
                
                x, y = uniform(-180,180), uniform(-90, 90) #generate random point
                url = "https://a.mapillary.com/v3/images?client_id=" + os.environ.get("CLIENT_ID") + "&per_page=1" + "&closeto=" + str(x) + ',' + str(y) + "&radius=1000000"
                req = urllib.request.urlopen(url) 
                data = json.load(req) #get random point close to the random point generated
                
                if len(data["features"]) != 0 and data["features"][0]["properties"]["quality_score"] >= 3: #if the point is valid, add it to our keys
                    check_image_reported = check_reported(request, data["features"][0]["properties"]["key"]).content
                    if check_image_reported.decode('utf-8') == 'OKAY':
                        print("image accepted")
                        locations_to_submit_final.append(data["features"][0]["properties"]["key"])
                    else: 
                        print("requested image is reported. getting another image...")
                    					

            map_to_submit = Map(name="testRandomWorld",
                creator="backend",
                map_type=3,
                num_of_locations=len(locations_to_submit_final),
                mapillary_image_key=locations_to_submit_final,
                times_played=0
            )

            map_to_submit.save()
            message_to_send = "Created map ID: " + str(map_to_submit.hash_id)
            messages.success(request, message_to_send)
            return redirect("/")
            
        else:
            messages.error(request, "Something wrong with your input! Is it more than 5?")
            return redirect("/map/createworld")
    else:
        form = GenerateRandomWorld()
    
    return render(request, 'map/create-world.html')

def report_image(request, image_key, reason_low_quality, reason_wrong_coordinates): 
    try:
        is_already_reported = ReportedImages.objects.get(mapillary_image=image_key)
        return HttpResponse("This image is already reported, therefore it will not be reported again")
    except ReportedImages.DoesNotExist:
        new_report = ReportedImages(
            mapillary_image=image_key,
            reason_is_low_quality=reason_low_quality,
            reason_is_wrong_coordinates=reason_wrong_coordinates
        )
        new_report.save()
        return HttpResponse(new_report.mapillary_image + " reported")


def check_reported(request, image_key):
    try: 
        #Be careful with images reported more than 1 time
        reported = ReportedImages.objects.get(mapillary_image=image_key)
        return HttpResponse("REPORTED") 
    
    #No image reported with that id
    except ReportedImages.DoesNotExist: 
        return HttpResponse("OKAY")


def get_map(request, hash):
    try:
        map = Map.objects.filter(hash_id=hash).values()
        return JsonResponse({"map": list(map)})
    except Map.DoesNotExist:
        raise Http404("No map with that id")
    