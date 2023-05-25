import datetime
from .entities.Restaurant import Restaurant
import requests
import googlemaps
from utilities import utilities

class ModelRestaurant():
    @classmethod
    def find(self, db, restaurant_name):
        try:
            result = db['restaurants'].find_one({'name': {"$regex": restaurant_name, "$options": "i"}})
            print(result)
            if result != None:
                return Restaurant(**result)
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def find_all(self, db):
        try:
            result = db['restaurants'].find()
            restaurants = []
            for restaurant in result:
                restaurants.append(Restaurant(**restaurant))
            return restaurants
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def save(self, db, name, id_google, id_yelp):
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


        #mandarlas al colab que regrese los tripletes
        reviews_triplets = []
        for review in reviews_yelp:
            triplets = utilities.get_triplets(review['review'])
            db['reviews_yelp'].insert_one({
                'id_yelp': id_yelp,
                'id_review': review['id_review'],
                'review': review['review'],
                'triplets': triplets
            })
            reviews_triplets.extend(triplets)
        
        for review in reviews_google:
            triplets = utilities.get_triplets(review['review'])
            db['reviews_google'].insert_one({
                'id_google': id_google,
                'id_review': review['id_review'],
                'review': review['review'],
                'triplets': triplets
            })
            reviews_triplets.extend(triplets)

        print(reviews_triplets)
        # Clusterizar los tripletes
        relevant_pairs = utilities.get_relevant_pairs(reviews_triplets)
        print(relevant_pairs)
        # Envíar al gpt-4
        generate_review = utilities.generate_review(relevant_pairs)
        print(generate_review)
        try:
            db['restaurants'].insert_one({
                'name': name, 
                'review': generate_review, 
                'data': utilities.from_triplets_to_db(reviews_triplets),
                'id_google': id_google, 
                'id_yelp': id_yelp, 
                'last_updated': datetime.datetime.now()
            })
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def delete(self, db, restaurant_name):
        try:
            db['restaurants'].delete_one({'name': {"$regex": restaurant_name, "$options": "i"}})
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def update(self, db, restaurant_name, new_name):
        try:
            db['restaurants'].update_one({'name': {"$regex": restaurant_name, "$options": "i"}}, {"$set": {'name': new_name}})
        except Exception as ex:
            raise Exception(ex)