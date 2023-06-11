import torch
#from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import SpectralClustering
from transformers import BertModel, BertTokenizer
from sklearn.decomposition import PCA
import csv

def encoding(phrase_pairs):
    vectors = []
    # Load BERT model pre-trained and tokenizer
    model_name = 'dccuchile/bert-base-spanish-wwm-cased'
    model = BertModel.from_pretrained(model_name, output_hidden_states=True)
    tokenizer = BertTokenizer.from_pretrained(model_name)

    aspects = [pair[0] for pair in phrase_pairs]

    # embedding_aspects.csv = cesped,"[0.2315973937511444, 0.467934787273407, ... ] \n liebre,"[0.6224402785301208, -0.03878629580140114, ...], ...  
    # load the vectors of the aspects and if is not found, encode it
    with open('embedding_aspects.csv', 'r') as f:
        reader = csv.reader(f)
        aspects_embbeding = dict(reader)
        
    for aspect in aspects:
        if aspect in aspects_embbeding:
            vectors.append(eval(aspects_embbeding[aspect]))
        else:
            encode_aspect = tokenizer(aspect, return_tensors="pt")
            with torch.no_grad():
                outputs = model(**encode_aspect)
                vector = outputs[2][-1][0][0]
                vectors.append(vector.tolist())  

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

def enconde_list_of_sentences(sentences):
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
    