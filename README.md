# Search-Engine-Project
Small Scale Search Engine with following steps

Scope:
general search

Web Crawling:
    Web crawler to fetch web pages. using Scrapy and BeautifulSoup

indexing.py:
    Responsibility: This file contains functions related to the indexing process. It is responsible for writing and reading data to/from a JSON file, running the web crawler to fetch data from a website, and performing TF-IDF indexing on the extracted data.
    Functions:
    write_to_json and read_from_json: Handle writing data to and reading data from a JSON file.
    load_data_from_json: Load data from a JSON file.
    index_doc_with_tfidf_to_json: Index a document by calculating TF-IDF values and storing the result in a JSON file.
    run_crawler: Run the web crawler to fetch data from a specified website.
    calculate_tfidf_and_index_to_json: Calculate TF-IDF values for documents and index them to a JSON file.
    Usage: It is used for the backend processes involved in indexing, such as running the crawler, calculating TF-IDF values, and storing the indexed data.
searching.py:
    Responsibility:
    This file contains functions related to the searching process.
    Functions:
    read write and delete from json
    search documents
routes.py:
    Responsibility: This file defines the routes (endpoints) of your Flask web application. It handles incoming HTTP requests and defines the behavior of the web application.
    Endpoints:
    home
    about
    search 
Templates:
Index:
    Main page for search engine
About:
    an about page that describes project to potential users
Results:
    results page that dynamically loads content from data.json based on search query.
