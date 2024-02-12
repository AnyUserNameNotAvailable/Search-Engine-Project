from flask import Blueprint, request, jsonify
from elasticsearch import Elasticsearch

search_routes = Blueprint('search_routes', __name__)

# create elasticsearch client
es = Elasticsearch(['http://localhost:9200'], request_timeout=15)
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
    

@search_routes.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    results = es.search(index=index_name, body={'query': {'multi_match': {'query': query, 'fields': ['title', 'description']}}})
    return jsonify(results['hits']['hits'])

def search_in_elasticsearch(query):
    results = es.search(index=index_name, body={'query': {'multi_match': {'query': query, 'fields': ['title', 'description']}}})
    return jsonify(results['hits']['hits'])