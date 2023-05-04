import numpy as np
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import torch
from transformers import AutoTokenizer, AutoModel

MODEL_NAME = 'dccuchile/bert-base-spanish-wwm-cased'
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

word_spans = [
  'RESTAURANTE recomendable' , 
'RESTAURANTE excelente opcion' , 
'RESTAURANTE buena opcion' , 
'RESTAURANTE recomiendo ir en la noche' , 
'RESTAURANTE sorpresa' , 
'RESTAURANTE favoritos' , 
'RESTAURANTE buen espacio' , 
'RESTAURANTE sorprendio para bien' , 
'RESTAURANTE recomendado' , 
'servicio atento y amigable al instante' , 
'servicio rapido y amable' , 
'menu delicioso' , 
'comidon espectacular' , 
'lugar para cenar con amigos' , 
'lugar agradable' , 
'lugar para pasar un buen rato con amigos' , 
'lugar para echar unos buenos tragos' , 
'lugar recomiendo' , 
'espacio lindo' , 
'atencion excelente' , 
'atencion buena y amigable' , 
'vino de la casa delicioso' , 
'dumplings decentes' , 
'risotto de limon bueno' , 
'milanesa recomendado' , 
'porcion perfecta' , 
'sabor lo vale' , 
'sabor bien' , 
'fondant de dulce de leche bueno' , 
'carta gourmet buena' , 
'variedad reducida' , 
'todos los platillos garantia' , 
'precio moderado' , 
'precio bajo' , 
'pulpo a las brasas de lo mejor' , 
'carnitas de conejo de lo mejor' , 
'seleccion de vinos buena' , 
'entrada no muy agradable' , 
'cocteles buenos' , 
'cocteles chicos' , 
'cocteles caros' , 
'comida interesante' , 
'comida servida medio fria' , 
'comida fino y delicado toque' , 
'comida deliciosa' , 
'comida buena' , 
'comida increible' , 
'risotto mal hecho' , 
'risotto pastoso y crudo' , 
'camarones ricos' , 
'gente amable' , 
'vibra buena' , 
'platillos exquisitos' , 
'platillos disfrutaras' , 
'chef creativo' , 
'chef inteligencia y practicidad' , 
'creaciones buenas' , 
'comer bien' , 
'barecito simplon' , 
'ambiente buen' , 
'ambiente padre' , 
'todo bueno' , 
'casa bonita y bien decorada' , 
'tapas lo mejor' , 
'tapas perfectas para compartir' , 
'sandwiches un clasico' , 
'calidad se perdio' , 
'zona pequeña' , 
'zona acogedora' , 
'parte grande bonita' , 
'vinos increibles' , 
'vino buen' , 
'calidad de los alimentos excelsa'
]

# Encode de frases y obtener las salidas del modelo
inputs = tokenizer(word_spans, return_tensors='pt', padding=True, truncation=True)
with torch.no_grad():
    outputs = model(**inputs)

# Tomar el promedio de todos los tokens en cada frase
embeddings = np.mean(outputs["last_hidden_state"].numpy(), axis=1)


n_clusters = 10
kmeans = KMeans(n_clusters=n_clusters)
kmeans.fit(embeddings)
labels = kmeans.labels_

pca = PCA(n_components=3)
reduced = pca.fit_transform(embeddings)

# Graficar los clusters en 3D
fig = px.scatter_3d(reduced,
                    x=0, y=1, z=2,
                    text = word_spans,
                    color=labels,
                    labels={'color': 'Cluster'})

fig.show()