import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import joblib  # To save/load the TF-IDF vectorizer model
from fuzzywuzzy import fuzz
from nltk.corpus import wordnet as wn

import nltk
nltk.download('wordnet')

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

def get_synonyms(word):
    synonyms = set()

    for synset in wn.synsets(word):
        for lemma in synset.lemmas():
            synonyms.add(lemma.name())
    
    return list(synonyms)

def expand_query_with_synonyms(query):
    expanded_query = []
    for word in query.split():
        # Get synonyms for the word
        synonyms = get_synonyms(word)
        # Add the original word and its synonyms to the expanded query
        expanded_query.append(word)
        expanded_query.extend(synonyms)
    # Join the expanded query terms into a single string
    return ' '.join(expanded_query)

# Main search function
def search_documents(query, json_data, tfidf_vectorizer):
    expanded_query = expand_query_with_synonyms(query)
    
    # Load the trained TF-IDF vectorizer
    try:
        tfidf_vectorizer = joblib.load(vectorizer_path)
    except FileNotFoundError:
        print(f"Vectorizer model not found at {vectorizer_path}.")
        return []

    # Transform the query using the loaded TF-IDF vectorizer
    query_vector = tfidf_vectorizer.transform([expanded_query])

    # Calculate cosine similarities between the query vector and document vectors
    cosine_similarities = linear_kernel(query_vector, tfidf_vectorizer.transform([doc['full_text'] for doc in json_data])).flatten()

    # Initialize a list to store combined scores
    combined_scores = []

    # Compute combined scores using both cosine similarity and fuzzy match score
    for i, doc in enumerate(json_data):
        # Compute fuzzy match score
        fuzzy_score = fuzz.ratio(query.lower(), doc['full_text'].lower()) / 100.0  # Normalize score to be between 0 and 1

        # Combine cosine similarity and fuzzy match score (simple average for this example)
        combined_score = (cosine_similarities[i] + fuzzy_score) / 2
        combined_scores.append((combined_score, i))

    # Sort documents by combined score in descending order
    combined_scores.sort(reverse=True)

    # Display and return the top 10 most similar documents based on combined score
    for score, i in combined_scores[:10]:
        print(f"Title: {json_data[i]['title']}\nDescription: {json_data[i]['description']}\nURL: {json_data[i]['url']}\n")

    return [json_data[i] for _, i in combined_scores[:10]]  # Return the top 10 sorted documents based on combined score
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
