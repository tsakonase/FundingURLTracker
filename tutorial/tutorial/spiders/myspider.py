import scrapy
from bs4 import BeautifulSoup
from Utils.SnippetExtractor import KeywordChecker

class TermsOfUseSpider(scrapy.Spider):
    name = "tou_spider"

    def start_requests(self):
        # provide a list of URLs
        for url in [
            "https://www.alexslemonade.org/terms-of-use"
        ]:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse (self, response):
        # try to parse the response text via BS:
        soup = None
        try:
            soup = BeautifulSoup(response.body, "html.parser")
        except:
            print ("BeautifulSoup failed to parse the response, exiting...")
            exit()

        # try to extract text from soup
        try:
            txt = soup.find_all(text=True)
            text = ' '.join([s for s in list(txt) if s.strip().strip("\n").strip()])
        except:
            print ("Failed to extract the text from HTML, exiting...")
            exit()

        # extract snippets:
        snippets = KeywordChecker().extract_snippets(text)

        # just log for now, until we know more:
        self.log("\n".join(snippets))

