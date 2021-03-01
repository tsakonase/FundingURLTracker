import unidecode
from nltk.tokenize import sent_tokenize
from intervaltree import IntervalTree, Interval
import re

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

                    "non-commercial",
                    "commercial purposes",
                    "commercial use",

                    "must not reproduce",
                    "reproduce for personal use",

                    "personal use",
                    "reproduction is prohibited",
                    ]

    def extract_snippets (self, text):

        snippets = []
        n_sents = [sent.lower() for sent in sent_tokenize(unidecode.unidecode(text))]
        for n_sent in n_sents:
            t = IntervalTree()
            for keyphrase in self.keyphrases:
                n_keyphrase = unidecode.unidecode(keyphrase).lower()
                for match in re.finditer(n_keyphrase, n_sent):
                    s = match.start()
                    e = match.end()
                    if t.overlap(s, e) and not t.envelop(s, e):
                        continue
                    elif t.overlap(s, e) and t.envelop(s, e):
                        t.remove_envelop(s, e)
                    else:
                        t[s:e] = (keyphrase, n_sent)
            snippets.extend(list(set([mykey[-1] for mykey in t])))
        #for keyphrase in self.keyphrases:
        #    n_keyphrase = unidecode.unidecode(keyphrase).lower()
        #    for n_sent in n_sents:
        #        if n_keyphrase in n_sent:
        #            snippets.append("ALOHA: " + keyphrase + " is in the SENTENCE: " + n_sent)
        return snippets
