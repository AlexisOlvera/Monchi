import json
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
import googlemaps
from models.ModelRestaurant import ModelRestaurant

app = Flask(__name__)

# Replace the following values with your MongoDB Atlas connection string
MONGODB_CONNECTION_STRING = "mongodb://root:root123@localhost:27017/?authSource=admin&readPreference=primary&ssl=false&directConnection=true"
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


if __name__ == "__main__":
    app.run(debug=True)
