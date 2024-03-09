import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.utils.project import get_project_settings
import numpy as np

# Instantiate the TfidfVectorizer once, at the beginning of the file
tfidf_vectorizer = TfidfVectorizer(max_df=0.7)

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

def index_doc_with_tfidf_to_json(title, url, description, tfidf_values, filename):
    full_text = title + " " + description + " " + url
    doc = {
        'title': title,
        'url': url,
        'description': description,
        'tfidf_values': tfidf_values.tolist(),
        'full_text': full_text,
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

def calculate_tfidf_and_index_to_json(crawled_items, filename, tfidf_vectorizer):
    existing_data = read_from_json(filename)
    existing_texts = [doc['full_text'] for doc in existing_data]
    all_texts = existing_texts + [item['title'] + ' ' + item['description'] + ' ' + item['url'] for item in crawled_items]
    
    # Initialize existing_vectors as None
    existing_vectors = None

    # Fit the vectorizer on all texts if existing data is not empty, else fit on new texts only
    if existing_texts:
        tfidf_matrix = tfidf_vectorizer.fit_transform(all_texts)
        existing_vectors = tfidf_matrix[:len(existing_texts)]
        new_vectors = tfidf_matrix[len(existing_texts):]
    else:
        new_vectors = tfidf_vectorizer.fit_transform(all_texts)
    
    for i, item in enumerate(crawled_items):
        if existing_vectors is not None:
            # Calculate cosine similarity between the new document and existing ones
            similarity_scores = cosine_similarity(new_vectors[i], existing_vectors)
            
            # If any score exceeds the threshold, the document is considered a duplicate
            if any(score[0] > 0.8 for score in similarity_scores):  # similarity_threshold = 0.8
                print(f"Duplicate document detected: {item['title']}")
                continue
        
        # If the document is not a duplicate, index it
        tfidf_values = new_vectors[i].toarray().flatten()
        index_doc_with_tfidf_to_json(item['title'], item['url'], item['description'], tfidf_values, filename)
        print(f"Indexed {item['title']} to JSON file")

    # Save the TF-IDF vectorizer to a file
    joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer.joblib')

# Set the JSON filename and website URL
json_filename = 'data.json'
website_url = input('Enter website URL: ')
crawled_items = run_crawler(start_url=f'http://{website_url}')
calculate_tfidf_and_index_to_json(crawled_items, json_filename, tfidf_vectorizer)
