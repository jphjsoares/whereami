mapboxgl.accessToken = 'pk.eyJ1IjoiY2FzZWlubWVsbCIsImEiOiJja2tpZWU3bG8wNXN4MnBzNzVibnN5dG90In0.D6Y43QmUBiirztruQeEFHA';
let map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11', // stylesheet location
    center: [-9.136068933525848, 38.74608203665869], // starting position [lng, lat]
    zoom: 9 // starting zoom
});

let mapillarySource;

let chosenCoords = {
    "coordinates": []
}

let markersCoords = {
    "markers": []
}

/*
TO FIND IMAGES CLOSE TO COORDINATES
https://www.mapillary.com/developer/api-documentation/#search-images
*/
/*
TO DELETE A MARKER, JUST USE markersCoords.markers[i].remove()
AND FOR THE JSON
delete markersaCoords.markers[i]
*/

map.on('style.load', function() {
    var mapillarySource = {
        type: 'vector',
        tiles: ["https://tiles3.mapillary.com/v0.1/{z}/{x}/{y}.mvt"],
        minzoom: 0,
        maxzoom: 14
    };

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
            'line-width': 3
        }
    });
    
    let i = 0;

    map.on('click', function(e){
        
        chosenCoords["coordinates"].push(e.lngLat.wrap()); // Add all the coordinates to a json object
        
        var marker = new mapboxgl.Marker()
        .setLngLat([chosenCoords.coordinates[i].lng, chosenCoords.coordinates[i].lat])
        .addTo(map);

        markersCoords["markers"].push(marker); // Add every marker to a marker json object
        let newCoordinate = document.createElement("li");
        let coordinateContent = document.createTextNode(chosenCoords.coordinates[i]);
        newCoordinate.appendChild(coordinateContent);
        newCoordinate.id = i;

        let element = document.getElementById("show-coords");
        element.appendChild(newCoordinate);
        console.log(chosenCoords["coordinates"]);
        i++;
    });

});


