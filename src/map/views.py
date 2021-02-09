from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Map
from .forms import GenerateRandomWorld
import os
import json
import urllib



#Main page of the map/ app
def index(request):
	return render(request, 'map/index.html')

#Let the user choose what places to add to a new map, by clicking
def create_custom(request):
	
	if request.method == 'POST':

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
			creator="tester",
			num_of_locations=len(locations_to_submit_final),
			mapillary_image_key=locations_to_submit_final,
			times_played=123
		)

		map_to_submit.save()
		messages.success(request, "Custom map created!")
		return redirect("/")
		
	else:
		return render(request, 'map/create-custom.html') 

#Let the user draw a polygon on the map, creating the "perimter"
#Give random coordinates, that are inside the polygon
def create_by_region(request):
	if request.method == "POST":
		
		input = request.POST["locations"].splitlines()
		locations_to_submit_final = []


		for random_location in input:
			locations_to_submit_final.append(random_location)
		
		map_to_submit = Map(name="testByRegion",
			creator="tester",
			num_of_locations=len(locations_to_submit_final),
			mapillary_image_key=locations_to_submit_final,
			times_played=441
		)

		map_to_submit.save()
		
		messages.success(request, "Random map by region created!")
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


			url = "https://a.mapillary.com/v3/images?client_id=" + os.environ.get("CLIENT_ID") + "&per_page=" + submitted_number_of_locations

			req = urllib.request.urlopen(url)
			data = json.load(req)
			
			#Add all the random pictures to the list that will be submitted
			for i in range(0, len(data["features"])):
				locations_to_submit_final.append(data["features"][i]["properties"]["key"])

			map_to_submit = Map(name="testRandomWorld",
				creator="tester",
				num_of_locations=len(locations_to_submit_final),
				mapillary_image_key=locations_to_submit_final,
				times_played=321
			)

			map_to_submit.save()
			
			messages.success(request, "Random map created!")
			return redirect("/")
		else:
			messages.error(request, "Something wrong with your input! Is it more than 5?")
			return redirect("/map/createworld") 
	else:
		form = GenerateRandomWorld()
	
	return render(request, 'map/create-world.html')

def get_map(request, id):
	try:
		#TODO (must do ASAP): Return a JSON instead
		map = Map.objects.filter(pk=id).values()
		return JsonResponse({"map": list(map)})
	except Map.DoesNotExist:
		raise Http404("No map with that id")
	