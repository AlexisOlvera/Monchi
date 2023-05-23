def aspects(pairs):
    # List of words in first position: aspects
    aspect_list = []
    for pair in pairs:
        aspect_list.append(pair[0].lower())
    
    return aspect_list

def opinions(pairs):
    # List of words in second position: opinions
    opinion_list = []
    for pair in pairs:
        opinion_list.append(pair[1].lower())
    
    return opinion_list

def tf(target, id2word):
    # Term Document Frequency, list
    freq_list = [id2word.doc2bow(target)]
    freq_list = freq_list[0]
    
    return freq_list