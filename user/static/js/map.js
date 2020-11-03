mapboxgl.accessToken = 'pk.eyJ1IjoicmFtejg1OCIsImEiOiJjazl1N3ZxYnUxa2dlM2dtb3ozemhtZWJ2In0.c7Pc5LCE0rvGoJ6hZYEftg';
var values=[];
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

// Map control and UI customization, 

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

// disable map rotation using right click + drag
map.dragRotate.disable();
map.dragRotate.pitchWithRotate = false;


// disable map rotation using touch rotation gesture WORKS rotate
map.touchZoomRotate.disableRotation();


//  