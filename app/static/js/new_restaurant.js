// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">
let map;
let service;
let infowindow;

const id_google_field = document.getElementById('id_google');
const name_restaurant_field = document.getElementById('name');
const id_yelp_field = document.getElementById('id_yelp');
const name_to_find = document.getElementById('name_restaurant');

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
        query: name_to_find.value,
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


function findInYelp(name, lattitude, longitude){
    const corsAnywhereUrl = 'https://cors-anywhere.herokuapp.com/';
    console.log(name, lattitude, longitude);
    const options = {
        method: 'GET',
        headers: {
          accept: 'application/json',
          Authorization: 'Bearer cqmtvw0bP7pf3ARZhZkD6QTXTIpwi8v2-dyil2BcbSzywQZEqOxEXzeiBDmhXYbJeJq7vBT8n-eNiKFq9yypOtcaG6MIjzPsZnkAvCXJyb0QVKM0rMRKOYHw9ipgY3Yx'
        }
      };
      //return the id of the restaurant or null 
      fetch(corsAnywhereUrl + `https://api.yelp.com/v3/businesses/search?location=CDMX&latitude=${lattitude}&longitude=${longitude}&term=${name}&radius=30&categories=restaurants&sort_by=best_match&limit=20`, options)
        .then(response => response.json())
        .then(response => {
            console.log(response);
            if (response.businesses.length > 0){
                id_yelp_field.value = response.businesses[0].id;
            }
        })
        .catch(err => console.error(err));
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
    name_restaurant_field.value = place.name;
    findInYelp(name_to_find.value , place.geometry.location.lat(), place.geometry.location.lng());
  });
}


window.addEventListener('load', () => {
    document.getElementById('find_restaurant').addEventListener('click', findRestaurant);
});

window.initMap = initMap;