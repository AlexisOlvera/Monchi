
function find_restaurant_redirect() {
    const restaurant_name = document.getElementById('find_field').value;
    if(restaurant_name == '') return;
    window.location.href = `/restaurants/${restaurant_name}`;
}


window.addEventListener('load', () => {
    document.getElementById('buscar').addEventListener('click', find_restaurant_redirect);
    const options = {
        includeScore: false
      };
      
      const fuse = new Fuse(restaurant_list, options);
      const searchInput = document.getElementById('find_field');
      const resultList = document.getElementById('result_list');
      
      searchInput.addEventListener('keyup', (event) => {
        const query = event.target.value;
        const result = fuse.search(query);
        let html = '';
      
        for (let i = 0; i < Math.min(result.length, 5); i++) {
          html += `<a class="dropdown-item" href="/restaurants/${result[i].item}">${result[i].item}</a>`;
        }
      
        resultList.innerHTML = html;
        resultList.classList.toggle('show', query.length > 0);
      });
      
      resultList.addEventListener('click', (event) => {
        if (event.target.tagName === 'A') {
          event.preventDefault();
          searchInput.value = event.target.textContent;
        }
      });
      
      document.addEventListener('click', (event) => {
        if (!event.target.matches('#find_field')) {
          resultList.classList.remove('show');
        }
      });      
});