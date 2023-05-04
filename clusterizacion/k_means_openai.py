import openai
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# set OpenAI API key
openai.api_key = "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"

# read phrases from file
with open("phrases.txt") as f:
    phrases = f.read().splitlines()

# embed phrases using OpenAI model
with open("embeddings.txt", 'r+') as f:
    embeddings = eval(f.read())
"""embeddings = []
for phrase in phrases:
    response = openai.Embedding.create(input=phrase, model="text-embedding-ada-002")
    embeddings.append(response['data'][0]['embedding'])

with open("embeddings.txt", '+w') as f:
    f.write(str(embeddings))
"""
# reduce dimensionality to 3D using PCA
reduced_embeddings = PCA(n_components=3).fit_transform(embeddings)

# cluster embeddings using k-means
kmeans = KMeans(n_clusters=10, random_state=0).fit(embeddings)
labels = kmeans.labels_

# plot clusters in 3D space
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'w']

for i in range(len(labels)):
    ax.scatter(reduced_embeddings[i][0], reduced_embeddings[i][1], reduced_embeddings[i][2])

plt.show()
