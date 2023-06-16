import json
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import googlemaps
from utilities import utilities
from models.ModelRestaurant import ModelRestaurant
from models.ModelRequest import ModelRequest
from models.ModelUser import ModelUser

app = Flask(__name__)
app.secret_key = 'QKy3NzXLu2k3l1XD'
#QKy3NzXLu2k3l1XD
# Replace the following values with your MongoDB Atlas connection string
MONGODB_CONNECTION_STRING = "mongodb+srv://monchi:QKy3NzXLu2k3l1XD@restaurants.svwsl9k.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client['monchi']

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/restaurants/<restaurant_name>')
def index(restaurant_name):
    print(restaurant_name)
    restaurant = ModelRestaurant.find(db, restaurant_name)
    print(restaurant)
    if restaurant != None:
        reviews_triplets = utilities.from_db_to_triplets_js(ModelRestaurant.get_reviews_from_db(db, restaurant.id_google, restaurant.id_yelp, restaurant.id_tripadvisor))
        print(reviews_triplets)
        labels, parents, values = utilities.data_to_list_ploty(restaurant.data)
        return render_template("restaurant.html", 
                            restaurant = restaurant,
                            labels = labels,
                            parents = parents,
                            values = values,
                            reviews_triplets = reviews_triplets
                        )
    else:
        return render_template("restaurant_not_found.html", restaurant_name = restaurant_name)
    
@app.route('/admin/restaurants', methods=['GET'])
def update_restaurants():
    if 'username' not in session:
        return redirect('/admin/login')
    restaurants = ModelRestaurant.find_all(db)
    return render_template("update_restaurants.html", restaurants = restaurants)

@app.route('/admin/new_restaurant', methods=['GET'])
def new_restaurant():
    if 'username' in session:
        return render_template("new_restaurant.html")
    else:
        return redirect('/')


@app.route('/admin/save_restaurant', methods=['POST'])
def save_restaurant():
    if 'username' not in session:
        return redirect('/admin/login')
    restaurant_name = request.form['name']
    id_google = request.form['id_google']
    try: 
        id_yelp = request.form['id_yelp']
        id_tripadvisor = request.form['id_tripadvisor']
    except:
        id_yelp = ''
        id_tripadvisor = ''
    ModelRestaurant.save(db, restaurant_name, id_google, id_yelp, id_tripadvisor)
    list_restaurants = db['restaurants'].distinct('name', {})
    with open('static/js/fuse_list.js', 'w+') as file:
        file.write(f"var restaurant_list = {json.dumps(list_restaurants)};")
    return redirect('/admin/new_restaurant')

@app.route('/admin/update_reviews/<_id>', methods=['GET'])
def update_reviews(_id):
    if 'username' not in session:
        return redirect('/admin/login')
    ModelRestaurant.update_reviews(db, _id)
    return redirect('/admin/restaurants')

@app.route('/admin/delete/<name_restaurant>', methods=['GET'])
def delete_restaurant(name_restaurant):
    if 'username' not in session:
        return redirect('/admin/login')
    print(name_restaurant)
    ModelRestaurant.delete(db, name_restaurant)
    return redirect('/admin/restaurants')

@app.route('/restaurants/request', methods=['POST', 'GET'])
def request_restaurants():
    restaurant_name = request.args.get('restaurant_name')
    print(restaurant_name)
    ModelRequest.new_request(db, restaurant_name)
    return redirect('/')

@app.route('/admin/requests', methods=['GET'])
def requests():
    if 'username' not in session:
        return redirect('/admin/login')
    requests = ModelRequest.find_requests(db)
    return render_template("requests.html", requests = requests)

@app.route('/admin/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if ModelUser.authenticate(db, username, password):
            session['username'] = username
            return redirect('/admin/restaurants')
        else:
            return render_template("login.html")
    return render_template("login.html")

@app.route('/admin/logout')
def logout():
  # Remove the username from the session
    if 'username' in session:
        session.pop('username', None)
    
    return redirect('/login')

@app.route('/admin/update_list_fuse', methods=['GET'])
def update_list_fuse():
    if 'username' not in session:
        return redirect('/admin/login')
    list_restaurants = db['restaurants'].distinct('name', {})
    with open('static/js/fuse_list.js', 'w+') as file:
        file.write(f"var restaurant_list = {json.dumps(list_restaurants)};")
    return jsonify({'status': 'ok'})

@app.route('/quienessomos')
def quienessomos():
    return render_template('quienessomos.html')

@app.route('/restaurants', methods=['GET'])
def list_restaurants():
    restaurants = ModelRestaurant.find_all(db)
    n_restaurants = len(restaurants)
    return render_template("restaurants.html", restaurants = restaurants, n_restaurants = n_restaurants)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):  
    return render_template('errors/500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)

