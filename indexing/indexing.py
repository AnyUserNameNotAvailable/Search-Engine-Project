import json
from sklearn.feature_extraction.text import TfidfVectorizer
from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.utils.project import get_project_settings


def write_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=2)

def read_from_json(filename):
    try:
        with open(filename, 'r') as json_file:
            return json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Handle the case where the file is not found or cannot be parsed as JSON
        print(f"Error reading {filename}.")
        return []

def index_doc_with_tfidf_to_json(title, url, tfidf_values, filename):
    doc = {
        'title': title,
        'url': url,
        'tfidf_values': tfidf_values.tolist()  # Convert numpy array to list
    }
    existing_data = read_from_json(filename)
    existing_data.append(doc)
    write_to_json(existing_data, filename)

def run_crawler():
    crawled_items = []  # Initialize an empty list to store crawled items

    def crawler_results(item, response, spider):
        crawled_items.append(item)

    process = CrawlerProcess(get_project_settings())
    website = input('Enter:')
    crawler = process.create_crawler('crawlin')
    
    # Connect the crawler_results function to the signals
    crawler.signals.connect(crawler_results, signal=signals.item_scraped)
    
    process.crawl(crawler, start_url=f'http://{website}')
    process.start()
    process.join()
    
    return crawled_items  # Return the list of crawled items
    
def calculate_tfidf_and_index_to_json(filename):
    crawled_items = run_crawler()
    documents = [item['title'] for item in crawled_items]
    
    # debuging print documents for inspection
    # print("Documents before TF-IDF vectorization:")
    # print(documents)

    # Create TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer(max_df=0.5)
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

    # Index documents with TF-IDF to JSON file
    for i, item in enumerate(crawled_items):
        tfidf_values = tfidf_matrix[i].toarray().flatten()
        index_doc_with_tfidf_to_json(item['title'], item['url'], tfidf_values, filename)
        print(f"Indexed {item['title']} to JSON file")

# Run the crawler and index to JSON file
json_filename = 'data.json'
calculate_tfidf_and_index_to_json(json_filename)

# Example search in the loaded JSON data
json_data = read_from_json(json_filename)
search_result = [item for item in json_data if 'python' in item['title'].lower()]
print(search_result)
