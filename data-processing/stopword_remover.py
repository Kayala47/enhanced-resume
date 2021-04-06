from nltk.corpus import stopwords 

def remove_from(word_tokens):
    stop_words = set(stopwords.words('english')) 
    filtered_sentence = [] 
  
    for w in word_tokens: 
        if w not in stop_words: 
            filtered_sentence.append(w) 

    return filtered_sentence