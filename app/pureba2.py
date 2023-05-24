
import requests
from pymongo import MongoClient
from get_triplets import get_relevant_triplets
MONGODB_CONNECTION_STRING = "mongodb+srv://monchi:QKy3NzXLu2k3l1XD@restaurants.svwsl9k.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client['monchi']

def get_triplets(review : str):
    url_ngrok = "http://c95f-35-226-206-45.ngrok-free.app"
    url_colab = url_ngrok+f"/api/predict?review='{review}'"
    print(url_colab)
    response = requests.get(url_colab)
    return response.json()

review = """
Contramar es quizás el mejor lugar de la Ciudad de México de comida de mar, sin embargo, su calidad se encuentra en el rango inferior cuando lo comparas con restaurantes de las playas de México. Su resalte es sujeto al contexto, no general.
El platillo que más disfruté fue el filete de pez espada y las tostadas de atún.
El precio-valor lo considero un poco elevado y su servicio de facturación en línea simplemente no sirve, así que les recomiendo hacerla en el lugar.
"""

id_review = "1"
id_yelp = 'X4hcgB5vwqM-hq00zzdQdg'
triplets = get_triplets(review)

print(triplets)

phrase_pairs = []
for triplet in triplets:
    phrase_pairs.append((triplet['aspect'], triplet['opinion']))

print(phrase_pairs)

relevant_triplets = get_relevant_triplets(phrase_pairs)

print(relevant_triplets)