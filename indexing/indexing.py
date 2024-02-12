import sys
from elasticsearch import Elasticsearch
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.insert(1,'/Users/femiadebisi/Documents/GitHub/Search Engine Project/crawler')

# Create an Elasticsearch client
es = Elasticsearch(['http://localhost:9200'], request_timeout=15)

# Set the index name
index_name = 'elasticsearch'

# Ensure the index exists
try:
    es.indices.create(index=index_name, ignore=400)
except Exception as e:
    print(f"Error creating index: {e}")
    
def index_doc(title, url):
    doc = {
        'title': title,
        'url': url
    }
    es.index(index=index_name, doc_type='_doc', body=doc)

def index_doc_with_tfidf(title, url, tfidf_values):
    doc = {
        'title': title,
        'url': url,
        'tfidf_values': tfidf_values.tolist()  # Convert numpy array to list
    }
    es.index(index=index_name, doc_type='_doc', body=doc)

# Run the crawler process
def run_crawler():
    process = CrawlerProcess(get_project_settings())
    website = input('Enter:')
    process.crawl('crawlin', start_url=f'http://{website}')
    process.start()
    # Return crawled items
    return process.crawl.items

# Function to search the index
def search(query):
    results = es.search(index=index_name, body={'query': {'match': {'title': query}}})
    return results['hits']['hits']

def calculate_tfidf_and_index():
    documents = []  # Collect all documents
    crawled_items = run_crawler()
    for item in crawled_items:
        documents.append(item['title'])

    # Create TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

    # Index documents with TF-IDF
    for i, item in enumerate(crawled_items):
        tfidf_values = tfidf_matrix[i].toarray().flatten()
        index_doc_with_tfidf(item['title'], item['url'], tfidf_values)

# Run the crawler
calculate_tfidf_and_index()

# Example search
print(search('python'))

# Close the Elasticsearch connection
es.close()
