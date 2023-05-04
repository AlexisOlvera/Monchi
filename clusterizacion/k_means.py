from transformers import BertModel, BertTokenizer
import torch
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import SpectralClustering
# Cargar el modelo BERT pre-entrenado y su tokenizer
model_name = 'dccuchile/bert-base-spanish-wwm-cased'
model = BertModel.from_pretrained(model_name, output_hidden_states=True)
tokenizer = BertTokenizer.from_pretrained(model_name)

# Definir los pares de frases a clusterizar
phrase_pairs = [
  ('lugar', 'enamorada'), 
  ('lugar', 'solicitado'), 
  ('lugar', 'ideal para pasarla con amigos'), 
  ('lugar', 'chiquito'), 
  ('lugar', 'acogedor'), 
  ('lugar', 'chiquitito'), 
  ('lugar', 'me encanta'), 
  ('lugar', 'pequeño'), 
  ('cocktailes', 'espectaculares'), 
  ('limonana', 'buenisimo'), 
  ('agua de almendras', 'buenisimo'), 
  ('humus', 'exquisitos'), 
  ('opcion', 'excelente'), 
  ('opcion', 'extraordinaria'), 
  ('platillos', 'pequeños'), 
  ('platillos', 'abundantes'), 
  ('sabores', 'exquisitos'), 
  ('hojas de parra', 'excelente'), 
  ('coliflor asada', 'excelente'), 
  ('postres', 'deliciosos'), 
  ('precios', 'excelentes'), 
  ('precios', 'justos'), 
  ('RESTAURANTE', 'regresare'), 
  ('RESTAURANTE', 'favorito'), 
  ('RESTAURANTE', 'favoritos'), 
  ('RESTAURANTE', 'ideal'), 
  ('RESTAURANTE', 'bien'), 
  ('RESTAURANTE', 'volveremos'), 
  ('RESTAURANTE', 'agradable sorpresa'), 
  ('RESTAURANTE', 'recomiendo'), 
  ('RESTAURANTE', 'buena opcion'), 
  ('RESTAURANTE', 'volveria sin dudarlo'), 
  ('RESTAURANTE', 'recomendable'), 
  ('comida', 'me encanta'), 
  ('comida', 'deliciosa'), 
  ('vino shiraz', 'rico'), 
  ('french toast', 'lo maximo'), 
  ('blintzes', 'lo maximo'), 
  ('relacion calidad precio', 'buena'), 
  ('menus', 'sucios y pegajosos'), 
  ('mesero', 'grosero'), 
  ('sabor', 'diferente y sorpresivo'), 
  ('ceviche', 'vale la pena'), 
  ('pan pita', 'espectacular'), 
  ('limonada con gin', 'refrescante'), 
  ('tarta de datil', 'un most'), 
  ('tabbuleh', 'puro trigo'), 
  ('kibbeh', 'crudo'), 
  ('kibbeh', 'demasiado m trigo y poca carne'), 
  ('botellas de agua natural', 'huelen aun a cloro'), 
  ('calidad de platillos', 'impresionante'), 
  ('originalidad', 'impresionante'), 
  ('ambiente', 'agradable'), 
  ('cordero al horno', 'delicioso'), 
  ('restaurante', 'pequeño y muy concurrido'), 
  ('chamorro', 'festin'), 
  ('preparacion', 'saludable')
]

# Codificar los pares de frases utilizando el modelo BERT
vectors = []
input_sentences = []
embeddings = None
for pair in phrase_pairs:
    input_sentences.append(pair[0]+' '+pair[1])

for pair in phrase_pairs:
    encoded_pair = tokenizer.encode_plus(pair[0], pair[1], add_special_tokens=True, return_tensors='pt')
    with torch.no_grad():
        outputs = model(**encoded_pair)
        vector = outputs[2][-1][0][0] # Tomar la última capa oculta de BERT
        vectors.append(vector.tolist())
    encoded_inputs = tokenizer(input_sentences, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**encoded_inputs)
        embeddings = outputs.last_hidden_state[:, 0, :].numpy()

similarity_matrix = cosine_similarity(embeddings)
n_clusters = 10
clusterer = SpectralClustering(n_clusters=n_clusters, affinity="precomputed")
labels = clusterer.fit_predict(similarity_matrix)

clusters_spectral = [[None]]*10
for i, label in enumerate(labels):
    clusters_spectral[label].append(input_sentences[i])
    
pca = PCA(n_components=3)
X = pca.fit_transform(vectors)

# Clusterizar los vectores utilizando KMeans
num_clusters = 10
kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(vectors)
labels = kmeans.labels_
clusters_kmeans = [[None]]*10
for i, pair in enumerate(phrase_pairs):
    clusters_kmeans[labels[i]].append(pair)

for clust, words in enumerate(clusters_spectral):
    print(f"Cluster {clust}")
    print("-"*30)
    for word in words:
        print(word)


for clust, words in enumerate(clusters_kmeans):
    print(f"Cluster {clust}")
    print("-"*30)
    for word in words:
        print(word)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X[:,0], X[:,1], X[:,2], c=kmeans.labels_)
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()
