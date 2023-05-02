import json
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
import googlemaps
from models.ModelRestaurant import ModelRestaurant

app = Flask(__name__)
#QKy3NzXLu2k3l1XD
# Replace the following values with your MongoDB Atlas connection string
MONGODB_CONNECTION_STRING = "mongodb+srv://monchi:QKy3NzXLu2k3l1XD@restaurants.svwsl9k.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client['monchi']
@app.route('/restaurants/<restaurant_name>')
def index(restaurant_name):
    print(restaurant_name)
    restaurant = ModelRestaurant.find(db, restaurant_name)
    print(restaurant)
    if restaurant != None:
        return render_template("restaurant.html", restaurant = restaurant)
    else:
        return render_template("index.html") # restaurant_not_found.hmtl"
    

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

if __name__ == "__main__":
    app.run(debug=True)
