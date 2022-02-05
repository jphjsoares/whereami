mapboxgl.accessToken = 'pk.eyJ1IjoiY2FzZWlubWVsbCIsImEiOiJja3o4anZjOHMwdWQxMndxbTFoZGM3YzI1In0.B6eDbdCeO01bXCrDkDZIdw';
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
    //These 2 variables make a bbox
    let maxLng = lng+0.001;
    let maxLat = lat+0.001;
    let reqUrl =  "https://graph.mapillary.com/images?fields=id&bbox=" + lat.toFixed(3) + "," + lng.toFixed(3) + "," + maxLat.toFixed(3) + "," + maxLng.toFixed(3);
    console.log(reqUrl);
    return reqUrl;
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
        $.ajax({
            url: isThereACloseImage(e.lngLat.wrap().lng, e.lngLat.wrap().lat),
            type: "GET",
            headers: {"Authorization": "OAuth MLY|7677134818979003|9333a16aef0cf8d9a8e79fa6ecd7bac3"},
            contentType: "application/json",
            success: function(data) {
                console.log(data);
            }
        });
        /*
        $.get(isThereACloseImage(e.lngLat.wrap().lng, e.lngLat.wrap().lat), function(data) {
            console.log(data);
            
            //Show error if no close image  
            if(data.data.length === 0) { 		
                message.setAttribute("open","open");
                message.appendChild(errorText);
                document.getElementById("dialog-container").appendChild(message);
            
            } else {
                let checkIfReported = window.location.origin + "/map/check_reported/" + data["data"][0];
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
        */
    });
});
