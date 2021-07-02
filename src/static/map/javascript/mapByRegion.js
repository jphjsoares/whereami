//mapboxgl.accessToken = 'pk.eyJ1IjoiY2FzZWlubWVsbCIsImEiOiJja2tpZWU3bG8wNXN4MnBzNzVibnN5dG90In0.D6Y43QmUBiirztruQeEFHA';
mapboxgl.accessToken = 'pk.eyJ1IjoiY2FzZWlubWVsbCIsImEiOiJja2x4d3ZobnAweWYyMndvNmw5d3Z6M2Q2In0.Oot19uqvGNmeGXD066LMJQ';

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
document.getElementById("submit-button").disabled = true;

map.addControl(draw);
map.on('draw.create', checkForPolygons);
map.on('draw.delete', checkForPolygons);
map.on('draw.update', checkForPolygons);

//Show tiles on map by region
map.on('style.load', function() {
    var mapillarySource = {
        type: 'vector',
        tiles: ["https://tiles3.mapillary.com/v0.1/{z}/{x}/{y}.mvt"],
        minzoom: 0,
        maxzoom: 14
    };

    map.addSource('mapillary', mapillarySource);
    
    //For long range
    map.addLayer({
        'id': 'mapillary',
        'type': 'circle',
        'source': 'mapillary',
        'source-layer':'mapillary-sequence-overview',
        'paint': {
            'circle-opacity': 0.2,
            'circle-color': 'rgb(53, 175, 109)',
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
 * @param  {Number} lng Randomly generated longitude
 * @param  {Number} lat Randomly generated latitude
 * @return {String}     Mapillary API url
 */
function buildUrl( box0, box1, box2, box3, lng, lat) {
    return "https://a.mapillary.com/v3/images?bbox=" + box0 + ',' + box1 + ',' + box2 + ',' + box3 + "&closeto=" + lng + ',' + lat + "&radius=50000&per_page=1&client_id=MGNWR1hFdWVhb3FQTTJxcDZPUExHZzo2NTE4YmM3NmY0YWYyNGYy";
}

/**
 * Generates a random point inside a polygon
 * 
 * @param {Polygon} polygon Drawn polygon by the user
 */
function generateRandomPointsOnRegion(polygon) {

    let polyBbox = turf.bboxPolygon(turf.bbox(polygon)); //Generate a polybbox with the given polygon
    let points = turf.randomPoint(1, polyBbox); //Generate one random point inside that polybox

    let newUrl = buildUrl(polyBbox["bbox"][0], polyBbox["bbox"][1], polyBbox["bbox"][2], polyBbox["bbox"][3], 
        points["features"][0]["geometry"]["coordinates"][0], 
        points["features"][0]["geometry"]["coordinates"][1]); //Build url to get point inside the bbox

    $.get(newUrl, function(data) {
        //If we get a valid image and if that image is INSIDE THE DRAWN POLYGON (not bbox) and if quality is more than 3
        if(data.features.length !== 0 && turf.booleanPointInPolygon(points["features"][0]["geometry"], polygon) && data["features"][0]["properties"].quality_score > 3) {      
            
            //Check if the image is reported
            let checkIfReported = window.location.origin + "/map/check_reported/" + data["features"][0]["properties"].key;
            $.get(checkIfReported, function(response) {
                if(response == 'OKAY') {
                    console.log(response);
                    coordinatesToSubmit.push(data["features"][0]["properties"].key); //Submit the point
                }
            });
        } else {
            generateRandomPointsOnRegion(polygon);
        }
    });
}


/**
 * Adds streetviews to the form
 */
function getReadyForSubmit() {
    for(locationIndex = 0; locationIndex < coordinatesToSubmit.length; locationIndex++) {
        //Every line on the text area will be in the form lng,lat
        //On the backend we must get every line and separate by comma and make an array for each pair
        document.getElementById("locations-to-submit").value += coordinatesToSubmit[locationIndex] + '\n';
    }
    $('form').unbind('submit').submit();
}

/**
 * Every 50ms check if the form is ready to be submitted
 */
function checkIfPopulated() {
    let timer = window.setInterval(function(){
        if (coordinatesToSubmit.length == 10) {
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
