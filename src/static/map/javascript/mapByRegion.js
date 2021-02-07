mapboxgl.accessToken = 'pk.eyJ1IjoiY2FzZWlubWVsbCIsImEiOiJja2tpZWU3bG8wNXN4MnBzNzVibnN5dG90In0.D6Y43QmUBiirztruQeEFHA';

let map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11', // stylesheet location
    center: [-68.13734351262877, 45.137451890638886], // starting position [lng, lat]
    zoom: 5 // starting zoom
});

let draw = new MapboxDraw({
    displayControlsDefault: false,
    controls: {
        polygon: true,
        trash: true
    }
});

let coordinatesToSubmit = []


map.addControl(draw);


function buildUrl( box0, box1, box2, box3, lng, lat) {
	return "https://a.mapillary.com/v3/images?bbox=" + box0 + ',' + box1 + ',' + box2 + ',' + box3 + "&closeto=" + lng + ',' + lat + "&per_page=1&client_id=MGNWR1hFdWVhb3FQTTJxcDZPUExHZzo2NTE4YmM3NmY0YWYyNGYy";
}

function generateRandomPointsOnRegion(polygon) {

	let polyBbox = turf.bboxPolygon(turf.bbox(polygon))
	let points = turf.randomPoint(1, polyBbox);

	let newUrl = buildUrl(polyBbox["bbox"][0], polyBbox["bbox"][1], polyBbox["bbox"][2], polyBbox["bbox"][3], 
		points["features"][0]["geometry"]["coordinates"][0], 
		points["features"][0]["geometry"]["coordinates"][1]);
	
	
	console.log(newUrl)

	//TODO: Check if mapillary has available images in the polygon!
	if(turf.booleanPointInPolygon(points["features"][0]["geometry"], polygon)) { //check if the point is inside the polygon
		let generatedPoint = [points["features"][0]["geometry"]["coordinates"][0], points["features"][0]["geometry"]["coordinates"][1]];
		coordinatesToSubmit.push(generatedPoint);
	} else {
		generateRandomPointsOnRegion(polygon);
	}
}

function handleClick() {
	
	let allPolygons = draw.getAll();
	let polygon = draw.getAll().features;
	let pointsToSubmit = []

	for (numOfPolygons = 0; numOfPolygons < polygon.length; numOfPolygons++) {
		
		//Number of points
		for(i = 0; i < 10; i++) {
			generateRandomPointsOnRegion(polygon[numOfPolygons]);
		}
	}

	for(locationIndex = 0; locationIndex < coordinatesToSubmit.length; locationIndex++) {
		//Every line on the text area will be in the form lng,lat
        //On the backend we must get every line and separate by comma and make an array for each pair
		document.getElementById("locations-to-submit").value += coordinatesToSubmit[locationIndex][0] + "," + coordinatesToSubmit[locationIndex][1] + '\n';
	}
	
}
