def stopword_dict(stopwords_path):
    from pickle import dump

    with open (stopwords_path, encoding='latin-1') as f:
        lines = f.readlines()

    sw_dir = {}

    for line in lines:
        line = line.strip()
        if line != '':
            words = line.split()
            token = words[0].strip()
            # uncomment for generate_cp.txt
            # token = token.replace('#', '')
            lemma = words[-1].strip()
            sw_dir[token] = lemma
    
    lemmas_list = list(sw_dir.items())
    return lemmas_list

# Entire doc
def clean(pairs, stopwords_path):
    cleaned = []
    stopwords = dict(stopword_dict(stopwords_path))
    pairs = [[word.lower() for word in pair] for pair in pairs]

    for i, pair in enumerate(pairs):
      if pair[0] in stopwords.keys():
        pairs[i][0] = pairs[i][0].replace(pair[0], stopwords[pair[0]])
      if pair[1] in stopwords.keys():
        pairs[i][1] = pairs[i][1].replace(pair[1], stopwords[pair[1]])
   
    return pairs