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
    zoom: 9 // starting zoom
});

window.addEventListener("resize", function() { mly.resize(); });
