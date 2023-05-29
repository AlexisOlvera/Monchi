import datetime
from .entities.Restaurant import Restaurant
import requests
import googlemaps
from utilities import utilities

class ModelRestaurant():

    def get_reviews(self, id_google, id_yelp, id_tripadvisor, just_new = False):
        reviews = dict(
            yelp = [],
            google = [],
            tripadvisor = [],
        )
        if id_yelp != '':    
            headers = {
                "accept": "application/json",
                "Authorization": "Bearer cqmtvw0bP7pf3ARZhZkD6QTXTIpwi8v2-dyil2BcbSzywQZEqOxEXzeiBDmhXYbJeJq7vBT8n-eNiKFq9yypOtcaG6MIjzPsZnkAvCXJyb0QVKM0rMRKOYHw9ipgY3Yx"
            }

            #More recent reviews from yelp
            url_yelp = f"https://api.yelp.com/v3/businesses/{id_yelp}/reviews?locale=es_MX&limit=20&sort_by=newest"
            response = requests.get(url_yelp, headers=headers)
            for review in response.json()['reviews']:
                if review['text'] == '':
                    continue
                reviews['yelp'].append({'review': review['text'], 'id_review': review['id']})


            #More relevant reviews from yelp
            if just_new == False:
                url_yelp = f"https://api.yelp.com/v3/businesses/{id_yelp}/reviews?locale=es_MX&limit=20&sort_by=yelp_sort"
                response = requests.get(url_yelp, headers=headers)
                for review in response.json()['reviews']:
                    if review['text'] == '':
                        continue
                    reviews['yelp'].append({'review': review['text'], 'id_review': review['id']})
        
        if id_tripadvisor != '':
            #More recent reviews from tripadvisor
            url = f"https://api.content.tripadvisor.com/api/v1/location/{id_tripadvisor}/reviews?key=7A043312545D413990FDE799105F27BC&language=es_MX"

            headers = {"accept": "application/json"}

            response = requests.get(url, headers=headers)
            for review in response.json()['data']:
                if review['text'] == '':
                    continue
                print(review['text'])
                reviews['tripadvisor'].append({'review': review['text'], 'id_review': review['id']})

        api_key = 'AIzaSyBcDJUy0pFP_bRlNgfW9f49q6hr1G56rfQ'
        gmaps = googlemaps.Client(key=api_key)

        #More recent reviews from google
        place = gmaps.place(id_google, language='es', reviews_no_translations=True, reviews_sort='newest')
        for review in place['result']['reviews']:
            if review['text'] == '':
                continue
            reviews['google'].append({'review': review['text'], 'id_review': review['time']})


        if just_new == False:
            #More relevant reviews from google
            place = gmaps.place(id_google, language='es', reviews_no_translations=True, reviews_sort='most_relevant')
            for review in place['result']['reviews']:
                if review['text'] == '':
                    continue
                reviews['google'].append({'review': review['text'], 'id_review': review['time']})

        return reviews
    
    def get_triplets_from_colab(self, db, reviews, id_google, id_yelp, id_tripadvisor):
        reviews_triplets = []

        for service, reviews_by_service in reviews.items():
            if reviews_by_service == []:
                continue
            for review in reviews_by_service:
                id_restaurant = eval(f'id_{service}')
                if db[f'reviews_{service}'].find_one({
                        f'id_{service}': id_restaurant, 
                        'id_review': review['id_review'] }) != None:
                    continue
                text_and_triplets = utilities.get_triplets(review['review'])
                triplets = text_and_triplets['triplets']
                text = text_and_triplets['review']
                print(text)
                print(triplets)
                db[f'reviews_{service}'].insert_one({
                    f'id_{service}': id_restaurant,
                    'id_review': review['id_review'],
                    'review': text,
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
    def save(self, db, name, id_google, id_yelp, id_tripadvisor):
        #Obtener las reviews de google y yelp
        reviews = self.get_reviews(self, id_google, id_yelp, id_tripadvisor)
        for service, reviews_by_service in reviews.items():
            print(service, '\n', '-'*50, '\n')
            print(reviews_by_service)
        #mandarlas al colab que regrese los tripletes
        reviews_triplets = self.get_triplets_from_colab(self, db, reviews, id_google, id_yelp, id_tripadvisor)
        if reviews_triplets == []:
            return
        print("reviews_triplets\n")
        print(reviews_triplets)
        # Clusterizar los tripletes
        #relevant_pairs = utilities.get_relevant_pairs(reviews_triplets)
        #print(relevant_pairs)
        # Envíar al gpt-4
        #generate_review = utilities.generate_review(relevant_pairs)
        #print(generate_review)
        try:
            db['restaurants'].insert_one({
                'name': name, 
                'review': "Falta generar la review", 
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
        
    @classmethod
    def get_reviews_from_db(self, db, id_google, id_yelp):
        try:
            reviews_yelp = db['reviews_yelp'].find({'id_yelp': id_yelp})
            reviews_google = db['reviews_google'].find({'id_google': id_google})
            #transform the cursor to a list and concat the lists
            reviews = list(reviews_yelp) + list(reviews_google)
            return reviews
        except Exception as ex:
            raise Exception(ex)