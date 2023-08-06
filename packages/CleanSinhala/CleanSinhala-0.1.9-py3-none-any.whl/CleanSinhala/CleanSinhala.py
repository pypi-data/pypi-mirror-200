def simplify(word):    
    simplify_words={
        'මූහූදට':'මුහුදට',
        U'\U0001F622':'sad',
        'පතුම්':'පැතුම්',
        'Chanaka':'Eranga'
    }
    try:
        return simplify_words[word]
    except KeyError:
        return word

    
   