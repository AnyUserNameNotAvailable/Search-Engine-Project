from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import string
from nltk.corpus import stopwords
from scrapy import Item, Field

class MyItem(Item):
    title = Field()
    url = Field()
    description = Field()

class CrawlingSpider(CrawlSpider):
    name = 'crawlin'
    allowed_domains = []  # allow any domain
    USER_AGENT = 'MyCrawlerBot (+http://www.example.com)'
    custom_settings = {
        'DOWNLOAD_DELAY': 0.2,  # Add a delay between requests
        'CLOSESPIDER_ITEMCOUNT': 100,  # Stop crawling after 10 pages
        'ROBOTSTXT_OBEY': True
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
        description = response.css('p::text').get()  # Extract the description text

        # clean title
        cleaned_title = self.clean_text(raw_title)
        cleaned_description = self.clean_text(description)

        # Assign the cleaned title and URL to the 'title' and 'url' fields in the item instance
        item['title'] = cleaned_title
        item['url'] = url
        item['description'] = cleaned_description  # Add the cleaned description to the item instance
        

        # Print or log the title and URL
        self.logger.info(f'Title: {item["title"]}, URL: {item["url"]}')

        yield item

    def clean_text(self, text):
        if text is None:
            return ''
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

        return text
