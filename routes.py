from flask import Flask, request, jsonify
import joblib  # Import joblib for loading the saved vectorizer

app = Flask(__name__)

# Load the saved vectorizer (adjust the path as needed)
vectorizer_path = 'path/to/save/tfidf_vectorizer.joblib'
tfidf_vectorizer = joblib.load(vectorizer_path)

from searching import load_data_from_json, search_documents 

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    json_data = load_data_from_json('data.json')
    search_results = search_documents(query, json_data, tfidf_vectorizer)  # Pass the loaded vectorizer to your search function
    
    # Return the search results as JSON
    return jsonify({'results': search_results})
