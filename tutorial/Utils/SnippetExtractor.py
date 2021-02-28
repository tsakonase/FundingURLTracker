import unidecode
from nltk.tokenize import sent_tokenize

class KeywordChecker:

    def __init__(self):
        self.keyphrases = [
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
                    "must not reproduce"]

    def extract_snippets (self, text):
        snippets = []
        n_sents = [sent.lower() for sent in sent_tokenize(unidecode.unidecode(text))]
        for keyphrase in self.keyphrases:
            n_keyphrase = unidecode.unidecode(keyphrase).lower()
            for n_sent in n_sents:
                if n_keyphrase in n_sent:
                    snippets.append("KEYPHRASE: " + keyphrase + " is in the SENTENCE: " + n_sent)
        return snippets