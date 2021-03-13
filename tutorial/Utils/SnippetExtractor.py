import unidecode
from nltk.tokenize import sent_tokenize
from intervaltree import IntervalTree
import re
import string
from collections import defaultdict
from .Tokenizers import WordTokenizeText


class KeywordChecker:

    def __init__(self, previous_snippets=None):

        self.tokenizer = WordTokenizeText()
        self.translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))

        self.previous_snippets = previous_snippets
        self.keyphrases = [
                            'you must not scrape', 'you must not data mining', 'data mining tools, robots',
                            'robot, spider or any other automated device or process',
                            'must not conduct any systematic or automated data collection activities',
                            'not use any bot, crawler, harvester, indexer, robot, spider, scraper or any other automated means',
                            'allow to reuse', 'public domain', 'public sector information',
                            'CC BY', 'CC0', 'CC BY-SA', 'CC BY-NC', 'CC BY-NC-SA', 'CC BY-ND', 'CC BY-NC-ND', 'OGL',
                            'without the written permission', 'without permission', 'prior consent', 'prior written consent',
                            'prior written permission', 'prior non-electronic consent',
                            'express written permission', 'request permission', 'rights reserved', 'commercial purposes',
                            'commercial use', 'commercial reproduction', 'non-commercial', 'noncommercial', 'personal use',
                            'reproduce for personal use', 'reproduction is prohibited', 'you must not reproduce',
                            'intellectual property', 'Creative Commons', 'Attribution', 'obligation', 'Usage of Content',
                            'web crawlers', 'User reverse, engineer, disassemble, decompile, reproduce',
                            'Attribution, Government Works, may be freely used',
                            'can be used without restriction', 'CC-BY', 'CC-BY-NC', 'CC-BY-NC-ND', 'CC-BY-NC-SA',
                            'CC-BY-ND', 'CC-BY-SA', 'copy', 'copyright', 'copyright free',
                            'Creative Commons Attribution', 'Creative Commons Attribution-NonCommercial',
                            'free of copyright, reuse', 'noncommercial use, requests for personal website use',
                            'open government licence', 'prior consent, intellectual property rights, personal use',
                            'public information', 'public information, may be distributed',
                            'public information, may be distributed or copied', 'public service, may be distributed',
                            'public use', 'public use, U.S. Government',
                            're-use', 're-use, government information, free of rights',
                            'United States government', 'without prior written permission',
                            'Urheberrechte', 'Urheberrecht',
                            'urheberrechtlich', 'geistigen Eigentums',
                            'kommerzielle Zwecke', 'propiedad intelectual', 'propiedad industrial',
                            'derechos de autor', 'información es pública',
                            'derechos reservados', 'Intellectuele eigendomsrechten', 'persoonlijk gebruik', 'auteursrecht',
                            'toestemming vereist'
                          ]


    # functions to compute similarity of text fragments:
    def kshingles(self, mystring, k=5):
        return [mystring[i:i + k] for i in range(len(mystring) - k + 1)]

    def jaccard_similarity(self, list1, list2):
        s1 = set(list1)
        s2 = set(list2)
        return float(len(s1.intersection(s2)) / len(s1.union(s2)))

    # function to extract the text fragments via keyword-based matching:
    def extract_snippets (self, text, comparator=False):
        snippets = []
        d = defaultdict(list)

        n_sents = [(sent, " ".join(self.tokenizer.word_tokenize(sent, remove_punct=True,
                                                    remove_stopwords=False, stem_words=False, purge_token_punct=True)))
                   for sent in sent_tokenize(unidecode.unidecode(text))]

        for idx, (sent, n_sent) in enumerate(n_sents):
            t = IntervalTree()

            for keyphrase in self.keyphrases:
                n_keyphrase = " ".join(self.tokenizer.word_tokenize(keyphrase, remove_punct=True,
                                                               remove_stopwords=False, stem_words=False,
                                                               purge_token_punct=True))
                pattern = re.compile(r'\b' + re.escape(n_keyphrase) + r'(\b|[,;.!?]|\s)', re.IGNORECASE)
                for match in list(pattern.finditer(n_sent)):
                    s = match.start()
                    e = match.end()
                    if t.envelop(s, e):
                        t.remove_envelop(s, e)
                    t[s:e] = (keyphrase, sent, n_sent, idx)

            # keep a dictionary:
            if not t:
                d[n_sent].append(["NK", idx])
                continue

            for s, e, (_key, my_sent, my_n_sent, id_s) in t:
                d[my_n_sent].append([_key, id_s])

        # group snippets:
        g_snippets = []
        for idx, (sent, n_sent) in enumerate(n_sents):
            if "NK" in d[n_sent][0]:
                if g_snippets: snippets.append(g_snippets)
                g_snippets = []
            else:
                concat_keywords = list(set([item[0] for item in d[n_sent]]))
                g_snippets.append((sent, concat_keywords))

        # compare previous year if those are provided and return:
        results = []
        for g_snippet in snippets:
            g_text = "\n".join([sent for sent, mykeys in g_snippet])
            s_keywords = set([])
            for sent, mykeys in g_snippet:
                s_keywords = s_keywords | set(mykeys)
            g_keywords = ', '.join(list(s_keywords))

            """
            # normalize and find the closest prev_snippet (in jaccard similarity), then remove it:
            n_snippet = ''.join(unidecode.unidecode(g_text.translate(translator).lower()).split())
            MAX_SIM = -1
            best_id = None
            if self.previous_snippets:
                for idx, prev_snippet in enumerate(self.previous_snippets):
                    n_prev_snippet = ''.join(unidecode.unidecode(prev_snippet.translate(translator).lower()).split())
                    _sim = jaccard_similarity(kshingles(n_snippet), kshingles(n_prev_snippet))
                    if _sim > MAX_SIM:
                        MAX_SIM = _sim
                        best_id = idx
                del self.previous_snippets[best_id]
            """

            results.append((g_text, g_keywords))

        similarity_previous = -1
        if self.previous_snippets:
            curr_text = " ".join([g_snp for g_snp, g_keys in results])
            prev_text = " ".join(self.previous_snippets)

            n_curr_text = ''.join(unidecode.unidecode(curr_text.translate(self.translator).lower()).split())
            n_prev_text = ''.join(unidecode.unidecode(prev_text.translate(self.translator).lower()).split())

            similarity_previous = self.jaccard_similarity(self.kshingles(n_curr_text), self.kshingles(n_prev_text))

        return results, similarity_previous

