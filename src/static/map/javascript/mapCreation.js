
/*
TO FIND IMAGES CLOSE TO COORDINATES
https://www.mapillary.com/developer/api-documentation/#search-images
https://a.mapillary.com/v3/images?client_id=MGNWR1hFdWVhb3FQTTJxcDZPUExHZzo2NTE4YmM3NmY0YWYyNGYy&closeto=-122.3079,47.6537 (lng,lat) (RADIUS IS 100m, by default)
*/
/*
TO DELETE A MARKER, JUST USE markersCoords.markers[i].remove()
AND FOR THE JSON
delete markersaCoords.markers[i]
*/


mapboxgl.accessToken = 'pk.eyJ1IjoiY2FzZWlubWVsbCIsImEiOiJja2tpZWU3bG8wNXN4MnBzNzVibnN5dG90In0.D6Y43QmUBiirztruQeEFHA';
let map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11', // stylesheet location
    center: [-9.136068933525848, 38.74608203665869], // starting position [lng, lat]
    zoom: 9 // starting zoom
});

/**
 * 
 * GLOBAL VARIABLES
 * 
 */

let i = 0;

let mapillarySource;

let chosenCoords = {
    "coordinates": []
}

let markersCoords = {
    "markers": []
}

let table = document.getElementById("show-coords");


function isThereACloseImage(lng, lat) {
    return "https://a.mapillary.com/v3/images?client_id=MGNWR1hFdWVhb3FQTTJxcDZPUExHZzo2NTE4YmM3NmY0YWYyNGYy&closeto=" + lng + "," + lat; 
}


function deleteSelection(indexToDelete) {
    //Instead of using delete, set it to an empty string and filter out on the backend
    chosenCoords.coordinates[indexToDelete] = ""; 
    markersCoords.markers[indexToDelete].remove(); //Remove marker from map
    markersCoords.markers[indexToDelete] = "";
}


function populateTable(index) {
    //Get the table and insert a row after the last element
    let rowToInsert = table.insertRow(-1); //Add a new row to end of table

    let cellToInsertInput = rowToInsert.insertCell(0); //Select cell for button
    let cellToInsertCoords = rowToInsert.insertCell(1); //Select cell for coords

    //Add the content to the cells
    let deleteCoordinateButton = document.createElement("input");
    deleteCoordinateButton.setAttribute("type", "button");
    deleteCoordinateButton.setAttribute("id", index);
    deleteCoordinateButton.setAttribute("class", "btn btn-danger");
    deleteCoordinateButton.value = "Delete";
    cellToInsertInput.appendChild(deleteCoordinateButton);

    let coordinateText = document.createTextNode(chosenCoords.coordinates[index]);
    cellToInsertCoords.appendChild(coordinateText);
    

    deleteCoordinateButton.onclick = function() {
        table.deleteRow(rowToInsert.rowIndex);
        deleteSelection(deleteCoordinateButton.getAttribute("id")); //Delete chosenCoords and markersCoords info about that object
    }
}


function handleSubmit() {

    for(i = 0; i < chosenCoords.coordinates.length; i++) {
        if(chosenCoords.coordinates[i] != "") {
            //Every line on the text area will be in the form lng,lat
            //On the backend we must get every line and separate by comma and make an array for each pair
            document.getElementById("locations-to-submit").value += chosenCoords.coordinates[i] + '\n';        
        }
    }    
}

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
    

    let message = document.createElement("DIALOG");
    let errorText = document.createTextNode("Oops... There's no available street view close to that point. Choose one closer to a green spot! Must be at least 100 meters close!");
    map.on('click', function(e){
        message.remove();
        
        $.ajaxSetup({
            async: false
        });
        $.get(isThereACloseImage(e.lngLat.wrap().lng, e.lngLat.wrap().lat), function(data) {
            if(data.features.length === 0) {			
                message.setAttribute("open","open");
                message.appendChild(errorText);
                document.getElementById("dialog-container").appendChild(message);
            } else {
                
                chosenCoords["coordinates"].push(data["features"][0]["properties"].key); // Add the key to a json object
                
                let marker = new mapboxgl.Marker()
                .setLngLat([e.lngLat.wrap().lng, e.lngLat.wrap().lat])
                .addTo(map);
        
                markersCoords["markers"].push(marker); // Add every marker to a marker json object

                //Add elements to table
                populateTable(i);

                i++;
            }
            
        });

    });
});
