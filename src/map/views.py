from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
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
	
	#TODO: Only allow POST requests if the user is signed in
	if request.method == 'POST':

		input = request.POST["locations"].splitlines()
		locations_to_submit_final = []

		if len(input) < 5: #Also be careful with xss and other vulns
			#Use django messages to show this error!

			return HttpResponse("Oops... Please select 5 or more locations")
		
		# gets lng and lat separated, ready for storing
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
		#And then redirect to a page!
	else:
		return render(request, 'map/create-custom.html')

#Let the user draw a polygon on the map, creating the "perimter"
#Give random coordinates, that are inside the polygon
def create_by_region(request):                                      
	return render(request, 'map/create-by-region.html')

#By defining how many locations to set,
#Give random locations around the world
def create_world(request):

	#TODO: Only allow POST requests if the user is signed in
	if request.method == "POST":
		form = GenerateRandomWorld(request.POST)
		if form.is_valid():

			locations_to_submit_final = []
			submitted_number_of_locations = request.POST["numoflocations"]


			url = "https://a.mapillary.com/v3/images?client_id=" + os.environ.get("CLIENT_ID") + "&per_page=" + submitted_number_of_locations

			request = urllib.request.urlopen(url)
			data = json.load(request)
			
			#Add all the random pictures to the list that will be submitted
			for i in range(0, len(data["features"])):
				locations_to_submit_final.append(data["features"][i]["geometry"]["coordinates"])

			#TODO: Create and save the new map

			return HttpResponse(locations_to_submit_final)
	else:
		form = GenerateRandomWorld()
	
	return render(request, 'map/create-world.html')