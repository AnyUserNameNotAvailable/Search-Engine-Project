import sys, os
from flask import Flask, request, render_template, jsonify
import joblib

# Appends the directory 'indexing' folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'indexing'))

app = Flask(__name__)

# Load the saved vectorizer
vectorizer_path = 'tfidf_vectorizer.joblib'
tfidf_vectorizer = joblib.load(vectorizer_path)

# Import your search function
from searching import load_data_from_json, search_documents

app = Flask(__name__)

@app.route('/')
def index():
    # Render the main page (search form)
    return render_template('index.html')

@app.route('/search', methods=['post'])
def search():
    query = request.form.get('query')
    # Process the query using your search function
    search_results = process_query(query, tfidf_vectorizer)
    # Render the results page with the search results
    return render_template('search.html', search_results=search_results)

@app.route('/about')
def about():
    # Render the about page
    return render_template('about.html')

def process_query(query, vectorizer):
    # Load the JSON data
    json_data = load_data_from_json('data.json')
    # Search the documents
    search_results = search_documents(query, json_data, vectorizer)
    return search_results

if __name__ == '__main__':
    app.run(debug=True)
