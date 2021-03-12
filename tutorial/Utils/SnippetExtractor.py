import unidecode
from nltk.tokenize import sent_tokenize
from intervaltree import IntervalTree, Interval
import re
from collections import defaultdict
from .Tokenizers import WordTokenizeText

class KeywordChecker:

    def __init__(self):

        self.tokenizer = WordTokenizeText()
        self.keyphrases = [
                            'you must not scrape',
                            'you must not data mining',
                            'data mining tools, robots',
                            'robot, spider or any other automated device or process',
                            'must not conduct any systematic or automated data collection activities',
                            'not use any bot, crawler, harvester, indexer, robot, spider, scraper or any other automated means',
                            'allow to reuse',
                            'public domain',
                            'public sector information',
                            'CC BY',
                            'CC0',
                            'CC BY-SA',
                            'CC BY-NC',
                            'CC BY-NC-SA',
                            'CC BY-ND',
                            'CC BY-NC-ND',
                            'OGL',
                            'without the written permission',
                            'without permission',
                            'prior consent',
                            'prior written consent',
                            'prior written permission',
                            'prior non-electronic consent',
                            'express written permission',
                            'request permission',
                            'rights reserved',
                            'commercial purposes',
                            'commercial use',
                            'commercial reproduction',
                            'non-commercial',
                            'noncommercial',
                            'personal use',
                            'reproduce for personal use',
                            'reproduction is prohibited',
                            'you must not reproduce',
                            'intellectual property',
                            'Creative Commons',
                            'Attribution',
                            'obligation',
                            'Usage of Content',
                            'web crawlers',
                            'User reverse, engineer, disassemble, decompile, reproduce',
                            'Attribution, Government Works, may be freely used',
                            'can be used without restriction',
                            'CC-BY',
                            'CC-BY-NC',
                            'CC-BY-NC-ND',
                            'CC-BY-NC-SA',
                            'CC-BY-ND',
                            'CC-BY-SA',
                            'copy',
                            'copyright',
                            'copyright free',
                            'Creative Commons Attribution',
                            'Creative Commons Attribution-NonCommercial',
                            'free of copyright, reuse',
                            'noncommercial use, requests for personal website use',
                            'open government licence',
                            'prior consent, intellectual property rights, personal use',
                            'public information',
                            'public information, may be distributed',
                            'public information, may be distributed or copied',
                            'public service, may be distributed',
                            'public use',
                            'public use, U.S. Government',
                            're-use',
                            're-use, government information, free of rights',
                            'United States government',
                            'without prior written permission',
                            'Urheberrechte',
                            'Urheberrecht',
                            'urheberrechtlich',
                            'geistigen Eigentums',
                            'kommerzielle Zwecke',
                            'propiedad intelectual',
                            'propiedad industrial',
                            'derechos de autor',
                            'información es pública',
                            'derechos reservados',
                            'Intellectuele eigendomsrechten',
                            'persoonlijk gebruik',
                            'auteursrecht',
                            'toestemming vereist'
                            ]

    def extract_snippets (self, text):
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
                concat_keywords = ', '.join(list(set([item[0] for item in d[n_sent]])))
                g_snippets.append((sent, concat_keywords))

        return snippets
