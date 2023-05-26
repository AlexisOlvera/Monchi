import datetime
from .entities.Restaurant import Restaurant
import requests
import googlemaps
from utilities import utilities

class ModelRestaurant():

    def get_reviews_from_google_yelp(self, id_google, id_yelp, just_new = False):
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer cqmtvw0bP7pf3ARZhZkD6QTXTIpwi8v2-dyil2BcbSzywQZEqOxEXzeiBDmhXYbJeJq7vBT8n-eNiKFq9yypOtcaG6MIjzPsZnkAvCXJyb0QVKM0rMRKOYHw9ipgY3Yx"
        }

        #More recent reviews from yelp
        url_yelp = f"https://api.yelp.com/v3/businesses/{id_yelp}/reviews?locale=es_MX&limit=20&sort_by=newest"
        response = requests.get(url_yelp, headers=headers)
        reviews_yelp = [{'review': review['text'], 'id_review': review['id']} for review in response.json()['reviews']]

        #More relevant reviews from yelp
        if just_new == False:
            url_yelp = f"https://api.yelp.com/v3/businesses/{id_yelp}/reviews?locale=es_MX&limit=20&sort_by=yelp_sort"
            response = requests.get(url_yelp, headers=headers)
            reviews_yelp.extend([{'review': review['text'], 'id_review': review['id']} for review in response.json()['reviews']])
        
        api_key = 'AIzaSyBcDJUy0pFP_bRlNgfW9f49q6hr1G56rfQ'
        gmaps = googlemaps.Client(key=api_key)

        #More recent reviews from google
        place = gmaps.place(id_google, language='es', reviews_no_translations=True, reviews_sort='newest')
        reviews_google = [{'review': review['text'], 'id_review': review['time']} for review in place['result']['reviews']]
        
        if just_new == False:
            #More relevant reviews from google
            place = gmaps.place(id_google, language='es', reviews_no_translations=True, reviews_sort='most_relevant')
            reviews_google.extend([{'review': review['text'], 'id_review': review['time']} for review in place['result']['reviews']])
        

        return reviews_yelp, reviews_google
    
    def get_triplets_from_colab(self, reviews_yelp, reviews_google, db, id_google, id_yelp):
        reviews_triplets = []
        for review in reviews_yelp:
            #Check if the review is in the database with the id_review and id_yelp
            if db['reviews_yelp'].find_one({'id_yelp': id_yelp, 'id_review': review['id_review']}) != None:
                continue
            triplets = utilities.get_triplets(review['review'])
            db['reviews_yelp'].insert_one({
                'id_yelp': id_yelp,
                'id_review': review['id_review'],
                'review': review['review'],
                'triplets': triplets
            })
            reviews_triplets.extend(triplets)
        
        for review in reviews_google:
            #Check if the review is in the database with the id_review and id_google
            if db['reviews_google'].find_one({'id_google': id_google, 'id_review': review['id_review']}) != None:
                continue
            triplets = utilities.get_triplets(review['review'])
            db['reviews_google'].insert_one({
                'id_google': id_google,
                'id_review': review['id_review'],
                'review': review['review'],
                'triplets': triplets
            })
            reviews_triplets.extend(triplets)
        
        return reviews_triplets

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
        #Obtener las reviews de google y yelp
        reviews_yelp, reviews_google = self.get_reviews_from_google_yelp(id_google, id_yelp)
        print(reviews_yelp)
        print(reviews_google)

        #mandarlas al colab que regrese los tripletes
        reviews_triplets = self.get_triplets_from_colab(reviews_yelp, reviews_google, db, id_google, id_yelp)

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
        
    @classmethod
    def new_request(self, db, restaurant_name):
        try:
            db['request'].insert_one({'name': restaurant_name, 'date': datetime.datetime.now()})
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def update_reviews(self, db, _id):
        try:
            if db['restaurants'].find_one({'_id': _id}) == None:
                return
            id_google = db['restaurants'].find_one({'_id': _id})['id_google']
            id_yelp = db['restaurants'].find_one({'_id': _id})['id_yelp']
            reviews_yelp, reviews_google = self.get_reviews_from_google_yelp(id_google, id_yelp, just_new=True)
            reviews_triplets = self.get_triplets_from_colab(reviews_yelp, reviews_google, db, id_google, id_yelp)
            #schema collection reviews_google: {'id_google': String, 'id_review': String, 'review': String, 'triplets': Array}
            #Just get the triplets arrays from db
            reviews_triplets.extend([triplet['triplets'] for triplet in db['reviews_yelp'].find({'id_yelp': id_yelp})])
            reviews_triplets.extend([triplet['triplets'] for triplet in db['reviews_google'].find({'id_google': id_google})])
            # Clusterizar los tripletes
            relevant_pairs = utilities.get_relevant_pairs(reviews_triplets)
            # Envíar al gpt-4
            generate_review = utilities.generate_review(relevant_pairs)
            db['restaurants'].update_one({'_id': _id}, 
                {"$set": {'review': generate_review}},
                {"$set": {'last_updated': datetime.datetime.now()}}, 
                {"$set": {'data': utilities.from_triplets_to_db(reviews_triplets)}}
            )
        except Exception as ex:
            raise Exception(ex)