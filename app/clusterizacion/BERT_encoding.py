import torch
#from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import SpectralClustering
from transformers import BertModel, BertTokenizer
from sklearn.decomposition import PCA

def encoding(phrase_pairs):
    vectors = []
    input_sentences = []
    embeddings = None

    # Load BERT model pre-trained and tokenizer
    model_name = 'dccuchile/bert-base-spanish-wwm-cased'
    model = BertModel.from_pretrained(model_name, output_hidden_states=True)
    tokenizer = BertTokenizer.from_pretrained(model_name)



    for pair in phrase_pairs:
        input_sentences.append(pair[0])

    for pair in phrase_pairs:
        #tokinize just the pair[0]
        encode_aspect = tokenizer(pair[0], return_tensors="pt")
        with torch.no_grad():
            outputs = model(**encode_aspect)
            vector = outputs[2][-1][0][0] # Tomar la última capa oculta de BERT
            vectors.append(vector.tolist())
        encoded_inputs = tokenizer(input_sentences, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**encoded_inputs)
            embeddings = outputs.last_hidden_state[:, 0, :].numpy()

    similarity_matrix = cosine_similarity(embeddings)
    n_clusters = 3
    clusterer = SpectralClustering(n_clusters=n_clusters, affinity="precomputed")
    labels = clusterer.fit_predict(similarity_matrix)
    clusters_spectral = [[None]]*3
    for i, label in enumerate(labels):
        clusters_spectral[label].append(input_sentences[i])
    
    return vectors

def encode_sentence(sentence: str):
    # Load BERT model pre-trained and tokenizer
    model_name = 'dccuchile/bert-base-spanish-wwm-cased'
    model = BertModel.from_pretrained(model_name, output_hidden_states=True)
    tokenizer = BertTokenizer.from_pretrained(model_name)

    #tokinize just the pair[0]
    encode_aspect = tokenizer(sentence, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**encode_aspect)
        vector = outputs[2][-1][0][0] # Tomar la última capa oculta de BERT
        return vector.tolist()

def enconde_list_of_sentences(sentences: list[str]):
    # Load BERT model pre-trained and tokenizer
    encoded_sentences = []
    model_name = 'dccuchile/bert-base-spanish-wwm-cased'
    model = BertModel.from_pretrained(model_name, output_hidden_states=True)
    tokenizer = BertTokenizer.from_pretrained(model_name)

    for sentence in sentences:
        with torch.no_grad():
            encode_aspect = tokenizer(sentence, return_tensors="pt")
            outputs = model(**encode_aspect)
            vector = outputs[2][-1][0][0] # Tomar la última capa oculta de BERT
            encoded_sentences.append(vector.tolist())

    return encoded_sentences
    
def redude_2d(bert_vectors):
    #Use PCA to reduce the dimensionality of the vector and sklearn to reduce it to 2D
    pca = PCA(n_components=2)
    reduced_vectors = pca.fit_transform(bert_vectors)
    return reduced_vectors
    