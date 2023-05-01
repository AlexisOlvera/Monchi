// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">
let map;
let service;
let infowindow;

const id_google_field = document.getElementById('id_google');

function initMap() {
    //@19.4234126,-99.1440656,12z
    const cdmx = new google.maps.LatLng(19.4234126, -99.1440656);
    
  infowindow = new google.maps.InfoWindow();
  map = new google.maps.Map(document.getElementById("map"), {
    center: cdmx,
    zoom: 12,
  });
}

function findRestaurant() {
    const request = {
        query: document.getElementById('name_restaurant').value,
        bounds: map.getBounds(),
        type: ['restaurant']
    };

    service = new google.maps.places.PlacesService(map);
    service.textSearch(request, (results, status) => {
        if (status === google.maps.places.PlacesServiceStatus.OK && results) {
            for (let i = 0; i < results.length; i++) {
                createMarker(results[i]);
            }

            map.setCenter(results[0].geometry.location);
        }
    });
}

function createMarker(place) {
  if (!place.geometry || !place.geometry.location) return;

  const marker = new google.maps.Marker({
    map,
    position: place.geometry.location,
  });

  google.maps.event.addListener(marker, "click", () => {
    infowindow.setContent(place.name || "");
    infowindow.open(map);
    id_google_field.value = place.place_id;
  });
}


window.addEventListener('load', () => {
    document.getElementById('find_restaurant').addEventListener('click', findRestaurant);
});

window.initMap = initMap;