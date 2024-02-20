import json
from sklearn.feature_extraction.text import TfidfVectorizer
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def write_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=2)

def read_from_json(filename):
    try:
        with open(filename, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return []

def index_doc_with_tfidf_to_json(title, url, tfidf_values, filename):
    doc = {
        'title': title,
        'url': url,
        'tfidf_values': tfidf_values.tolist()  # Convert numpy array to list
    }
    existing_data = read_from_json(filename)
    existing_data.append(doc)
    write_to_json(existing_data, filename)

def run_crawler():
    process = CrawlerProcess(get_project_settings())
    website = input('Enter:')
    process.crawl('crawlin', start_url=f'http://{website}')
    process.start()
    process.join()
    
    return process.crawl.get_output()

def calculate_tfidf_and_index_to_json(filename):
    documents = []  # Collect all documents
    crawled_items = run_crawler()
    for item in crawled_items:
        documents.append(item['title'])

    # Create TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

    # Index documents with TF-IDF to JSON file
    for i, item in enumerate(crawled_items):
        tfidf_values = tfidf_matrix[i].toarray().flatten()
        index_doc_with_tfidf_to_json(item['title'], item['url'], tfidf_values, filename)

# Run the crawler and index to JSON file
json_filename = 'data.json'
calculate_tfidf_and_index_to_json(json_filename)

# Example search in the loaded JSON data
json_data = read_from_json(json_filename)
search_result = [item for item in json_data if 'python' in item['title'].lower()]
print(search_result)
