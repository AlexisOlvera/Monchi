import BERT_encoding
import lda_training
import normalize
import visualize
import extract

from sklearn.cluster import KMeans
import gensim.corpora as corpora
import pickle

# Change path to where "generate_cp.txt" is located
stopwords_root = '/Users/fabiola/Documents/ESCOM/Trabajo terminal/proyecto/clusterizacion/kmeans_lda/generate_cp.txt'
topic_list = []
trims = []
k = 3

# Deserialize list of tuples (aspect, opinion)
with open('pairs.pkl', 'rb') as f:
    phrase_pairs = pickle.load(f) 

# K-means
# Normalize phrase pairs
phrase_pairs = normalize.clean(phrase_pairs, stopwords_root)
# Train model and get clusters
vectors = BERT_encoding.encoding(phrase_pairs)
# Clusterizar los vectores utilizando KMeans
kmeans = KMeans(n_clusters=k, random_state=0).fit(vectors)
labels = kmeans.labels_
clusters_kmeans = [[None]]*k
for i, pair in enumerate(phrase_pairs):
    clusters_kmeans[labels[i]].append(pair)

clusters_kmeans[0].pop(0)
# Print
pair_clusters = visualize.print_to_vis(clusters_kmeans[0], labels)
X = visualize.cluster_plot(labels, vectors)
visualize.elbow_plot(X)


# LDA
# Extract opinions
opinions = extract.opinions(pair_clusters[1])
# Create Dictionarys
id2word_o = corpora.dictionary.Dictionary([opinions])
# Frequency list: aspects
o_freq_list = extract.tf(opinions, id2word_o)
# List to dict for sorting
o_freq_dict = dict(o_freq_list)
# Sort frequency on aspects
sorted_freq_opinions = sorted(o_freq_dict.items(), key=lambda x: x[1], reverse=True)
# LDA model training
opinion_lda_model, topics = lda_training.train(o_freq_list, id2word_o, sorted_freq_opinions)
# LDA visualization for aspect/opinion
# visualize.visLDA(opinion_lda_model, o_freq_list, id2word_o, 'opinions') 

# Get distribution
topics_as_list = [topic for topic in topics]
for pair in topics_as_list:
    topic_list.append(pair)

topic_list = topic_list[0][1]
topic_list = topic_list.split("+")
for item in topic_list:
  trims.append(item.split("*"))

topic_list = []
for pair in trims:
    topic_list.append(pair[1].replace('"', ""))

print(topic_list)