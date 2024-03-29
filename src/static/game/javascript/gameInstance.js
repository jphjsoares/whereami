const mapillaryApiKey = "MLY|7677134818979003|9333a16aef0cf8d9a8e79fa6ecd7bac3";
let { Viewer } = mapillary;

let viewer = new Viewer({
    accessToken: mapillaryApiKey,
    container: 'mly',
    imageId: keys[0],
});

mapboxgl.accessToken = 'pk.eyJ1IjoiY2FzZWlubWVsbCIsImEiOiJja3o4anZjOHMwdWQxMndxbTFoZGM3YzI1In0.B6eDbdCeO01bXCrDkDZIdw';
let map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11', // stylesheet location
    center: [-9.136068933525848, 38.74608203665869], // starting position [lng, lat]
    zoom: 3 // starting zoom
});

let toGuess = []; //[imageIndex, [lnt,lat]]
let markers = [];
let nextImage = 1;
let hasGuessed = false;
let mapIsOpen = false;
let score = 0;
let howManyImages = keys.length;
let alertOfReportHasBeenShown = false;
let pointsToAdd = 0;

/**
 * Makes network requests to get coordinates for
 * each image key. To compare every guess
 */
for(let i = 0; i < keys.length; i++) {

    let url = "https://graph.mapillary.com/" + keys[i] + "?fields=id,computed_geometry";
    $.ajax({
        url: url,
        type: "GET",
        headers: {"Authorization": "OAuth MLY|7677134818979003|9333a16aef0cf8d9a8e79fa6ecd7bac3"},
        contentType: "application/json",
        success: function(result) {
            toGuess.push([i, result.computed_geometry.coordinates]);

        }
    });
}

document.getElementById("img-index").innerText = nextImage + " / " + keys.length;
document.getElementById("game-score").innerText = "Score " + score;

/**
 * 
 * Updates current street view,
 * Showing next image
 */
function nextImageSetup() {
    mapIsOpen = false;
    viewer.remove();
    viewer = new Viewer({
        accessToken:mapillaryApiKey,
        container:'mly',
        imageId: keys[nextImage],
    });
    nextImage++;
    document.getElementById("img-index").innerHTML = nextImage + " / " + keys.length;
}


/**
 * Handles all the marker placements
 */
map.on('click', function(e){
    if (hasGuessed) { //Don't allow map clicking after guess has been taken!
        return;
    }
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


/**
 * Opens map when user clicks "I THINK I KNOW"
 */
function openMap() {
    //open
    if (!mapIsOpen) {
        mapIsOpen = true;
        $("#mly").css("width", "65%");
        $("#map").css("flex-grow", "1");
        map.resize();
    } else { //close
        mapIsOpen = false;
        $("#mly").css("width", "100%");
        $("#map").css("flex-grow", "1");
        map.resize();
    }
}



/**
 * Handles a user guess, showing real location and
 * updating score
 */
function handleGuess() {
    hasGuessed = true; //Notify the code that the user has submitted a guess
    document.getElementById("trigger-guess").style.display = "none"; //Hide guess button to prevent bugs
    document.getElementById("open-map").style.display = "none";
    document.getElementById("map").style.width = "65%"; //Make map bigger
    document.getElementById("mly").style.width = "35%"; //Make viewer smaller
    map.resize();
    
    let realLng;
    let realLat;
    let guessedLng = markers[0]["_lngLat"].lng;
    let guessedLat = markers[0]["_lngLat"].lat;

    //This gets the coordinates of the image being seen
    //Very weird, but it works lol
    for(let i = 0; i < toGuess.length; i++) {
        if(toGuess[i][0] === nextImage-1) {
            realLng = toGuess[i][1][0]; //lng of real location
            realLat = toGuess[i][1][1]; //lat of real location
        }
    }
    
    
    //Add real location marker
    let exactLocation = new mapboxgl.Marker({
            color:"#fc0303"
        })
        .setLngLat([realLng, realLat])
        .addTo(map);
    markers.push(exactLocation);

    //Calculate the distance in km
    let distanceBetweenPoints = turf.distance(turf.point([guessedLng, guessedLat]), turf.point([realLng, realLat]));

    //If the guess was under 2250 km give points
    if (distanceBetweenPoints <= 2250) {
        pointsToAdd = 2250-Math.round(distanceBetweenPoints);
        score  = score + pointsToAdd;
        document.getElementById("game-score").innerHTML = "Score " + score;
    }

    //This is to draw the line string on the map
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

    lineOfDistance["features"][0]["geometry"]["coordinates"].push([realLng,realLat]);
    lineOfDistance["features"][0]["geometry"]["coordinates"].push([guessedLng,guessedLat]);

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

    //Show results div
    let guessResultText = "You were " + (Math.round(distanceBetweenPoints * 10) / 10) + " km far!";
    let parToInsert = "<p class='lead distance-result'>" + guessResultText + "</p>";
    $(parToInsert).insertBefore('#next-img');
    document.getElementById("guess-results").style.display = "block";

    //this will appear once we guessed the FINAL image
    //handles end of game
    if(nextImage==keys.length) {
        document.getElementById("next-img").innerHTML = "End of game!";
        $("#next-img").click(function() {
            let updatePlayer = window.location.origin + '/game/ps/' + (window.location.href).split('/')[4] + '/' + score;
            $.get(updatePlayer, function(data) {
                let urlOfEndgame =  window.location.origin + '/game/eg/' + (window.location.href).split('/')[4];
                window.location.href = urlOfEndgame;
                console.log(data);    
            });
        });
    }
}


/**
 * Cleans interface and sets up window for
 * the next street view.
 */
function cleanUp() {
    document.getElementById("guess-results").style.display = "none";  //remove the div with results
    document.getElementById("open-map").style.display = "block"; //show button to open map
    $("#mly").css("width", "100%"); //make viewer page width
    $("#map").css("width", "0"); //hide map again
    hasGuessed = false; //Be able to take guess next round
    mapIsOpen = false;
    $(".distance-result").remove(); //Remove all the messages with distance of guesses

    //remove all markers from the map
    for(let i = 0; i < markers.length; i++) {
        markers[i].remove(); 
    }

    //remove all markers from the array so they can be reused
    markers = [];

    //Remove linestrings from previous guesses
    map.removeLayer("LineString");
    map.removeSource("LineString");

    map.resize();
    nextImageSetup();
}


/**
 * Handles a player reporting an image
 */
function reportImage() {
    let reason_low_quality = 0;
    let reason_wrong_coordinates = 0;

    //Reason for report
    if(document.getElementById("low-quality-check").checked){
        reason_low_quality = 1;
    }
    if(document.getElementById("wrong-coordinates-check").checked) {
        reason_wrong_coordinates = 1;
    }
    
    //Report the current image
    let urlOfReport = window.location.origin + "/map/report/"  + keys[nextImage-1] + "/" + reason_low_quality + "/" + reason_wrong_coordinates; 
    $.get(urlOfReport, function(data){
        console.log(data);
    });

    howManyImages--;

    //This will handle the report if it's made in the last viewer of the game
    if(nextImage==keys.length) {
    
        let updatePlayer = window.location.origin + '/game/ps/' + (window.location.href).split('/')[4] + '/' + score;
        $.get(updatePlayer, function(data) {
            let urlOfEndgame =  window.location.origin + '/game/eg/' + (window.location.href).split('/')[4];
            window.location.href = urlOfEndgame;
            console.log(data);    
        });
        
    } else {
        if(hasGuessed) {
            score = score - pointsToAdd;
            document.getElementById("game-score").innerHTML = "Score " + score;
            cleanUp();
        } else if (mapIsOpen) {
            document.getElementById("open-map").style.display = "block"; //show button to open map
            document.getElementById("trigger-guess").style.display = "none"; //Hide guess button to prevent bugs
            $("#mly").css("width", "100%"); //make viewer page width
            $("#map").css("width", "0"); //hide map again
            
            //remove all markers from the map
            for(let i = 0; i < markers.length; i++) {
                markers[i].remove(); 
            }
            mapIsOpen = false;
            nextImageSetup();
        } else {
            nextImageSetup();
        }
    }           
    document.getElementById("report-div").style.display = "none";
}

/**
 * ALL THE BUTTON CLICK HANDLERS
 */

$("#report-view").click(function(){
    let element = document.getElementById("report-div");
    if(howManyImages == 5 && !alertOfReportHasBeenShown) {
        alert("WARNING: REPORTING STREET VIEWS ON A 5 ACTIVE LOCATIONS MAP, WILL CAUSE THE MAP TO BE DELETED.\n\nTherefore, it will most likely cause strange behaviour. We never recommend our users to play a 5 location map only")
        alertOfReportHasBeenShown = true;
    }  
    if(element.style.display == "none") {
        element.style.display = "block";
    } else {
        element.style.display = "none";
    }
});

$("#image-button-reporter").click(reportImage);

$("#open-map").click(openMap);

$("#trigger-guess").click(handleGuess);

$("#next-img").click(cleanUp);
