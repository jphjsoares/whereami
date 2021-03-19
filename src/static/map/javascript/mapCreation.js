mapboxgl.accessToken = 'pk.eyJ1IjoiY2FzZWlubWVsbCIsImEiOiJja2tpZWU3bG8wNXN4MnBzNzVibnN5dG90In0.D6Y43QmUBiirztruQeEFHA';
let map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11', // stylesheet location
    center: [-9.136068933525848, 38.74608203665869], // starting position [lng, lat]
    zoom: 9 // starting zoom
});


let i = 0;
let mapillarySource;
let mapillaryImages = {
    "keys": []
}
let markersCoords = {
    "markers": []
}
let table = document.getElementById("show-coords");

/**
 * Builds url to get a street view
 * 
 * @param  {Number} lng Click longitude
 * @param  {Number} lat Click latitude
 * @return {String}     Mapillary API url
 */
function isThereACloseImage(lng, lat) {
    return "https://a.mapillary.com/v3/images?client_id=MGNWR1hFdWVhb3FQTTJxcDZPUExHZzo2NTE4YmM3NmY0YWYyNGYy&closeto=" + lng + "," + lat; 
}

/**
 * Deletes marker and key
 * 
 * @param {Number} indexToDelete index of the marker and key to remove
 */
function deleteSelection(indexToDelete) {
    //Instead of using delete, set it to an empty string and filter out on the backend (quickfix)
    mapillaryImages.keys[indexToDelete] = ""; 
    markersCoords.markers[indexToDelete].remove(); //Remove marker from map
    markersCoords.markers[indexToDelete] = "";
}

/**
 * Inserts new marker, location and button of a 
 * chosen location
 * 
 * @param {Number} index key and marker index
 * @param {String} colorOfMarker custom color of marker and button
 */
function populateTable(index, colorOfMarker) {
    //Get the table and insert a row after the last element
    let rowToInsert = table.insertRow(-1); //Add a new row to end of table

    let cellToInsertInput = rowToInsert.insertCell(0); //Select cell for button
    let cellToInsertCoords = rowToInsert.insertCell(1); //Select cell for key

    //Delete button
    let deleteCoordinateButton = document.createElement("button");
    deleteCoordinateButton.setAttribute("id", index);
    deleteCoordinateButton.setAttribute("class", "btn btn-danger");
    deleteCoordinateButton.style.backgroundColor = colorOfMarker;
    deleteCoordinateButton.style.borderColor = colorOfMarker;
    deleteCoordinateButton.innerText = "Delete";
    cellToInsertInput.appendChild(deleteCoordinateButton); //Add button

    //Selected image key label
    let imageKey = document.createTextNode(mapillaryImages.keys[index]);
    cellToInsertCoords.appendChild(imageKey); 

    deleteCoordinateButton.onclick = function() {
        table.deleteRow(rowToInsert.rowIndex); //remove row from table
        deleteSelection(deleteCoordinateButton.getAttribute("id")); //Delete mapillaryImages and markers about that object
    }
}


/**
 * Adds streetviews to the form
 */
function handleSubmit() {

    for(i = 0; i < mapillaryImages.keys.length; i++) {
        if(mapillaryImages.keys[i] != "") {
            document.getElementById("locations-to-submit").value += mapillaryImages.keys[i] + '\n';        
        }
    }    
}

/**
 * Generates random color for each location
 * @returns custom color
 */
function getRandomColor() {
    let letters = '0123456789ABCDEF';
    let color = '#';
    
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

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

    //For close range
    map.addLayer({
        'id': 'mapillary2',
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
    
    //Show loading icon after choosing location
    $(document).on({
        ajaxStart: function(){
            $("#loading-for-custom").css("display", "block");
        },
        ajaxStop: function(){ 
            $("#loading-for-custom").css("display", "none");
        }    
    });

    let message = document.createElement("DIALOG");
    let errorText = document.createTextNode("Oops... There's no available street view close to that point. Choose one closer to a green spot! Must be at least 100 meters close!");

    map.on('click', function(e){
        message.remove();
        
        $.get(isThereACloseImage(e.lngLat.wrap().lng, e.lngLat.wrap().lat), function(data) {
            
            //Show error if no close image  
            if(data.features.length === 0) { 		
                message.setAttribute("open","open");
                message.appendChild(errorText);
                document.getElementById("dialog-container").appendChild(message);
            
            } else {
                let checkIfReported = window.location.origin + "/map/check_reported/" + data["features"][0]["properties"].key;
                $.get(checkIfReported, function(response) {
                    if(response == 'REPORTED') {
                        alert("Sorry, this image was reported, please use another one");
                    } else {
                        let colorOfMarker = getRandomColor(); //Generate a random color to identify each marker individually
                        mapillaryImages["keys"].push(data["features"][0]["properties"].key); // Add the key to a json object    
                        let marker = new mapboxgl.Marker({
                                        color:colorOfMarker
                                    })
                                    .setLngLat([e.lngLat.wrap().lng, e.lngLat.wrap().lat])
                                    .addTo(map);
                        markersCoords["markers"].push(marker); //Add marker to a marker json object
                        populateTable(i, colorOfMarker); //Add elements to table
                        i++;
                    }
                });
            }
        });
    });
});
