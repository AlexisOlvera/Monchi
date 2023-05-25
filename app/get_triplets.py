
from clusterizacion.BERT_encoding import encoding
from clusterizacion.lda_training import train
from clusterizacion.normalize import clean 
from clusterizacion.visualize import print_to_vis
from clusterizacion.extract import extract_opinions, tf

from sklearn.cluster import KMeans
import gensim.corpora as corpora


def get_relevant_pairs(phrase_pairs):
    stopwords_root = '../generate_cp.txt'
    k = 3

    # K-means
    # Normalize phrase pairs
    phrase_pairs = clean(phrase_pairs, stopwords_root)
    # Train model and get clusters
    vectors = encoding(phrase_pairs)
    # Clusterizar los vectores utilizando KMeans
    kmeans = KMeans(n_clusters=k, random_state=0).fit(vectors)
    labels = kmeans.labels_
    clusters_kmeans = [[None]]*k
    for i, pair in enumerate(phrase_pairs):
        clusters_kmeans[labels[i]].append(pair)

    clusters_kmeans[0].pop(0)
    # Print
    pair_clusters = print_to_vis(clusters_kmeans[0], labels)
    relevant_pairs = []
    # LDA
    for cluster in pair_clusters:
        topic_list = []
        trims = []
        # Extract opinions
        opinions = extract_opinions(cluster)
        # Create Dictionarys
        id2word_o = corpora.dictionary.Dictionary([opinions])
        # Frequency list: aspects
        o_freq_list = tf(opinions, id2word_o)
        # List to dict for sorting
        o_freq_dict = dict(o_freq_list)
        # Sort frequency on aspects
        sorted_freq_opinions = sorted(o_freq_dict.items(), key=lambda x: x[1], reverse=True)
        # LDA model training
        opinion_lda_model, topics = train(o_freq_list, id2word_o, sorted_freq_opinions)
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
            topic_list.append(pair[1].replace('"', "").rstrip())

        relevant_pairs_per_cluster = []
        for opinion in cluster:
            if opinion[1] in topic_list:
                relevant_pairs_per_cluster.append(opinion)
        relevant_pairs.append(relevant_pairs_per_cluster)
    
    return relevant_pairs