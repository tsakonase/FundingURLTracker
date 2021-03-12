import scrapy
from bs4 import BeautifulSoup
from Utils.SnippetExtractor import KeywordChecker

class TermsOfUseSpider(scrapy.Spider):
    name = "tou_spider"

    def start_requests(self):

        ## provide a list of URLs
        #for url in [
        #    "https://www.alexslemonade.org/terms-of-use"
        #]:

        # or, read the URL from command line:
        url = getattr(self, 'url', None)
        if url is not None:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse (self, response):
        # try to parse the response text via BS:
        soup = None
        try:
            soup = BeautifulSoup(response.body, "html.parser")
        except:
            print ("BeautifulSoup failed to parse the response, exiting...")
            exit()

        text = None
        # try to extract text from soup
        try:
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()  # rip it out
            # get text
            text = soup.get_text()
            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = [phrase.strip() for line in lines for phrase in line.split("  ")]
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
        except:
            print ("Failed to extract the text from HTML, exiting...")
            exit()

        # extract snippets:
        snippets = KeywordChecker().extract_snippets(text)

        yield {"output": snippets}
