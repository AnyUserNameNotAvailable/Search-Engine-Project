from flask import Blueprint, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from crawler import run_crawler
import json

search_routes = Blueprint('search_routes', __name__)
CORS(search_routes)

# JSON file to store indexed data
json_filename = 'data.json'

def write_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=2)

def read_from_json(filename):
    try:
        with open(filename, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return []

def index_doc_with_tfidf_to_json(title, url, tfidf_values):
    doc = {
        'title': title,
        'url': url,
        'tfidf_values': tfidf_values.tolist()  # Convert numpy array to list
    }
    existing_data = read_from_json(json_filename)
    existing_data.append(doc)
    write_to_json(existing_data, json_filename)

@search_routes.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    json_data = read_from_json(json_filename)
    
    # Example search in the loaded JSON data
    results = [item for item in json_data if query.lower() in item['title'].lower()]
    return jsonify(results)

def search_in_json(query, json_data):
    # Example search in the provided JSON data
    results = [item for item in json_data if query.lower() in item['title'].lower()]
    return jsonify(results)

@search_routes.route('/index', methods=['POST'])
def index():
    website = request.json.get('website')
    crawled_items = run_crawler(website)
    
    documents = []
    for item in crawled_items:
        documents.append(item['title'])

    # Create TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

    # Index documents with TF-IDF to JSON file
    for i, item in enumerate(crawled_items):
        tfidf_values = tfidf_matrix[i].toarray().flatten()
        index_doc_with_tfidf_to_json(item['title'], item['url'], tfidf_values)

    return jsonify({'message': 'Indexing successful'})

def index_in_json(crawled_items, json_data):
    documents = []
    for item in crawled_items:
        documents.append(item['title'])

    # Create TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

    # Index documents with TF-IDF to JSON data
    for i, item in enumerate(crawled_items):
        tfidf_values = tfidf_matrix[i].toarray().flatten()
        index_doc_with_tfidf_to_json(item['title'], item['url'], tfidf_values)

    return jsonify({'message': 'Indexing successful'})
