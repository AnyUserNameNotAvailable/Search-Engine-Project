import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import joblib  # To save/load the TF-IDF vectorizer model

# Utility functions
def write_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=2)

def load_data_from_json(json_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error loading data from {json_file}: {e}")
        return []

def delete_data_from_json(json_file):
    with open(json_file, 'w', encoding='utf-8') as file:
        file.write("[]")
    return []

# Main search function
def search_documents(query, json_data, tfidf_vectorizer):
    query_vector = tfidf_vectorizer.transform([query])
    
    # Load the trained TF-IDF vectorizer
    try:
        tfidf_vectorizer = joblib.load(vectorizer_path)
    except FileNotFoundError:
        print(f"Vectorizer model not found at {vectorizer_path}.")
        return []

    # Transform the query using the loaded TF-IDF vectorizer
    query_vector = tfidf_vectorizer.transform([query])

    # Calculate cosine similarities between the query vector and document vectors
    cosine_similarities = linear_kernel(query_vector, tfidf_vectorizer.transform([doc['title'] for doc in json_data])).flatten()

    # Get indices of sorted documents by similarity
    sorted_indices = np.argsort(cosine_similarities)[::-1]

    # Display and return the top 10 most similar documents
    for i in sorted_indices[:10]:
        print(f"Title: {json_data[i]['title']}\nURL: {json_data[i]['url']}\n")

    return [json_data[i] for i in sorted_indices[:10]] # Return the top 10 sorted documents
    # return json_data[sorted_indices[0]] # Return the first sorted document (for testing purposes)
    # return [json_data[i] for i in sorted_indices[::100]] # Return every 100th sorted document (for testing purposes)


# Example usage
json_filename = 'data.json'
vectorizer_path = 'tfidf_vectorizer.joblib'  # Ensure this path matches where you saved the vectorizer in your indexing process
json_data = load_data_from_json(json_filename)

# if json_data:
#     query = input("Enter Search Query: ")
#     search_result = search_documents(query, json_data, vectorizer_path)
#     # delete_data_from_json(json_filename)  # Delete the indexed data from the JSON file (forr testing purposes)
# else:
#     print("No data found in the JSON file.")
