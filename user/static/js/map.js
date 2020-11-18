mapboxgl.accessToken = 'pk.eyJ1IjoicmFtejg1OCIsImEiOiJjazl1N3ZxYnUxa2dlM2dtb3ozemhtZWJ2In0.c7Pc5LCE0rvGoJ6hZYEftg';
var values=[];

var userData = eval($("#sections").text());
var featureBounds = $("#bounds").text();

if(featureBounds) {
    featureBounds = featureBounds.trim().split(',');
    featureBounds = featureBounds.map(coordinate => parseFloat(coordinate));
}

console.log(featureBounds);
var bounds = [
    [-117.368317,32.650938], // Southwest coordinates
    [-117.020874,32.938386] // Northeast coordinates
];

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/ramz858/ckbx684hi1m4m1inxh6sdnxwv', 
    center: [-117.191,32.794], // starting position [lng, lat]
    maxBounds: bounds, // Sets bounds as max
    zoom: 10, // starting zoom
    minZoom:10,
    maxZoom:16.9,
    maxPitch:0
});

//  ============= Map control and UI customization =======================     

// Hide rotation control.
map.addControl(new mapboxgl.NavigationControl({
    showCompass: false
}), 'bottom-right');

// / Add geolocate control to the map.
map.addControl(
    new mapboxgl.GeolocateControl({
        positionOptions: {
        enableHighAccuracy: true
        },
        trackUserLocation: true
    })
);

// logo control
class LogoControl {
    onAdd(map) {
        this._map = map;
        this._container = document.createElement('div');
        this._container.className = 'mapboxgl-ctrl logoContainer';
        this._container.innerHTML = '<img src="/logo.png" width="85">';
        return this._container;
    }

    onRemove() {
        this._container.parentNode.removeChild(this._container);
        this._map = undefined;
    }
}

var logoControl = new LogoControl();
map.addControl(logoControl, 'bottom-left');

// geocoder control
var geocoderControl = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken,
    mapboxgl: mapboxgl,
    collapsed: true
});

map.addControl(geocoderControl, 'top-left');

// disable map rotation using right click + drag
map.dragRotate.disable();
map.dragRotate.pitchWithRotate = false;


// disable map rotation using touch rotation gesture WORKS rotate
map.touchZoomRotate.disableRotation();

// Scratch layer
var selectedRoads = {
    "type": "FeatureCollection",
    "features": []
};

// load map layer
map.on('load', function(e) {
    // Route source and layer
    map.addSource('route', {
        type: 'vector',
        //old with no dl time
        url: 'mapbox://ramz858.ckbrddrjh00u222o5ufdwlt2r-6mw1r',
        //url: 'mapbox://ramz858.1ssa1o1c',
        buffer: 500     
    });

    map.addLayer(
        {
            'id': 'route',
            'type': 'line',
            'source': 'route',
            //old no dl time
            'source-layer': 'csvnew',
            //'source-layer': 'CMB_NOTSIMPLE_2-coho6z',
            'layout': {
                'line-join': 'round',
                'line-cap': 'round'
                
            },
            'paint': {
                'line-color': '#888',
                'line-width': 45,
                'line-opacity': 0  
            }
    });


    // Selected roads source and layer
    map.addSource('selectedRoad', {
        "type": "geojson",
        "data": selectedRoads
    });

    map.addLayer({
        "id": "selectedRoad",
        "type": "line",
        "source": "selectedRoad",
        "layout": {
            "line-join": "round",
            "line-cap": "round"
        },
        "paint": {
            "line-color": "yellow",
            "line-width":8,
            "line-opacity": .8
            
        }
    });

    map.addLayer({
        "id": "tip2-copy-4",
        "type": "symbol",
        "source": "selectedRoad",
        "layout": {
            "symbol-placement": "line-center",
            "text-font": ["Roboto Bold Italic", "Arial Unicode MS Regular"],
            "text-size": 10,
            "text-allow-overlap": true,
            "text-anchor": "bottom",
            "text-keep-upright": false,
            "text-field": ["get", "DL2 TIME"],
            "text-radial-offset": 2.9
        },
        "paint": {
            "text-halo-color": "hsl(0, 3%, 100%)",
            "text-halo-width": 1,
            "text-color": "black"
        }
    });

    map.addLayer({
        "id": "tip2-copy-3",
        "type": "symbol",
        "source": "selectedRoad",
        "layout": {
            "symbol-placement": "line-center",
            "text-font": ["Roboto Bold Italic", "Arial Unicode MS Regular"],
            "text-size": 10,
            "text-allow-overlap": true,
            "text-anchor": "top",
            "text-keep-upright": false,
            "text-field": ["get", "DL1 TIME"],
            "text-radial-offset": 2.9
        },
        "paint": {
            "text-halo-color": "hsl(0, 3%, 100%)",
            "text-halo-width": 1,
            "text-color": "black"
        }
    });

    // fit map to selected features bounds
    if(featureBounds.length == 4) {
        // map.fitBounds(featureBounds,);

        // filterFields = userData.map(field => field.split('_')[1]);
        // filterData();
    }

    // Change the cursor to a pointer when the mouse is over the states layer.
     map.on('mouseenter', 'route', function () {
        map.getCanvas().style.cursor = 'pointer';
    });

    // Change it back to a pointer when it leaves.
     map.on('mouseleave', 'route', function () {
        map.getCanvas().style.cursor = '';
    });

    map.on('click', 'route', function(e) {

        var features = map.queryRenderedFeatures(e.point, { layers: ['route'] });

        console.log(features);
        if (!features.length) {
            return;
        }

        var feature = features[0];
        if(isFeatureSelected(feature, selectedRoads)) {
            selectedRoads = filterSelectedRoads(feature);

            updateSelectedRoad(selectedRoads);

            // remove the  deselected form group
            var id = feature.properties.OID;
            $('#' + id).remove();
        }
        else if(selectedRoads.features.length >= 4) {
            alert("Cannot add any more streets");
            return ;

        } else {
            selectedRoads.features.push(feature);

            updateSelectedRoad(selectedRoads);

            var coordinates = e.features[0].geometry.coordinates.slice();
            var att = e.features[0].properties;

            // append values to form input
            var index = selectedRoads.features.length;
            appendFormInput(att, index);

            // Scroll to the form
            if(selectedRoads.features.length == 4) {
                var element = document.getElementById("formdiv");
                var deviceWidth = document.documentElement.clientWidth;

                if(deviceWidth < 768) {
                    element.scrollIntoView(true);
                }
                
            }
        }
    });

     // hide the spinner
     $('.spinner-container').toggleClass("d-none");
});

// filter the sourcdata
function filterSources(e){
    // console.log(e);
    if (e.sourceId == 'route' && e.isSourceLoaded && !e.hasOwnProperty('sourceDataType')){
        
        // filter the data 
        if(typeof userData  == 'object' && selectedRoads.features.length < 4){
            // update the map view to the first feature
            filterFields = userData.map(field => field.split('_')[1]);
            filterData();
            
        } 
    }
}

function filterData(){
    // filter the data with specific oid
    filterFields = userData.map(field => field.split('_')[1]);

    console.log(filterFields);
    if(selectedRoads.features[0] && filterFields[0]) {
        selectedRoads.features = [];
    }

    // filter the data
    filterFields.forEach(oid => {
        // let feature = data.features.find(feature => feature.properties.OID == OID);
        var feature = map.querySourceFeatures('route',{
            //old no dl time
            sourceLayer:'csvnew',
            //sourceLayer:'CMB_NOTSIMPLE_2-coho6z',
            
            filter:["==","OID", parseInt(oid)]
        });

        if(feature[0]){
            if(selectedRoads.features.length <= 4) {
                console.log(feature[0]);
                // update selected roads object
                selectedRoads.features.push(feature[0]);

                // update the form input
                appendFormInput(feature[0].properties, 2);
            }
            
        }
    });

    console.log(selectedRoads);
    // updated selected Roads source
    updateSelectedRoad(selectedRoads);
    fitToDataBounds();
}

// fit to mapbounds
function fitToDataBounds() {
    var bbox = turf.bbox(selectedRoads);
    map.fitBounds(bbox,{
        padding:50
    });
}

map.on('sourcedata', filterSources);

// check if selected 
function isFeatureSelected (feature, selectedRoads) {
    var featureClicked = selectedRoads.features.find(route => {
       if (route.properties.OID == feature.properties.OID) {
           return route;
       }
   });

   return Boolean(featureClicked);
}

// add form input to the map
function appendFormInput(att, index) {
    // get the id
    var id = att.OID;

    // add a form input element
    var data = "<div class='input-group input-group-sm my-1' id='" + id + "'><div class='input-group-append' for='res_name'><span class='input-group-text' id='basic-addon1'>Street"+
    "</span></div>" +
    "<input type='text' class='form-control' name='res_name_"+ id+"' id='display_label_"+id+"' value='" + att.SL +
    "' placeholder='Name' readonly> <div class='input-group-append'><span class='"+ id +" text-center input-group-text' role='button' data-target='" + id + "'>X</span></div></div>";


    $("#street-form").append(data);
    
    let closeBtn = $('.'+id);
    addlistener(closeBtn);
}

// filter the selectedRoad from 
function filterSelectedRoads (feature) {
    selectedRoads.features = selectedRoads.features.filter(route => {
        if (route.properties.OID != feature.properties.OID) {
            return route;
        }
    });

    return selectedRoads;
}

// update the selectedRoad source layer
function updateSelectedRoad (selectedRoads) {
    map.getSource('selectedRoad').setData(selectedRoads);
}

// add eventlistener to form deselect buttons
function addlistener (element){
    element.on('click', function (e) {
        var id = $(this).attr('data-target');
        console.log(id);

        $('#' + id).remove();

        // update the map data 
        selectedRoads.features = selectedRoads.features.filter(route => {
            if(route.properties.OID != parseInt(id)){
                return route;
            }
        });

        updateSelectedRoad(selectedRoads);
    });
}


// form submit event
$('#form').on('submit', function(e) {
    e.preventDefault();

    if(selectedRoads.features.length == 0) {
        alert("Please click on at least one road section, you can change your roads anytime");
        return;
    }

    // fit map to selected features bounds
    fitToDataBounds();

    // get the bounds object
    let bbox = turf.bbox(selectedRoads);
 
     var data = $(this).serializeArray();
 
     // add oid to the data
     let length = data.length;
     var [csrf, ...sections] = data;

     console.log(sections);

     var sectionsData = sections.map(datum => {
         if(datum.name.includes('res_name')) {
             return datum;   
         }
     }).filter(dt => dt);

          
     sections = sections.slice(sectionsData.length, sections.length + 1);
 
     sectionsData.forEach((section,i) => {
         section.value = section.value+'_'+section.name.split('_')[2];
         return section;
     });
     
     let formData = [csrf, ...sectionsData, ...sections];

     bbox = bbox.map(coordinate => parseFloat(coordinate.toFixed(5)));

     console.log(bbox);
     formData.push({"name":"bounds", 'value':bbox.toString()});

     console.log(formData);
     saveData(formData);
 });

// Save the value to a csv file
function saveData (data) {
    $('.spinner-message').text("Saving data ...");
    $('.spinner-container').toggleClass("d-none");
    
    console.log(data);

    // send the data to the backend
    $.ajax({    
        url:window.location.pathname,
        data:data,
        type:'POST',
        success:function(response) {
            console.log(response);
            var res = response;
            console.log(res);

            if(res.message == 'success'){
                setTimeout(function(e){
                    window.location.assign(res.navigate_to)
                }, 1000);
                
            }else {
                // add errors to the form
                var errors = res.errors;
                var keys = Object.keys(res.errors);

                keys.forEach(key =>{
                    $('input[name='+key+']').parent().before("<small class='text-danger text-small error'>"+errors[key]+"</small>");
                });

                setTimeout(function(e){
                    $('.spinner-container').toggleClass("d-none");
                },1000)
                

            }
        },
        error:function(error){
            console.log(error);
            $('.spinner-container').toggleClass("d-none");
        }
    });
}

// add a pattent to input type phone_number
var phoneNumber = document.getElementById('id_phone_number');
if(phoneNumber) {
    // phoneNumber.setAttribute('pattern', "[0-9]{10}");
}

// disable doubleClickZoom
var hasTouchScreen = false;

if ("maxTouchPoints" in navigator) { 
    hasTouchScreen = navigator.maxTouchPoints > 0;
} else if ("msMaxTouchPoints" in navigator) {
    hasTouchScreen = navigator.msMaxTouchPoints > 0; 
} else {
    var mQ = window.matchMedia && matchMedia("(pointer:coarse)");

    if (mQ && mQ.media === "(pointer:coarse)") {
        hasTouchScreen = !!mQ.matches;
    } else if ('orientation' in window) {
        hasTouchScreen = true; // deprecated, but good fallback
    } else {
        // Only as a last resort, fall back to user agent sniffing
        var UA = navigator.userAgent;
        hasTouchScreen = (
            /\b(BlackBerry|webOS|iPhone|IEMobile)\b/i.test(UA) ||
            /\b(Android|Windows Phone|iPad|iPod)\b/i.test(UA)
        );
    }
}

if (hasTouchScreen) {
    map.doubleClickZoom.disable();
}