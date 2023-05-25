import requests
import json
import openai
from get_triplets import get_relevant_pairs
class utilities:
    @staticmethod
    def data_to_list_ploty(data : dict):
        labels = []
        values = []
        parents = []
        for aspect, opinions_sent in data.items():
            labels.append(aspect)
            parents.append('')
            values.append(sum(opinions_sent.values()))
            for opinion, count in opinions_sent.items():
                labels.append(opinion)
                parents.append(aspect)
                values.append(count)
        return labels, parents, values
    

    @staticmethod
    def get_triplets(review : str):
        url_ngrok = "http://795c-35-197-129-71.ngrok-free.app"
        url_colab = url_ngrok+f"/api/predict?review='{review}'"
        response = requests.get(url_colab)
        return response.json()


    @staticmethod
    def get_relevant_pairs(triplets : list):
        phrase_pairs = [(triplet['aspect'], triplet['opinion']) for triplet in triplets]
        with open('phrase_pairs.json', 'w') as file:
            json.dump(phrase_pairs, file)
        relevant_pairs = get_relevant_pairs(phrase_pairs)
        with open('relevant_aspects.json', 'w') as file:
            json.dump(relevant_pairs, file)
        top_three = []
        for clusters in relevant_pairs:
            top_three.extend(clusters[:3])
        return top_three
    
    @staticmethod
    def generate_review(relevant_pairs : list):
        openai.api_key = "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"
        promt = f"""
        Escribe una reseña que incluya la siguiente lista de pares de aspectos y opiniones, es decir [aspecto, opinion], donde la opinion es un adjetivo que califica al aspecto:
        {str(relevant_pairs)}
        """
        print(promt)
        response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
                    {"role": "system", "content": "Eres un critico de restaurantes que escribe en un peridico de gran nombre, y que sus reseñas son de un maximo de 500 caracteres."},
                    {"role": "user", "content": promt}
                ]
        )
        print(response['choices'][0]['message']['content'])
        return response['choices'][0]['message']['content']