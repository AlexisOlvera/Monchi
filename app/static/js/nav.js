
function find_restaurant_redirect() {
    const restaurant_name = document.getElementById('find_field').value;
    if(restaurant_name == '') return;
    window.location.href = `/restaurants/${restaurant_name}`;
}


window.addEventListener('load', () => {
    document.getElementById('buscar').addEventListener('click', find_restaurant_redirect);
});