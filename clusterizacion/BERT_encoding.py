import torch
#from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import SpectralClustering
from transformers import BertModel, BertTokenizer

def encoding(phrase_pairs):
    vectors = []
    input_sentences = []
    embeddings = None

    # Load BERT model pre-trained and tokenizer
    model_name = 'dccuchile/bert-base-spanish-wwm-cased'
    model = BertModel.from_pretrained(model_name, output_hidden_states=True)
    tokenizer = BertTokenizer.from_pretrained(model_name)

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
    n_clusters = 3
    clusterer = SpectralClustering(n_clusters=n_clusters, affinity="precomputed")
    labels = clusterer.fit_predict(similarity_matrix)
    clusters_spectral = [[None]]*3
    for i, label in enumerate(labels):
        clusters_spectral[label].append(input_sentences[i])
    
    return vectors
