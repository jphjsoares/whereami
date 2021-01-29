mapboxgl.accessToken = 'pk.eyJ1IjoiY2FzZWlubWVsbCIsImEiOiJja2tpZWU3bG8wNXN4MnBzNzVibnN5dG90In0.D6Y43QmUBiirztruQeEFHA';
let map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11', // stylesheet location
    center: [-74.5, 40], // starting position [lng, lat]
    zoom: 12 // starting zoom
});

var mapillarySource;

map.on('style.load', function() {
    var mapillarySource = {
        type: 'vector',
        tiles: ['https://tiles3.mapillary.com/v0.1/{z}/{x}/{y}.mvt'],
        minzoom: 0,
        maxzoom: 14
    };
});


map.addSource('mapillary', mapillarySource);

map.addLayer({
    'id': 'mapillary',
    'type': 'line',
    'source': 'mapillary',
    'source-layer': 'mapillary-sequences',
    'layout': {
        'line-cap': 'round',
        'line-join': 'round'
    },
    'paint': {
        'line-opacity': 0.6,
        'line-color': 'rgb(53, 175, 109)',
        'line-width': 2
    }
});