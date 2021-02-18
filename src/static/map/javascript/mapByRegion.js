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

document.getElementById("submit-button").disabled = true;

map.on('draw.create', checkForPolygons);
map.on('draw.delete', checkForPolygons);
map.on('draw.update', checkForPolygons);



function checkForPolygons() {
    let polygon = draw.getAll().features;
    if(polygon.length > 0) {
        document.getElementById("submit-button").disabled = false;
    } else {
        document.getElementById("submit-button").disabled = true;
    }       
}


function buildUrl( box0, box1, box2, box3, lng, lat) {
    //Be careful with radius, might generate a point out of polygon, requires more testing
    return "https://a.mapillary.com/v3/images?bbox=" + box0 + ',' + box1 + ',' + box2 + ',' + box3 + "&closeto=" + lng + ',' + lat + "&radius=50000&per_page=1&client_id=MGNWR1hFdWVhb3FQTTJxcDZPUExHZzo2NTE4YmM3NmY0YWYyNGYy";
}

function generateRandomPointsOnRegion(polygon) {

    let polyBbox = turf.bboxPolygon(turf.bbox(polygon))
    let points = turf.randomPoint(1, polyBbox);

    let newUrl = buildUrl(polyBbox["bbox"][0], polyBbox["bbox"][1], polyBbox["bbox"][2], polyBbox["bbox"][3], 
        points["features"][0]["geometry"]["coordinates"][0], 
        points["features"][0]["geometry"]["coordinates"][1]);

    $.get(newUrl, function(data) {
        if(data.features.length !== 0 && turf.booleanPointInPolygon(points["features"][0]["geometry"], polygon)) {          
            coordinatesToSubmit.push(data["features"][0]["properties"].key);
        } else {
            generateRandomPointsOnRegion(polygon);
        }
    });
}

function getReadyForSubmit() {
    for(locationIndex = 0; locationIndex < coordinatesToSubmit.length; locationIndex++) {
        //Every line on the text area will be in the form lng,lat
        //On the backend we must get every line and separate by comma and make an array for each pair
        document.getElementById("locations-to-submit").value += coordinatesToSubmit[locationIndex] + '\n';
    }
    $('form').unbind('submit').submit();
}

function checkIfPopulated() {
    let timer = window.setInterval(function(){
        if (coordinatesToSubmit.length == 10) {
            window.clearInterval(timer);
            console.log(coordinatesToSubmit);
            getReadyForSubmit();
        }
    }, 50);
}


$("#form").on('submit', function(e) {
    e.preventDefault();
    let polygon = draw.getAll().features;
    document.getElementById("main-content").style.display = "none";
    document.getElementById("loading").style.display = "block";
    document.getElementById("loading-text").style.display = "block";
    console.log("Starting....")

    for (numOfPolygons = 0; numOfPolygons < polygon.length; numOfPolygons++) {
        
        //Number of points
        for(let i = 0; i < 10; i++) {
            generateRandomPointsOnRegion(polygon[numOfPolygons]);
        }
        checkIfPopulated();
    }
});
