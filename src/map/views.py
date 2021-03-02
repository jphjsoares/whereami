from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Map, ReportedImages
from .forms import GenerateRandomWorld, GenerateMapByRegion, GenerateCustomMap
from random import uniform, choice
import random
import os
import json
import urllib
import concurrent.futures

bboxes_for_create_world = [
    #When inserting new boxes make sure the calculations for create_world() will work
    "-168.38,55.81,-107.82,71.49", #top canada and alaska
    "-131.2,23.45,-51.0,56.05", #north america
    "-114.5,-1.4,-49.4,27.5", #central and north of south america
    "-56.76,59.65,-36.19,73.99", #greenland
    "-24.63,63.24,-13.29,66.59", #iceland
    "5.03,62.03,32.23,71.28", #north scandinavia
    "30.7,44.0,163.8,69.5", #russia and top asia
    "-11.54,33.95,41.81,62.64", #europe and south scandinavia
    "-18.0,3.7,35.8,36.3", #North and middle africa
    "34.8,2.6,97.9,44.2", #middle east
    "90.9,-4.4,146.8,47.6", #china, east and south asias
    "-81.7,-55.8,-33.3,1.2", #south america
    "4.6,-34.9,60.8,12.8", #south africa
    "94.2,-12.2,154.3,6.2", #south asia
    "112.79,-44.08,153.92,-10.39", #australia
    "113.0,-39.0,156.1,-11.5",  #new zealend
    "8.72,45.51,27.88,53.76", #middle europe 2
    "-31.71,32.4,10.31,43.63", #penisule iberic and some european islands
    "5.3,53.85,31.58,63.86", #south scandinavia
    "-126.54,31.73,-100.52,51.89", #west coast us and canada
    "-74.3,-55.2,-36.5,-13.6", #shouth america 2
    "111.56,-35.17,132.22,19.31", #australia 2
    "140.61,-47.43,179.28,-9.31", #australia 3 and fiji
    "-116.6,25.7,-80.2,57.5", #central usa and canada
    "63.26,4.43,110.37,31.47", #india
]

locations_to_submit_final = []

# ------- Main page ------- 
def index(request):
    return render(request, 'map/index.html')

# ------- Let the user choose what places to add to a new map, by clicking ------- 
def create_custom(request):
    
    if request.method == 'POST':
        form = GenerateCustomMap(request.POST)
        if form.is_valid():
        
            input = request.POST["locationscustom"].splitlines()
            locations_to_submit_final = []

            for submitted_location in input:
                locations_to_submit_final.append(submitted_location)

            map_to_submit = Map(name="custom",
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
            errors = json.loads(form.errors.as_json())
            messages.error(request, errors["locationscustom"][0]["message"])
            return redirect("/map/createcustom")        
    else:
        return render(request, 'map/create-custom.html') 

# ------- Let the user draw a polygon on the map, creating the "perimter" ------- 
def create_by_region(request):
    if request.method == "POST":
        form = GenerateMapByRegion(request.POST)
        if form.is_valid():        
            
            input = request.POST["locations"].splitlines()
            locations_to_submit_final = []

            for random_location in input:
                locations_to_submit_final.append(random_location)
            
            map_to_submit = Map(name="by-region",
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
            errors = json.loads(form.errors.as_json())
            messages.error(request, errors["locations"][0]["message"])
            return redirect("/map/createbyregion")
    else: 
        return render(request, 'map/create-by-region.html')

# ------- Generate random locations for create_world() ------- 
def get_location(picked_box, request):
    print("Starting threads...")
    url = "https://a.mapillary.com/v3/images?client_id=" + os.environ.get("CLIENT_ID") + "&per_page=50&min_quality_score=3&bbox=" + picked_box
    req = urllib.request.urlopen(url) 
    data = json.load(req)
    print(data["features"])
    # ------- Make sure we have some results ------- 
    if len(data["features"]) != 0:
        randomly_selected_image = random.choice(data["features"])
        
        #filter user 'wbs' and 'adminmapillary' (low quality and wrong coordinates)
        if randomly_selected_image["properties"]["username"] != "wbs" and randomly_selected_image["properties"]["username"] != "adminmapillary": 
            # ------- Check if the randomly chosen image is reported ------- 
            check_image_reported = check_reported(request, randomly_selected_image["properties"]["key"]).content
            if check_image_reported.decode('utf-8') == 'OKAY':
                locations_to_submit_final.append(randomly_selected_image["properties"]["key"])
                print("CREATED " + randomly_selected_image["properties"]["key"])
            else: 
                get_location(picked_box)
    else:
         get_location(picked_box)

# ------- Give random locations around the world ------- 
def create_world(request):

    if request.method == "POST":
        form = GenerateRandomWorld(request.POST)
        if form.is_valid():
            
            chosen_bboxes = []
            submitted_number_of_locations = request.POST["numoflocations"]
        
            # ------- Choose boxes randomly for new map ------- 
            for i in range(0, int(submitted_number_of_locations)):
                
                picked_box = random.choice(bboxes_for_create_world).split(',') #choose a random box and prepare it
                
                #All bboxes were chosen so that none of these operations outputs negative
                long_difference = float(picked_box[2]) - float(picked_box[0])
                lat_difference = float(picked_box[3]) - float(picked_box[1])
                to_divide_long = long_difference/2 
                to_divide_lat = lat_difference/2
                
                #For each coordinate randomly subtract, or sum based on what was calculated
                picked_box[0] = str(float(picked_box[0]) - random.uniform(to_divide_long*(-1), to_divide_long))
                picked_box[2] = str(float(picked_box[2]) - random.uniform(to_divide_long*(-1), to_divide_long))
                picked_box[1] = str(float(picked_box[1]) - random.uniform(to_divide_lat*(-1), to_divide_lat))
                picked_box[3] = str(float(picked_box[3]) - random.uniform(to_divide_lat*(-1), to_divide_lat))
                picked_box = ','.join(picked_box)
                chosen_bboxes.append(picked_box)
            
            # ------- Each thread is responsible for 1 location ------- 
            with concurrent.futures.ThreadPoolExecutor(max_workers=int(submitted_number_of_locations)) as e:
                for i in range(0, int(submitted_number_of_locations)):
                    e.submit(get_location, chosen_bboxes[i], request)
            
            map_to_submit = Map(name="random-world",
                creator="backend",
                map_type=3,
                num_of_locations=len(locations_to_submit_final),
                mapillary_image_key=locations_to_submit_final,
                times_played=0
            )
            map_to_submit.save()

            #clear locations because there was a bug where locations would persist (because it's global)
            locations_to_submit_final.clear()
            message_to_send = "Created map ID: " + str(map_to_submit.hash_id)
            messages.success(request, message_to_send)
            return redirect("/")
            
        else:
            errors = json.loads(form.errors.as_json())
            messages.error(request, errors["numoflocations"][0]["message"])
            return redirect("/map/createworld")

    else:
        form = GenerateRandomWorld()
    return render(request, 'map/create-world.html')

# ------- Image reported ------- 
def report_image(request, image_key, reason_low_quality, reason_wrong_coordinates): 
    try:
        is_already_reported = ReportedImages.objects.get(mapillary_image=image_key)
        return HttpResponse("This image is already reported, therefore it will not be reported again")
    except ReportedImages.DoesNotExist:
        all_the_maps = Map.objects.all()

        #Cycle through all the existent maps delete the image key from the map if it has it
        #If the leftover len(locations) is less than 5 delete the map, else save
        for current_map in all_the_maps:

            if image_key in current_map.mapillary_image_key:
                current_map.mapillary_image_key.remove(image_key)
                current_map.num_of_locations -= 1
                if current_map.num_of_locations < 5:
                    current_map.delete()
                else:
                    current_map.save()

        new_report = ReportedImages(
            mapillary_image=image_key,
            reason_is_low_quality=reason_low_quality,
            reason_is_wrong_coordinates=reason_wrong_coordinates
        )
        new_report.save()

        return HttpResponse(new_report.mapillary_image + " reported")

# ------- Check if images are reported ------- 
def check_reported(request, image_key):
    try: 
        #Be careful with images reported more than 1 time
        reported = ReportedImages.objects.get(mapillary_image=image_key)
        return HttpResponse("REPORTED") 
    
    #No image reported with that id
    except ReportedImages.DoesNotExist: 
        return HttpResponse("OKAY")

# ------- Get the json for a map ------- 
def get_map(request, hash):
    try:
        map = Map.objects.filter(hash_id=hash).values()
        return JsonResponse({"map": list(map)})
    except Map.DoesNotExist:
        raise Http404("No map with that id")
    