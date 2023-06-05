import gensim.models as models

#LDA model training
def train(freq_list, id2word, sorted_aspects):
    # number of topics
    num_topics = 10
    # Build LDA model
    lda_model = models.LdaModel(
        corpus=[freq_list], 
        id2word=id2word, 
        num_topics=num_topics, 
        update_every=1, 
        chunksize=10000, 
        passes=1)
    # Print the most relevant topics
    relevant_topics = lda_model.print_topics(num_topics=1, num_words=3)

    return lda_model, relevant_topics