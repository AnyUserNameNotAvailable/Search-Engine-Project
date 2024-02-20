from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from scrapy import Item, Field

class MyItem(Item):
    title = Field()
    url = Field()

class CrawlingSpider(CrawlSpider):
    name = 'crawlin'
    allowed_domains = []  # allow any domain
    USER_AGENT = 'MyCrawlerBot (+http://www.example.com)'
    custom_settings = {
        'DOWNLOAD_DELAY': 0.1,  # Add a delay between requests
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_ITEMS' :1,
        'CLOSESPIDER_PAGECOUNT': 1,
        'CLOSESPIDER_ITEMCOUNT': 10
    }

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def __init__(self, *args, **kwargs):
        super(CrawlingSpider, self).__init__(*args, **kwargs)

        # Get the start URL from the command line arguments
        self.start_urls = [kwargs.get('start_url', 'http://www.example.com/')]

    def parse_item(self, response):
        item = MyItem()
        raw_title = response.css('title::text').get()
        url = response.url  # Extract the URL

        # clean title
        cleaned_title = self.clean_text(raw_title)

        # Assign the cleaned title and URL to the 'title' and 'url' fields in the item instance
        item['title'] = cleaned_title
        item['url'] = url

        # Print or log the title and URL
        self.logger.info(f'Title: {item["title"]}, URL: {item["url"]}')

        yield item

    def clean_text(self, text):
        # Remove HTML tags
        soup = BeautifulSoup(text, 'html.parser')
        text = soup.get_text()

        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))

        # Convert to lowercase
        text = text.lower()

        # Remove stop words
        stop_words = set(stopwords.words('english'))
        words = [word for word in text.split() if word.lower() not in stop_words]

        # Stem words
        stemmer = PorterStemmer()
        words = [stemmer.stem(word) for word in words]

        # Join words back into a string
        text = ' '.join(words)

        return text
