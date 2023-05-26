document.getElementById('solicitar').addEventListener('click', () => {
    const restaurant_name = document.getElementById('name_restaurant').innerHTML;
    //send request to server not sync just send
    fetch(`/restaurants/request`, {
        method: 'POST',
        body: JSON.stringify({
            restaurant_name: restaurant_name
        })
    })
    .then(response => response.json())
    .then(result => {
        if(result.error) {
            alert(result.error);
        } else {
            alert(result.message);
        }
    })
    .catch(error => {
        console.log(error);
    });


    window.location.href = `/`;
});