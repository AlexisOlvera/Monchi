
let reviewText = "RESTAURANTE nos encanto el lugar . la reservacion originalmente era para 10 y cuando pedimos que nos cambiaran a una mesa mas grande porque seriamos 13 , nos ofrecieron hacerlo sin mostrar molestia . el risotto con filete delicioso y el coctel de mezcal con pepino y chile riquisimo . muy buena experiencia la musica aunque un poco alta , muy buena RESTAURANTE";
let triplets = [
    [[4], [1, 2], 'POS'],
    [[35, 36, 37], [38], 'POS'],
    [[41, 42, 43, 44, 45], [48], 'POS'],
    [[52], [51], 'POS'],
    [[54], [58], 'POS'],
    [[54], [61], 'POS']
];
const visualizar = document.getElementById('vizualizar');
const resena = document.getElementById('resena');

function convertToListOfLists(str) {
    let tuples = str.replaceAll(/\(/g, "[").replaceAll(/\)/g, "]").replaceAll("'", "\"");
    console.log(tuples);
    return JSON.parse(tuples);
}
  

visualizar.addEventListener('click', () =>{
    const separados = resena.value.split("#### #### ####");
    console.log(separados);
    reviewText = separados[0];
    triplets = convertToListOfLists(separados[1]);
    console.log(triplets);
    document.getElementById('review').innerHTML = highlightTriplets();
    addPopover();
    addHoverEffect();

    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

});

function highlightTriplets() {
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

function addPopover() {
    const aspectsOpinions = document.querySelectorAll('.aspect, .opinion');

    aspectsOpinions.forEach(element => {
        const tripletIndex = element.dataset.triplet;
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
