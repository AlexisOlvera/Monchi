function add_reviews(reviewText, triplets, index){
    console.log(triplets);
    document.getElementById('review' + index).innerHTML = highlightTriplets(reviewText, triplets);
    addPopover(triplets);
    addHoverEffect();

    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

function highlightTriplets(reviewText, triplets) {
    let highlightedReview = reviewText.split(' ');

    triplets.forEach(triplet => {
        const aspectPositions = triplet[0];
        const opinionPositions = triplet[1];
        const sentiment = triplet[2];

        aspectPositions.forEach(pos => {
            highlightedReview[pos] = `<span class="aspect" data-triplet="${triplets.indexOf(triplet)}">${highlightedReview[pos]}</span>`;
        });

        opinionPositions.forEach(pos => {
            highlightedReview[pos] = `<span class="opinion" data-triplet="${triplets.indexOf(triplet)}">${highlightedReview[pos]}</span>`;
        });
    });

    return highlightedReview.join(' ');
}

function addPopover(triplets) {
    const aspectsOpinions = document.querySelectorAll('.aspect, .opinion');
    aspectsOpinions.forEach(element => {
        const tripletIndex = element.dataset.triplet;
        if (tripletIndex === undefined || triplets[tripletIndex] === undefined) return;
        const sentiment = triplets[tripletIndex][2];

        element.setAttribute('data-bs-toggle', 'popover');
        element.setAttribute('data-bs-placement', 'top');
        element.setAttribute('title', `Sentimiento: ${sentiment}`);
    });
}

function addHoverEffect() {
    const aspectsOpinions = document.querySelectorAll('.aspect, .opinion');

    aspectsOpinions.forEach(element => {
        element.addEventListener('mouseover', () => {
            const tripletIndex = element.dataset.triplet;
            const aspects = document.querySelectorAll(`.aspect[data-triplet="${tripletIndex}"]`);
            const opinions = document.querySelectorAll(`.opinion[data-triplet="${tripletIndex}"]`);

            aspects.forEach(aspect => aspect.classList.add('highlight'));
            opinions.forEach(opinion => opinion.classList.add('highlight'));
        });

        element.addEventListener('mouseout', () => {
            const tripletIndex = element.dataset.triplet;
            const aspects = document.querySelectorAll(`.aspect[data-triplet="${tripletIndex}"]`);
            const opinions = document.querySelectorAll(`.opinion[data-triplet="${tripletIndex}"]`);

            aspects.forEach(aspect => aspect.classList.remove('highlight'));
            opinions.forEach(opinion => opinion.classList.remove('highlight'));
        });
    });
}

document.addEventListener('DOMContentLoaded', function () {
    console.log(reviews_triplets);
    const reviewsDiv = document.getElementById('reviewsDiv');
    reviews_triplets.forEach((review_triplet, index) => {
        // create a new div element with id = review + index
        reviewsDiv.appendChild(document.createElement('div')).setAttribute('id', 'review' + index);
        const reviewText = review_triplet.review;
        const triplets = review_triplet.triplets;
        add_reviews(reviewText, triplets, index);
    });
});

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