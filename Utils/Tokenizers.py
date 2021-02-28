import nltk
import unidecode
from nltk.tokenize import word_tokenize, sent_tokenize
from string import punctuation
from nltk.corpus import stopwords

nltk.download("stopwords")
nltk.download("wordnet")
"""
Word tokenizer wrapper based on NTLK
"""
class WordTokenizeText:

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
