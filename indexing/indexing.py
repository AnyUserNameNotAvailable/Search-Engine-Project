import sys
sys.path.insert( 1,'/Users/femiadebisi/Documents/GitHub/Search Engine Project/crawler')

from elasticsearch import Elasticsearch
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Create an Elasticsearch client

es = Elasticsearch(['http://localhost:9200'], timeout=15)

# Set the index name
index_name = 'elasticsearch'

# Ensure the index exists
try:
    es.indices.create(index=index_name, ignore=400)
except Exception as e:
    print(f"Error creating index: {e}")

# Function to index a document
def index_doc(title, url):
    doc = {
        'title': title,
        'url': url
    }
    es.index(index=index_name, doc_type='_doc', body=doc)

# Run the crawler process
def run_crawler():
    process = CrawlerProcess(get_project_settings())
    website = input('Enter:')
    process.crawl('crawlin', start_url=f'http://{website}')
    process.start()

# Function to search the index
def search(query):
    results = es.search(index=index_name, body={'query': {'match': {'title': query}}})
    return results['hits']['hits']

# Run the crawler
crawled_items = run_crawler()
for item in crawled_items:
    index_doc(item['title'], item['url'])
    

# Example search
print(search('python'))

# Close the Elasticsearch connection
es.close()

