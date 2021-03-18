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
    """List of bboxes with points to choose from"""
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
    "113.0,-39.0,156.1,-11.5",  #new zealend
    "8.72,45.51,27.88,53.76", #middle europe 2
    "-31.71,32.4,10.31,43.63", #penisule iberic and some european islands
    "5.3,53.85,31.58,63.86", #south scandinavia
    "-126.54,31.73,-100.52,51.89", #west coast us and canada
    "-74.3,-55.2,-36.5,-13.6", #shouth america 2
    "111.56,-35.17,132.22,19.31", #australia 1
    "140.61,-47.43,179.28,-9.31", #australia 2 and fiji
    "-116.6,25.7,-80.2,57.5", #central usa and canada
    "63.26,4.43,110.37,31.47", #india
]

# Will be filled with all the locations in random world generator
locations_to_submit_final = []

def index(request):
    return render(request, 'map/index.html')

def create_custom(request):
    """Creates a map with locations chosen by the user"""

    if request.method == 'POST':
        form = GenerateCustomMap(request.POST)
        if form.is_valid():
            
            # create a list with each location
            input = request.POST["locationscustom"].splitlines()
            locations_to_submit_final = []

            for submitted_location in input:
                locations_to_submit_final.append(submitted_location)

            map_to_submit = Map(
                map_type=1,
                num_of_locations=len(locations_to_submit_final),
                mapillary_image_key=locations_to_submit_final
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

def create_by_region(request):
    """Creates a map with locations randomly selected inside a polygon"""

    if request.method == "POST":
        form = GenerateMapByRegion(request.POST)
        if form.is_valid():        
            
            # create a list with each location
            input = request.POST["locations"].splitlines()
            locations_to_submit_final = []

            for random_location in input:
                locations_to_submit_final.append(random_location)
            
            map_to_submit = Map(
                map_type=2,
                num_of_locations=len(locations_to_submit_final),
                mapillary_image_key=locations_to_submit_final
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

def get_location(picked_box, request):
    """Selects a random location inside a bbox
    
    This function takes a bbox and makes a request to mapillary api
    selecting a random image, after performing some validations

    Parameters
    ----------
    picked_bbox : 
        Randomly selected bbox from the list
    
    Returns
    -------
        Appends randomly selected image key inside the bbox
        to a list, if it passes all checks
    
    Validates
    ---------
        If request contains data
        If the images are not from the user "wbs" and "adminmapillary"
        If image is not reported
    """
    
    url = "https://a.mapillary.com/v3/images?client_id=" + os.environ.get("CLIENT_ID") + "&per_page=50&min_quality_score=3&bbox=" + picked_box
    req = urllib.request.urlopen(url) 
    data = json.load(req)
    
    #Make sure request contains data
    if len(data["features"]) != 0:
        randomly_selected_image = random.choice(data["features"])
        
        #filter user 'wbs' and 'adminmapillary' (low quality and wrong coordinates)
        if randomly_selected_image["properties"]["username"] != "wbs" and randomly_selected_image["properties"]["username"] != "adminmapillary": 
            
            #Check if the randomly chosen image is reported
            check_image_reported = check_reported(request, randomly_selected_image["properties"]["key"]).content
            if check_image_reported.decode('utf-8') == 'OKAY':
                locations_to_submit_final.append(randomly_selected_image["properties"]["key"])
                print("CREATED " + randomly_selected_image["properties"]["key"])
            else: 
                get_location(picked_box)
    else:
         get_location(picked_box)
 
def create_world(request):
    """Creates a map with random locations

    To create a map with random locations all over the world we drew multiple bboxes
    manually containing multiple regions of the world. We then select one randomly and
    resize it also randomly (so that per_page argument gives us different images). We then
    make a request to the mapillary API with a thread for each location. We then choose 
    one random image from the ones given and we do multiple checks, making sure
    the image is allowed to be used
    """

    if request.method == "POST":
        form = GenerateRandomWorld(request.POST)
        if form.is_valid():
            
            chosen_bboxes = [] #bboxes that were randomly chosen
            submitted_number_of_locations = request.POST["numoflocations"]
        
             
            for i in range(0, int(submitted_number_of_locations)):
                """Select a random bbox for each location, with random sizes"""

                picked_box = random.choice(bboxes_for_create_world).split(',') #choose a random box and split coordinates
                
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
            
            # Run a thread for each location, that gets a random image on each chose bbox 
            with concurrent.futures.ThreadPoolExecutor(max_workers=int(submitted_number_of_locations)) as e:
                for i in range(0, int(submitted_number_of_locations)):
                    e.submit(get_location, chosen_bboxes[i], request)
            
            map_to_submit = Map(
                map_type=3,
                num_of_locations=len(locations_to_submit_final),
                mapillary_image_key=locations_to_submit_final
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
    """Report an image
    
    This function reports an image and removes it from
    all the maps that contain it

    Parameters:
    ----------
        image_key :
            key to the image being reported
        reason_low_quality :
            1 if the image was reported because of low quality
        reason_wrong_coordinates :
            1 if the image was reported because of wrong coordinates
    
    Validates:
    ----------
        Makes sure if the image hasn't been reported
    """

    try:
        is_already_reported = ReportedImages.objects.get(mapillary_image=image_key)
        return HttpResponse("This image is already reported, therefore it will not be reported again")
    except ReportedImages.DoesNotExist:
        all_the_maps = Map.objects.all()
        for current_map in all_the_maps:
            """
            Find occurrences of the image in all maps and remove it,
            If the resulting number of locations in the map is less than 5
            delete the map
            """

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

def check_reported(request, image_key):
    """Checks if an image is reported"""
    try: 
        reported = ReportedImages.objects.get(mapillary_image=image_key)
        return HttpResponse("REPORTED")     
    #No image reported with that id
    except ReportedImages.DoesNotExist: 
        return HttpResponse("OKAY")
