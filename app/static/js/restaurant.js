//on load 
function initMap() {
    var request = {
        placeId: id_google,
        fields: ['photo', 'geometry']
    };
    service = new google.maps.places.PlacesService(document.createElement('div'));
    service.getDetails(request, callback);

    function callback(place, status) {
        if (status == google.maps.places.PlacesServiceStatus.OK) {
            let photos = place.photos;
            for (let i = 0; i < photos.length; i++) {
                let image = photos[i].getUrl();
                console.log(image);
                //<div class="carousel-item active">
                //<img src="https://img.gruporeforma.com/imagenes/960x640/5/930/4929843.jpg" class="d-block w-100" alt="...">
                //</div>
                document.getElementById('photos_google').innerHTML += 
                    `<div class="carousel-item ${ i==0 ?'active':''}">` +
                        `<img src="${image}" class="d-block w-100" alt="photo_${i}">` + 
                    '</div>';
            }

            let lat = place.geometry.location.lat();
            let lng = place.geometry.location.lng();
            document.getElementById('nav-map-tab').innerHTML =
                `<img src="https://maps.googleapis.com/maps/api/staticmap?center=${lat},${lng}&zoom=17&size=400x400&key=AIzaSyBcDJUy0pFP_bRlNgfW9f49q6hr1G56rfQ">`;
        }
    }

};


window.initMap = initMap;