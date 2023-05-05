import sys
import re

import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords
stop_words = set(stopwords.words("english"))

# tokenize a string of text into tokens of alphanumeric characters
def tokenize(text):
    tokens = []

    alphanum = re.compile("^[a-z]|[0-9]&")

    word = ""
    for char in text:    
        char = char.lower()
        if(alphanum.search(char)): 
            # builds tokens as it iterates through each character
            word += char
        else:
            # add fully built token to list
            if(word != "" or len(word) > 1):
                tokens.append(word)
                word = ""
            if(char == ""):
                break

    return tokens

#filters out stopwords from a list of tokens.
def remove_stopwords(tokens):
    filtered_list = []

    for t in tokens:
        if t in stop_words:
            continue
        filtered_list.append(t)

    return filtered_list

# Creates a dictionary of frequencies of all the tokens.
def computeWordFrequencies(tokens):
    # Use a dictionary to map tokens to frequency count
    freq = {}

    #increments the count of each token
    for t in tokens:
        if(t not in freq):
            freq[t] = 1
        else:
            freq[t] += 1

    return freq