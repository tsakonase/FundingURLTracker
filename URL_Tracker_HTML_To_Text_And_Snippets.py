import requests
from bs4 import BeautifulSoup
import nltk
import unidecode
from nltk.tokenize import word_tokenize, sent_tokenize
from string import punctuation
from nltk.corpus import stopwords
nltk.download("stopwords")
nltk.download("wordnet")

keyphrases = [

"not scrape",
"not data mining", 
"allow to reuse",
"public domain",
"public sector information",
"CC BY",
"CC0",
"CC BY-SA",
"CC BY-NC",
"CC BY-NC-SA",
"CC BY-ND",
"CC BY-NC-ND",
"without the written permission",
"without permission",
"rights reserved",
"commercial purposes",
"commercial use",
"non-commercial",
"personal use",
"reproduce for personal use",
"reproduction is prohibited",
"must not reproduce"
]

class TokenizeText:

    def __init__(self):
        self.stopword_set = set(stopwords.words("english"))
        self.word_stemmer = nltk.WordNetLemmatizer()
        self.punctuation = set(punctuation)

    def purge_punct_tok(self, word):
        return ''.join(c for c in word if c not in punctuation)

    def word_tokenize(self, text, remove_punct = True, remove_stopwords = False, stem_words = False, purge_token_punct=False):
        # unidecode the text:
        n_text = unidecode.unidecode(text).replace("\n", " ")
        # nltk tokenization
        tokens = [word.lower() for sent in sent_tokenize(n_text) for word in word_tokenize(sent)]
        # if remove punctuation:
        if remove_punct:
            tokens = [token for token in tokens if not all(char in self.punctuation for char in token)]
        # if remove stopwords:
        if remove_stopwords:
            tokens = [token for token in tokens if token not in self.stopword_set]
        # if stem words:
        if stem_words:
            tokens = [self.word_stemmer.lemmatize(token) for token in tokens]
        # if purge punctuation within a token:
        if purge_token_punct:
            tokens = [self.purge_punct_tok(token) for token in tokens]

        return tokens

import os
from bs4 import BeautifulSoup
import unidecode
from termcolor import colored
from collections import defaultdict
import shutil

karam_directory = "path/to/HTMLpages/Results"
new_directory  = "path/to/URL_Tracker_ManualValidation"

for filename in os.listdir(karam_directory):
    snippets = []
    soup = BeautifulSoup(open(os.path.join(karam_directory, filename), "rb"), "html.parser")
    txt = soup.find_all(text=True)
    text = ' '.join([s for s in list(txt) if s.strip().strip("\n").strip()])
    os.mkdir(new_directory + "/" + filename[:-5] + "/")
    
    shutil.copy(karam_directory + "/" + filename, new_directory + "/" + filename[:-5] + "/" )
    
    with open(new_directory + "/" + filename[:-5] + "/" + filename[:-5] + "_text", "w") as f:
        f.write(unidecode.unidecode(text))
        
    n_sents = [sent.lower() for sent in sent_tokenize(unidecode.unidecode(text))]
    for keyphrase in keyphrases:
        n_keyphrase = unidecode.unidecode(keyphrase).lower()
        for n_sent in n_sents:
            if n_keyphrase in n_sent:
                snippets.append("KEYPHRASE: " + keyphrase + " is in the SENTENCE: " + n_sent)
                
    with open(new_directory + "/" + filename[:-5] + "/" + filename[:-5] + "_snippets", "w") as f:
        f.write("\n".join(snippets))

        
