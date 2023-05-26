import json
from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
import googlemaps
from utilities import utilities
from models.ModelRestaurant import ModelRestaurant
from models.ModelRequest import ModelRequest

app = Flask(__name__)
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
        labels, parents, values = utilities.data_to_list_ploty(restaurant.data)
        return render_template("restaurant.html", restaurant = restaurant, labels = labels, parents = parents, values = values)
    else:
        return render_template("restaurant_not_found.html", restaurant_name = restaurant_name) # "
    

@app.route('/get_review/<place_id>')
def get_review(place_id):
    api_key = 'AIzaSyBcDJUy0pFP_bRlNgfW9f49q6hr1G56rfQ'
    gmaps = googlemaps.Client(key=api_key)
    place = gmaps.place(place_id, language='es', reviews_no_translations=True, reviews_sort='most_newest')

    # Extract the review text for each review in the response
    reviews = []
    for review in place['result']['reviews']:
        reviews.append(review['text'])

    # Return the review text as a JSON response
    return jsonify({'reviews': reviews})


@app.route('/admin/restaurants', methods=['GET'])
def update_restaurants():
    restaurants = ModelRestaurant.find_all(db)
    return render_template("update_restaurants.html", restaurants = restaurants)

@app.route('/admin/new_restaurant', methods=['GET'])
def new_restaurant():
    return render_template("new_restaurant.html")


@app.route('/admin/save_restaurant', methods=['POST'])
def save_restaurant():
    restaurant_name = request.form['name']
    id_google = request.form['id_google']
    id_yelp = request.form['id_yelp']
    ModelRestaurant.save(db, restaurant_name, id_google, id_yelp)
    return render_template("new_restaurant.html")

@app.route('/admin/update_list_fuse', methods=['GET'])
def update_list_fuse():
    list_restaurants = db['restaurants'].distinct('name', {})
    with open('static/js/fuse_list.js', 'w+') as file:
        file.write(f"var restaurant_list = {json.dumps(list_restaurants)};")
    return jsonify({'status': 'ok'})
    
@app.route('/admin/update_reviews/<_id>', methods=['GET'])
def update_reviews(_id):
    return {'status': 'ok'}

@app.route('/restaurants/request', methods=['POST', 'GET'])
def request_restaurants():
    restaurant_name = request.args.get('restaurant_name')
    print(restaurant_name)
    ModelRequest.new_request(db, restaurant_name)
    return redirect('/')

@app.route('/admin/requests', methods=['GET'])
def requests():
    requests = ModelRequest.find_requests(db)
    return render_template("requests.html", requests = requests)


if __name__ == "__main__":
    app.run(debug=True)
