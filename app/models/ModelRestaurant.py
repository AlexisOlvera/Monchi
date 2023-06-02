import datetime
from .entities.Restaurant import Restaurant
import requests
import googlemaps
from utilities import utilities
from clusterizacion.BERT_encoding import enconde_list_of_sentences, redude_2d, encode_sentence

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
    def get_reviews_from_db(self, db, id_google, id_yelp, id_tripadvisor):
        try:
            reviews_yelp = db['reviews_yelp'].find({'id_yelp': id_yelp})
            reviews_google = db['reviews_google'].find({'id_google': id_google})
            reviews_tripadvisor = db['reviews_tripadvisor'].find({'id_tripadvisor': id_tripadvisor})
            #transform the cursor to a list and concat the lists
            reviews = list(reviews_yelp) + list(reviews_google) + list(reviews_tripadvisor)
            return reviews
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def save_data_of_bubble_plot(self, db, restaurant: Restaurant):
        reviews = self.get_reviews_from_db(db, restaurant.id_google, restaurant.id_yelp, restaurant.id_tripadvisor)
        aspects = utilities.get_aspects(reviews)
        opinions = utilities.get_opinions(reviews) 
        #make a dict with count of each aspect and other dict with count of each opinion

        set_of_aspects = set(aspects)
        set_of_opinions = set(opinions)
        aspects_data = []
        opinions_data = []
        encoded_aspects = enconde_list_of_sentences([aspect for aspect in set_of_aspects])
        encoded_opinions = enconde_list_of_sentences([opinion for opinion in set_of_opinions])
        reduced_vector_aspects = redude_2d(encoded_aspects)
        reduced_vector_opinions = redude_2d(encoded_opinions)
        for index, aspect in enumerate(set_of_aspects):
            aspects_data.append({
                'aspect': aspect,
                'x': reduced_vector_aspects[index][0],
                'y': reduced_vector_aspects[index][1],
                'size': aspects.count(aspect)
            })

        for index, opinion in enumerate(set_of_opinions):
            opinions_data.append({
                'opinion': opinion,
                'x': reduced_vector_opinions[index][0],
                'y': reduced_vector_opinions[index][1],
                'size': opinions.count(opinion)
            })

        try:
            db['data_of_bubble_plot'].insert_one({
                'id_restaurant': restaurant._id,
                'aspects': aspects_data,
                'opinions': opinions_data
            })
        except Exception as ex:
            raise Exception(ex)
        
        return {'status': 'ok'}

    @classmethod
    def get_data_of_bubble_plot(self, db, id_restaurant):
        try:
            data = db['data_of_bubble_plot'].find_one({'id_restaurant': id_restaurant})
            if data == None:
                return None
            result = {}
            x = []
            y = []
            size = []
            text = []
            for aspect in data['aspects']:
                x.append(aspect['x'])
                y.append(aspect['y'])
                size.append(aspect['size'])
                text.append(aspect['aspect'])
            result['aspects'] = {'x': x, 'y': y, 'size': size, 'text': text}
            x = []
            y = []
            size = []
            text = []
            for opinion in data['opinions']:
                x.append(opinion['x'])
                y.append(opinion['y'])
                size.append(opinion['size'])
                text.append(opinion['opinion'])
            result['opinions'] = {'x': x, 'y': y, 'size': size, 'text': text}
            return result
        except Exception as ex:
            raise Exception(ex)
        

    
    @classmethod
    def find(self, db, restaurant_name):
        try:
            result = db['restaurants'].find_one({'name': {"$regex": restaurant_name, "$options": "i"}})
            print(result)
            if result != None:
                restaurant  = Restaurant(**result)
                return restaurant
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
        if(not(reviews['yelp'] == [] and reviews['google'] == [] and reviews['tripadvisor'] == [])):
            reviews_triplets = self.get_triplets_from_colab(self, db, reviews, id_google, id_yelp, id_tripadvisor)
        print("reviews_triplets\n")
        print(reviews_triplets)
        reviews_triplets = self.get_reviews_from_db(db, id_google, id_yelp, id_tripadvisor)
        triplets = []
        for review_triplet in reviews_triplets:
            triplets.extend(review_triplet['triplets'])

        #print(triplets)
        # Clusterizar los tripletes
        relevant_pairs = utilities.get_relevant_pairs(triplets)
        print(relevant_pairs)
        # Envíar al gpt-4
        generated_review = utilities.generate_review(relevant_pairs)
        print(generated_review)
        try:
            db['restaurants'].insert_one({
                'name': name, 
                'review': generated_review, 
                'id_google': id_google, 
                'id_yelp': id_yelp, 
                'id_tripadvisor': id_tripadvisor,
                'data': utilities.from_triplets_to_db(triplets),
                'relevant_pairs': relevant_pairs,
                'last_updated': datetime.datetime.now()
            })
            #find by id_google
            resturant = Restaurant(**db['restaurants'].find_one({'id_google': id_google}))
            self.save_data_of_bubble_plot(db, resturant)
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
            restaurant = Restaurant(**db['restaurants'].find_one({'_id': _id}))
            if restaurant == None:
                return
            reviews = self.get_reviews_from_google_yelp(restaurant.id_google, restaurant.id_yelp, restaurant.id_tripadvisor, True)
            
            if(not(reviews['yelp'] == [] and reviews['google'] == [] and reviews['tripadvisor'] == [])):
                reviews_triplets = self.get_triplets_from_colab(self, db, reviews, restaurant.id_google, restaurant.id_yelp, restaurant.id_tripadvisor)
            reviews_triplets = self.get_reviews_from_db(db, restaurant.id_google, restaurant.id_yelp, restaurant.id_tripadvisor)
            triplets = []
            for review_triplet in reviews_triplets:
                triplets.extend(review_triplet['triplets'])

            relevant_pairs = utilities.get_relevant_pairs(triplets)
            # Envíar al gpt-4
            generate_review = utilities.generate_review(relevant_pairs)
            db['restaurants'].update_one({'_id': _id}, 
                {"$set": {'review': generate_review}},
                {"$set": {'last_updated': datetime.datetime.now()}}, 
                {"$set": {'data': utilities.from_triplets_to_db(triplets)}},
                {"$set": {'relevant_pairs': relevant_pairs}}
            )
        except Exception as ex:
            raise Exception(ex)
        
    


