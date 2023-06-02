var num_positivos = 0;
var num_negativos = 0;


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

function setMultipleAttributesonElement(elem, elemAttributes) {
    Object.keys(elemAttributes).forEach(attribute => {
        elem.setAttribute(attribute, elemAttributes[attribute]);
    });
    
}

document.addEventListener('DOMContentLoaded', function () {
    const num_reviews = document.getElementById('num_reviews');
    num_reviews.innerHTML = reviews_triplets.length;
    console.log('DOM loaded');
    initBubblePlot();
    initIndicatorPlot();
    console.log(reviews_triplets);
    const reviewsDiv = document.getElementById('reviewsDiv');
    const reviewsList = document.getElementById('reviews-list-tab');
    reviews_triplets.forEach((review_triplet, index) => {
        // create a new div element with id = review + index
        // <div class="tab-pane fade show active" id="reviewN" role="tabpanel" aria-labelledby="list-home-list">...</div>
        //<div class="list-group" id="reviews-list-tab" role="tablist">
        //<a class="list-group-item list-group-item-action active" id="list-reviewN-list" data-bs-toggle="list" href="#reviewN" role="tab" aria-controls="list-reviewN">Review n</a>
        const element_a_Attributes = {
            'class': 'list-group-item list-group-item-action ' + (index==0 ? 'active':''),
            'id': 'list-review' + index + '-list',
            'data-bs-toggle': 'list',
            'href': '#review' + index,
            'role': 'tab',
            'aria-controls': 'list-review' + index
        };

        const element_div_Attributes = {
            'class': 'tab-pane fade show '+ (index==0 ? 'active':''),
            'id': 'review' + index,
            'role': 'tabpanel',
            'aria-labelledby': 'list-review' + index + '-list'
        };

        const element_a = document.createElement('a');
        setMultipleAttributesonElement(element_a, element_a_Attributes);
        element_a.innerHTML = 'Review ' + (index + 1);

        const element_div = document.createElement('div');
        setMultipleAttributesonElement(element_div, element_div_Attributes);

        reviewsList.appendChild(element_a);
        reviewsDiv.appendChild(element_div);
        
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

function initBubblePlot(){
    size_aspects = size_aspects.map(x => x * 10);
    let trace_aspects = {
        x: x_aspects,
        y: y_aspects,
        mode: 'markers',
        marker: {
            color: 'rgb(240, 62, 2)',
            size: size_aspects
        },
        text: text_aspects
    };
    size_opinions = size_opinions.map(x => x * 10);
    let trace_opinions = {
        x: x_opinions,
        y: y_opinions,
        mode: 'markers',
        marker: {
            size: size_opinions,
            color: 'rgb(24, 28, 245)'
        },
        text: text_opinions
    };


    let data = [trace_aspects, trace_opinions];

    let layout = {
        title: 'Aspectos y opiniones',
        showlegend: false,
        height: 600,
        width: 600
    };

    Plotly.newPlot('bubblePlot', data, layout);
}

function count_triplets_pos_neg(){
    num_positivos = 0;
    num_negativos = 0;
    reviews_triplets.forEach(review_triplet => {
        review_triplet.triplets.forEach(triplet => {
            if(triplet[2] == 'POS'){
                num_positivos++;
            }else{
                num_negativos++;
            }
        });
    });
    console.log(num_positivos);
    console.log(num_negativos);
}

function initIndicatorPlot(){
    count_triplets_pos_neg();
    let data = [
        {
          type: "indicator",
          domain: { x: [0, 1], y: [0, 1] },
          title: 'Positivos vs Negativos',
          value: num_positivos,
          mode: "gauge+number+delta",
          delta: { reference: num_positivos+num_negativos},
          gauge: { axis: { visible: true, range: [0, num_positivos+num_negativos] } },
          domain: { row: 0, column: 0 }
        },
    ];

    let layout = {
        showlegend: false,
        height: 600,
        width: 600
    };

    Plotly.newPlot('indicatorPlot', data, layout);
}