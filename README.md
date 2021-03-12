# FundingURLTracker

Based on Scrapy and NLTK. 

## Development:

Providing a URL extract snippets pertaining to specific keywords related to Terms of Use.
In this rudimentary version of the service, the snippets are extracted through NLTK sentence
tokenizer and basic regex keyword matchiing.

### How to run the code:
- Git clone the repository and  install dependencies via ```pip3 install requirements.txt``` 
- Run from terminal ```scrapy crawl tou_spider -a url=<url> -o ./ResultSnippets/output.json```

