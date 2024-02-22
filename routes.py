from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from scrapy.crawler import CrawlerProcess
import json
import numpy as np
from indexing import search_documents


app = Flask(__name__)

# json file storing indexed data
json_file = 'data.json'

# json functions
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


@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    json_data = load_data_from_json('data.json')
    search_results = search_documents(query, json_data)
    
    # Return the search results as JSON
    return jsonify({'results': search_results})


@app.route('/index', methods=['POST'])
def index():
    # Load indexed data from JSON file
    data = load_data_from_json(json_file)

    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform the indexed documents
    tfidf_values = vectorizer.fit_transform([doc['title'] for doc in data])

    # Index each document with its title, URL, and TF-IDF values
    for i, doc in enumerate(data):
        index_doc_with_tfidf_to_json(doc['title'], doc['url'], tfidf_values[i], json_file)

    return jsonify({'message': 'Indexing complete'})
