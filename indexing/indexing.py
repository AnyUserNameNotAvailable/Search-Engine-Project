import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.utils.project import get_project_settings
import numpy as np

# Instantiate the TfidfVectorizer once, at the beginning of the file
tfidf_vectorizer = TfidfVectorizer(max_df=0.5)

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

def delete_data_from_json(json_file):
    with open(json_file, 'w', encoding='utf-8') as file:
        file.write("[]")
    return []


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


def calculate_tfidf_and_index_to_json(documents, filename, tfidf_vectorizer):
    # Use the passed-in TF-IDF vectorizer
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

    # Index documents with TF-IDF to JSON file
    for i, item in enumerate(crawled_items):
        tfidf_values = tfidf_matrix[i].toarray().flatten()
        index_doc_with_tfidf_to_json(item['title'], item['url'], tfidf_values, filename)
        print(f"Indexed {item['title']} to JSON file")

    # Save the TF-IDF vectorizer to a file
    joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer.joblib')
    return tfidf_vectorizer, tfidf_matrix  # Return vectorizer and matrix


# Set the JSON filename and website URL
json_filename = 'data.json'

website_url = input('Enter website URL: ')
crawled_items = run_crawler(start_url=f'http://{website_url}')
# Pass the tfidf_vectorizer as an argument to the function
tfidf_vectorizer, tfidf_matrix = calculate_tfidf_and_index_to_json(documents=[item['title'] for item in crawled_items], filename=json_filename, tfidf_vectorizer=tfidf_vectorizer)
