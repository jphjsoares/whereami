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
    zoom: 3 // starting zoom
});

window.addEventListener("resize", function() { mly.resize(); });



let toGuess = []; //[imageIndex, [lnt,lat]]
let markers = [];
let nextImage = 1;

//Get the exact locs to guess
for(let i = 0; i < keys.length; i++) {

    //TODO:get the image in the same order
    let url = "https://a.mapillary.com/v3/images/"  + keys[i] + "?client_id=MGNWR1hFdWVhb3FQTTJxcDZPUExHZzo2NTE4YmM3NmY0YWYyNGYy";
    $.get(url, function(data) {
        toGuess.push([i, data["geometry"]["coordinates"]]); //store it in a way so that we can access the index of an image and the respective coordinates
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


$("#open-map").click(function(){
    document.getElementById("open-map").style.display = "none";
    $("#mly").css("width", "65%");
    $("#map").css("flex-grow", "1");
    map.resize();   
});





$("#trigger-guess").click(function() {
    $('#map').click(false); //Dont allow clicks
    document.getElementById("trigger-guess").style.display = "none";
    let realLng;
    let realLat;
    let guessedLng = markers[0]["_lngLat"].lng;
    let guessedLat = markers[0]["_lngLat"].lat;
    let lineOfDistance = {
        'type': 'FeatureCollection',
            'features': [
                {
                'type': 'Feature',
                'geometry': {
                    'type': 'LineString',
                    'properties': {},
                    'coordinates': []
                }
            }
        ]
    };


    let guessTurfPoint = turf.point([guessedLng, guessedLat]); //Guess made by user


    for(let i = 0; i < toGuess.length; i++) {
        if(toGuess[i][0] === nextImage-1) {
            realLng = toGuess[i][1][0]; //lng of real location
            realLat = toGuess[i][1][1]; //lat of real location
        }
    }
    
    lineOfDistance["features"][0]["geometry"]["coordinates"].push([realLng,realLat]);
    lineOfDistance["features"][0]["geometry"]["coordinates"].push([guessedLng,guessedLat]);

    let exactLocation = new mapboxgl.Marker({
            color:"#fc0303"
        })
        .setLngLat([realLng, realLat])
        .addTo(map);

    markers.push(exactLocation);

    let realTurfPoint = turf.point([markers[1]["_lngLat"].lng, markers[1]["_lngLat"].lat]);

    let distanceBetweenPoints = turf.distance(guessTurfPoint, realTurfPoint);

    map.addSource('LineString', {
        'type': 'geojson',
        'data': lineOfDistance
    });

    map.addLayer({
        'id': 'LineString',
        'type': 'line',
        'source': 'LineString',
        'layout': {
            'line-join': 'round',
            'line-cap': 'round'
        },
        'paint': {
            'line-color': '#000',
            'line-width': 1
        }
    });

    console.log(distanceBetweenPoints);
});