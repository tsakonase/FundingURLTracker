import scrapy
import pandas as pd
from string import punctuation

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        data = pd.read_excel("/Users/tsakonase/tutorial/tutorial/spiders/Training - Data G&F - Only URLs - SS and MM.xlsx")
        toU_URL_col = data[data['ToU (Terms of Use should refer to copyright/reuse of data) URL'].notnull()]

        urls = list(toU_URL_col['ToU (Terms of Use should refer to copyright/reuse of data) URL'])

        for url in urls[:2]:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse (self, response):
        page = ''.join(c for c in ''.join(response.url.split("/")) if c != ' ' and c not in punctuation)
        filename = f'/Users/tsakonase/tutorial/tutorial/spiders/Results/ToU-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')


# # # GEOGRAFICAL ENTITY: Q27096213
# # Q8502 --> mountain
# # Q813672 --> basin
# # Q820477 --> mine
# # Q47089 --> fault (geology)
#
#
# from SPARQLWrapper import SPARQLWrapper, JSON
#
# sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
#
# QUERY = """
# SELECT DISTINCT ?item ?name ?coord ?lat ?lon ?globe
# {
#    ?item wdt:P31 wd:Q820477 ;
#          p:P625 [
#            psv:P625 [
#              wikibase:geoLatitude ?lat ;
#              wikibase:geoLongitude ?lon ;
#              wikibase:geoGlobe ?globe ;
#            ] ;
#            ps:P625 ?coord
#          ]
#   FILTER ( ?globe = wd:Q2 )
#   SERVICE wikibase:label {
#     bd:serviceParam wikibase:language "en" .
#     ?item rdfs:label ?name
#    }
# }
# LIMIT 100000
# """
#
# QUERY2 = """
#
# SELECT ?s ?desc WHERE {
#
# ?s wdt:P279+ wd:Q27096213 .
#
# OPTIONAL {
#
# ?s rdfs:label ?desc filter (lang(?desc) = "en").
#
# }
#
# }
#
# """
#
# sparql.setQuery(QUERY2)
# sparql.setReturnFormat(JSON)
#
# results = sparql.query().convert()
#
# import json
# with open("./file.txt", "w") as json_file:
#     for res in results['results']['bindings']:
#         json_file.write(json.dumps(res))

