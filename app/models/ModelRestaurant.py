from .entities.Restaurant import Restaurant
import requests
import googlemaps

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
        url = f"https://api.yelp.com/v3/businesses/{id_yelp}/reviews?locale=es_MX&limit=20&sort_by=newest"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer cqmtvw0bP7pf3ARZhZkD6QTXTIpwi8v2-dyil2BcbSzywQZEqOxEXzeiBDmhXYbJeJq7vBT8n-eNiKFq9yypOtcaG6MIjzPsZnkAvCXJyb0QVKM0rMRKOYHw9ipgY3Yx"
        }

        response = requests.get(url, headers=headers)
        #make an list of reviews just with the text
        reviews_yelp = [{'review': review['text'], 'id_review': review['id']} for review in response.json()['reviews']]
        
        api_key = 'AIzaSyBcDJUy0pFP_bRlNgfW9f49q6hr1G56rfQ'
        gmaps = googlemaps.Client(key=api_key)
        place = gmaps.place(id_google, language='es', reviews_no_translations=True, reviews_sort='most_newest')

        # Extract the review text for each review in the response
        reviews_google = []
        for review in place['result']['reviews']:
            reviews_google.append(review['text'])
        print(reviews_yelp)
        print(reviews_google)
        """ try:
            db['restaurants'].insert_one({'name': name, 'id_google': id_google, 'id_yelp': id_yelp})
        except Exception as ex:
            raise Exception(ex) """
        