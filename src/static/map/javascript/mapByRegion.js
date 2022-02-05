mapboxgl.accessToken = 'pk.eyJ1IjoiY2FzZWlubWVsbCIsImEiOiJja3o4anZjOHMwdWQxMndxbTFoZGM3YzI1In0.B6eDbdCeO01bXCrDkDZIdw';

let map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11', // stylesheet location
    center: [-9.136068933525848, 38.74608203665869], // starting position [lng, lat]
    zoom: 5 // starting zoom
});

let draw = new MapboxDraw({
    displayControlsDefault: false,
    controls: {
        polygon: true,
        trash: true
    }
});

let imageIdsToSubmit = []
document.getElementById("submit-button").disabled = true;

map.addControl(draw);
map.on('draw.create', checkForPolygons);
map.on('draw.delete', checkForPolygons);
map.on('draw.update', checkForPolygons);

//Show tiles on map by region
map.on('style.load', function() {
    map.addSource('mapillary', {
        type: 'vector',
        tiles: ['https://tiles.mapillary.com/maps/vtp/mly1_public/2/{z}/{x}/{y}?access_token=MLY|7677134818979003|9333a16aef0cf8d9a8e79fa6ecd7bac3'],
        minzoom: 6,
        maxzoom: 20
    });
    map.addLayer({
        'id': 'mapillary-sequences',
        'type': 'line',
        'source': 'mapillary',
        'source-layer': 'sequence',
        'layout': {
            'line-join': 'round',
            'line-cap': 'round'
        },
        'paint': {
            'line-color': '#05CB63',
            'line-width': 1
        }
    });
});


/**
 * Allows submit button to be clicked if there's
 * more than 1 polygon drawn
 */
function checkForPolygons() {
    let polygon = draw.getAll().features;
    if(polygon.length > 0) {
        document.getElementById("submit-button").disabled = false;
    } else {
        document.getElementById("submit-button").disabled = true;
    }       
}



/**
 * Builds url to get a street view
 * 
 * @param  {Float} box0 Min longitude of bbox
 * @param  {Float} box1 Min latitude of bbox
 * @param  {Float} box2 Max longitude of bbox
 * @param  {Float} box3 Max latitude of bbox
 * @return {String}     Mapillary API url
 */
function buildUrl( box0, box1, box2, box3) {
    return "https://graph.mapillary.com/images?fields=id,computed_geometry&limit=1&bbox=" + box0 + ',' + box1 + ',' + box2 + ',' + box3;
}

/**
 * Generates a random point inside a polygon
 * 
 * @param {Polygon} polygon Drawn polygon by the user
 */
async function generateRandomPointsOnRegion(polygon) {

    let polyBbox = turf.bboxPolygon(turf.bbox(polygon)); //Generate a polybbox with the given polygon
    let newUrl = buildUrl(polyBbox["bbox"][0], polyBbox["bbox"][1], polyBbox["bbox"][2], polyBbox["bbox"][3]);

    $.ajax({
        url: newUrl,
        type: "GET",
        headers: {"Authorization": "OAuth MLY|7677134818979003|9333a16aef0cf8d9a8e79fa6ecd7bac3"},
        contentType: "application/json",
        success: function(result) {
            
            // CAREFUL: this version does not take into account low quality images
            if (turf.booleanPointInPolygon(result["data"][0].computed_geometry.coordinates, polygon) && !imageIdsToSubmit.includes(result["data"][0].id)) {
                let checkIfReported = window.location.origin + "/map/check_reported/" + result["data"][0].id;
                $.get(checkIfReported, function(response) {
                    if(response == 'OKAY') {
                        imageIdsToSubmit.push(result["data"][0].id); //Submit the point
                    }
                });
            } else {
                generateRandomPointsOnRegion(polygon);
            }
        }
    });
}


/**
 * Adds streetviews to the form
 */
function getReadyForSubmit() {
    for(locationIndex = 0; locationIndex < imageIdsToSubmit.length; locationIndex++) {
        //Every line on the text area will be in the form lng,lat
        //On the backend we must get every line and separate by comma and make an array for each pair
        document.getElementById("locations-to-submit").value += imageIdsToSubmit[locationIndex] + '\n';
    }
    $('form').unbind('submit').submit();
}

/**
 * Every 50ms check if the form is ready to be submitted
 */
function checkIfPopulated() {
    let timer = window.setInterval(function(){
        if (imageIdsToSubmit.length == 10) {
            window.clearInterval(timer);
            getReadyForSubmit();
        }
    }, 50);
}


/**
 * Starts random street view generator
 */
$("#form").on('submit', function(e) {
    e.preventDefault();
    let polygon = draw.getAll().features; //Get all drawn polygons
    document.getElementById("main-content").style.display = "none";
    document.getElementById("footer").style.display = "none";
    document.getElementById("loading").style.display = "block";
    document.getElementById("loading-text").style.display = "block";

    for (numOfPolygons = 0; numOfPolygons < polygon.length; numOfPolygons++) {
        
        //Number of points
        for(let i = 0; i < 10; i++) {
            generateRandomPointsOnRegion(polygon[numOfPolygons]);
        }
        checkIfPopulated();
    }
});
