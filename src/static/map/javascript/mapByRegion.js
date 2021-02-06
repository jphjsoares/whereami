mapboxgl.accessToken = 'pk.eyJ1IjoiY2FzZWlubWVsbCIsImEiOiJja2tpZWU3bG8wNXN4MnBzNzVibnN5dG90In0.D6Y43QmUBiirztruQeEFHA';

let map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11', // stylesheet location
    center: [-68.13734351262877, 45.137451890638886], // starting position [lng, lat]
    zoom: 5 // starting zoom
});

var draw = new MapboxDraw({
    displayControlsDefault: false,
    controls: {
        polygon: true,
        trash: true
    }
});
map.addControl(draw);

map.on('draw.create', updateArea);
map.on('draw.delete', updateArea);
map.on('draw.update', updateArea);

function generateRandomPointsOnRegion(polygon) {

	let polyBbox = turf.bboxPolygon(turf.bbox(polygon))
	let points = turf.randomPoint(1, polyBbox);


		//TODO: Check if mapillary has available images in the polygon!

	if(turf.booleanPointInPolygon(points["features"][0]["geometry"], polygon)) { //check if the point is inside the polygon
		let generatedPoint = [points["features"][0]["geometry"]["coordinates"][0], points["features"][0]["geometry"]["coordinates"][1]];
		
		//marker and the console.log are only used for debugging
		console.log(generatedPoint);
		//var marker = new mapboxgl.Marker(generatedPoint).setLngLat().addTo(map);
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
}
