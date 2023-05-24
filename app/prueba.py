from pymongo import MongoClient
from models.entities.Restaurant import Restaurant
import json
import requests
import googlemaps
import sys
from get_triplets import get_relevant_triplets
 
# adding Folder_2 to the system path
sys.path.insert(1, '/home/aolvera/Documentos/TT/monchi/monchi/clusterizacion')
import get_triplets


MONGODB_CONNECTION_STRING = "mongodb+srv://monchi:QKy3NzXLu2k3l1XD@restaurants.svwsl9k.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client['monchi']


def get_triplets(review : str):
    url_ngrok = "http://7121-35-187-246-236.ngrok-free.app"
    url_colab = url_ngrok+f"/api/predict?review='{review}'"
    response = requests.get(url_colab)
    return response.json()

id_google = 'ChIJez8vvy__0YURP0rx5WhEig4'
id_yelp = 'm5fGRczOFYKpw-nOXsSPDA'




headers = {
    "accept": "application/json",
    "Authorization": "Bearer cqmtvw0bP7pf3ARZhZkD6QTXTIpwi8v2-dyil2BcbSzywQZEqOxEXzeiBDmhXYbJeJq7vBT8n-eNiKFq9yypOtcaG6MIjzPsZnkAvCXJyb0QVKM0rMRKOYHw9ipgY3Yx"
}
#More relevant reviews from yelp
url_yelp = f"https://api.yelp.com/v3/businesses/{id_yelp}/reviews?locale=es_MX&limit=20&sort_by=yelp_sort"
response = requests.get(url_yelp, headers=headers)
reviews_yelp = [{'review': review['text'], 'id_review': review['id']} for review in response.json()['reviews']]
#More recent reviews from yelp
url_yelp = f"https://api.yelp.com/v3/businesses/{id_yelp}/reviews?locale=es_MX&limit=20&sort_by=newest"
response = requests.get(url_yelp, headers=headers)
reviews_yelp.extend([{'review': review['text'], 'id_review': review['id']} for review in response.json()['reviews']])
api_key = 'AIzaSyBcDJUy0pFP_bRlNgfW9f49q6hr1G56rfQ'
gmaps = googlemaps.Client(key=api_key)

#More relevant reviews from google
place = gmaps.place(id_google, language='es', reviews_no_translations=True, reviews_sort='most_relevant')
reviews_google = [{'review': review['text'], 'id_review': review['time']} for review in place['result']['reviews']]
#More recent reviews from google
place = gmaps.place(id_google, language='es', reviews_no_translations=True, reviews_sort='most_newest')
reviews_google.extend([{'review': review['text'], 'id_review': review['time']} for review in place['result']['reviews']])
print(reviews_yelp)
print(reviews_google)
"""
Scheme of database of reviews
{id_google: "", 
reviews:[{id_review: "", triplets: [{aspect: "", sentiment: "", opinion: ""}], review: ""}]}
"""

phrase_pairs = []

for review in reviews_google:
    # Check if review is already in database
    triplets = get_triplets(review['review'])
    print('-'*30)
    print(review['review'])
    print(triplets)
    print('Review added to database')
    for triplet in triplets:
        phrase_pairs.append((triplet['aspect'], triplet['opinion']))


for review in reviews_yelp:
    # Check if review is already in database
    triplets = get_triplets(review['review'])
    print('-'*30)
    print(review['review'])
    print(triplets)
    print('Review added to database')
    for triplet in triplets:
        phrase_pairs.append((triplet['aspect'], triplet['opinion']))



with open('phrase_pairs.json', 'w') as file:
    json.dump(phrase_pairs, file)

relevant_aspects = get_relevant_triplets(phrase_pairs)

print(relevant_aspects)