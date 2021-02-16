let mly = new Mapillary.Viewer({
	apiClient:"MGNWR1hFdWVhb3FQTTJxcDZPUExHZzo2NTE4YmM3NmY0YWYyNGYy",
	component: {
		cover: false,
	},
	container:'mly',
	imageKey: keys[0],
});

mapboxgl.accessToken = 'pk.eyJ1IjoiY2FzZWlubWVsbCIsImEiOiJja2tpZWU3bG8wNXN4MnBzNzVibnN5dG90In0.D6Y43QmUBiirztruQeEFHA';
let map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11', // stylesheet location
    center: [-9.136068933525848, 38.74608203665869], // starting position [lng, lat]
    zoom: 5 // starting zoom
});

window.addEventListener("resize", function() { mly.resize(); });

let toGuess = [];
let markers = [];
let nextImage = 1;

//Get the exact locs to guess
for(let i = 0; i < keys.length; i++) {

	//TODO:get the image in the same order
	let url = "https://a.mapillary.com/v3/images/"  + keys[i] + "?client_id=MGNWR1hFdWVhb3FQTTJxcDZPUExHZzo2NTE4YmM3NmY0YWYyNGYy";
	$.get(url, function(data) {
		toGuess.push(data["geometry"]["coordinates"]);
	});
}

//Change viewer
function nextImageSetup() {
	mly.remove();
	mly = new Mapillary.Viewer({
		apiClient:"MGNWR1hFdWVhb3FQTTJxcDZPUExHZzo2NTE4YmM3NmY0YWYyNGYy",
		component: {
			cover: false,
		},
		container:'mly',
		imageKey: keys[nextImage],
	});
	nextImage++;
}

map.on('click', function(e){
	if (markers.length > 0) {
		markers[0].remove(); //remove marker from map
		markers.pop(); //remove marker from array
	}
	let marker = new mapboxgl.Marker()
		.setLngLat([e.lngLat.wrap().lng, e.lngLat.wrap().lat])
		.addTo(map);
	markers.push(marker);
	document.getElementById("trigger-guess").style.display = "block";
});


$("#trigger-guess").click(function() {
	let guessTurfPoint = turf.point([markers[0]["_lngLat"]. lng,markers[0]["_lngLat"].lat]);
	
	let exactLocation = new mapboxgl.Marker({
			color:"#fc0303"
		})
		.setLngLat([toGuess[nextImage-1][0], toGuess[nextImage-1][1]])
		.addTo(map);
	markers.push(exactLocation);

	let realTurfPoint = turf.point([markers[1]["_lngLat"]. lng,markers[1]["_lngLat"].lat]);

	let distance = turf.distance(guessTurfPoint, realTurfPoint);
	console.log(distance);
});