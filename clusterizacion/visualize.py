from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pyLDAvis.gensim_models
from pprint import pprint
import pyLDAvis
import pickle


# Print
def print_to_vis(clusters, labels):
    cluster_0 = []
    cluster_1 = []
    cluster_2 = []
    for i, each in enumerate(labels):
        if labels[i] == 0:
            cluster_0.append(clusters[i])
        if labels[i] == 1:
            cluster_1.append(clusters[i])
        if labels[i] == 2:
            cluster_2.append(clusters[i])

    clusters = [cluster_0, cluster_1, cluster_2]

    for cl in clusters:
        print(cl)
        print(len(cl))

    #print(kmeans.n_iter_)
    return clusters


def cluster_plot(labels, vectors):
    #n_comp = min(len(phrase_pairs), 2)
    n_comp = 3
    pca = PCA(n_components=n_comp)
    X = pca.fit_transform(vectors)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X[:,0], X[:,1], X[:,2], c=labels)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()

    return X


def elbow_plot(X):
    sse = []
    k_rng = range(1,10)
    for k in k_rng:
        km = KMeans(n_clusters = k)
        km.fit(X)
        sse.append(km.inertia_)


def visLDA(lda_model, freq_list, id2word, vis):
    # Visualize the topics
    LDAvis_file = '/Users/fabiola/Documents/ESCOM/Trabajo terminal/proyecto/clusterizacion/kmeans_lda/result'+vis+'.txt'
    #LDAvis_file = '/content/result'+vis+'.txt'

    if 1 == 1:
        LDAvis_prepared = pyLDAvis.gensim_models.prepare(lda_model, [freq_list], id2word)
        with open(LDAvis_file, 'wb') as f:
            pickle.dump(LDAvis_prepared, f)
    # load the pre-prepared pyLDAvis data from disk
    with open(LDAvis_file, 'rb') as f:
        LDAvis_prepared = pickle.load(f)
    # Save on html file     
    pyLDAvis.save_html(LDAvis_prepared, 'result_'+ vis +'.html')
    LDAvis_prepared


def get_topics(topics):
    pprint(topics)
