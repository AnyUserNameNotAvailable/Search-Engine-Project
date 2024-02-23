import json
from sklearn.feature_extraction.text import TfidfVectorizer
from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.utils.project import get_project_settings
import numpy as np


def write_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=2)


def read_from_json(filename):
    try:
        with open(filename, 'r') as json_file:
            return json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error reading {filename}.")
        return []


def load_data_from_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def index_doc_with_tfidf_to_json(title, url, tfidf_values, filename):
    doc = {
        'title': title,
        'url': url,
        'tfidf_values': tfidf_values.tolist()
    }
    existing_data = read_from_json(filename)
    existing_data.append(doc)
    write_to_json(existing_data, filename)


def run_crawler(start_url):
    crawled_items = []

    def crawler_results(item, response, spider):
        crawled_items.append(item)

    process = CrawlerProcess(get_project_settings())
    crawler = process.create_crawler('crawlin')

    crawler.signals.connect(crawler_results, signal=signals.item_scraped)

    process.crawl(crawler, start_url=start_url)
    process.start()
    process.join()

    return crawled_items


def calculate_tfidf_and_index_to_json(documents, filename):
    # Create TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer(max_df=0.5)
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

    # Index documents with TF-IDF to JSON file
    for i, item in enumerate(crawled_items):
        tfidf_values = tfidf_matrix[i].toarray().flatten()
        index_doc_with_tfidf_to_json(item['title'], item['url'], tfidf_values, filename)
        print(f"Indexed {item['title']} to JSON file")

    return tfidf_vectorizer, tfidf_matrix  # Return vectorizer and matrix


# Search documents
def search_documents(query, json_data):
    query_vector = np.array([0.0] * len(json_data[0]['tfidf_values']))  # Initialize query vector
    for term in query.split():
        if term in json_data[0]['tfidf_values']:
            query_vector += np.array(json_data[0]['tfidf_values'][term])

    # Calculate cosine similarities
    cosine_similarities = [np.dot(query_vector, doc['tfidf_values']) for doc in json_data]

    # Get indices of sorted similarities
    sorted_indices = np.argsort(cosine_similarities)[::-1]
    
    for i in sorted_indices[:10]:
        print(f"Title: {json_data[i]['title']}\nURL: {json_data[i]['url']}\n")

    return [json_data[i] for i in sorted_indices[:10]]  # Return the top 10 sorted documents
    # return [json_data[i] for i in sorted_indices[:10]]  # Return the top 10 sorted documents
    # return [json_data[i] for i in sorted_indices[-10:]]  # Return the bottom 10 sorted documents
    # return [json_data[i] for i in sorted_indices[::10]]  # Return the every 10th sorted document
    # return [json_data[i] for i in sorted_indices[::100]]  # Return the every 100th sorted document
    # return [json_data[i] for i in sorted_indices[::1000]]  # Return the every 1000th sorted document


# Set the JSON filename and website URL
json_filename = 'data.json'

# Example search in the loaded JSON data
query = input("Enter Search Query: ")

# Load data from JSON
json_data = load_data_from_json(json_filename)

# Perform search
search_result = search_documents(query, json_data)


website_url = input('Enter website URL: ')
crawled_items = run_crawler(start_url=f'http://{website_url}')
tfidf_vectorizer, tfidf_matrix = calculate_tfidf_and_index_to_json(documents=[item['title'] for item in crawled_items], filename=json_filename)


