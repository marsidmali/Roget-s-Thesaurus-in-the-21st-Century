from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import json
import os
"""
Author: Marsid Mali
Date: 2024-02-20
Description: This script is designed to fetch embeddings for a set of terms using the specified model, with functionality to handle rate limiting and store the results in manageable chunks. It leverages concurrent execution to efficiently process batches of terms. The script includes two key functions for managing embeddings:
1. `store_embeddings_in_chunks` which stores the embeddings in smaller JSON files to manage file size and facilitate easier data handling.
2. `read_embeddings` which loads embeddings from multiple JSON files and combines them into a single map for further processing or analysis.

Dependencies: concurrent.futures, time, json, os
"""


def get_embeddings(client, batch, model="text-embedding-3-large"):
    """
    Fetches embeddings for a batch of terms from the specified model.

    :param client: The client object used to interact with the embeddings API.
    :param batch: A list of terms to fetch embeddings for.
    :param model: The model identifier to use for fetching embeddings. Defaults to 'text-embedding-3-large'.
    :return: A list of tuples, where each tuple contains a term and its corresponding embedding.
    """
    embeddings = client.embeddings.create(input=batch, model=model).data
    return [(term, embedding.embedding) for term, embedding in zip(batch, embeddings)]


def fetch_embeddings_with_rate_limit(client, unique_terms, model="text-embedding-3-large", requests_per_minute=2900, batch_size=100):
    """
    Fetches embeddings for a set of terms with rate limiting to avoid exceeding API limits.

    :param client: The client object used to interact with the embeddings API.
    :param unique_terms: A list of unique terms to fetch embeddings for.
    :param model: The model identifier to use for fetching embeddings. Defaults to 'text-embedding-3-large'.
    :param requests_per_minute: The maximum number of requests allowed per minute. Defaults to 2900.
    :param batch_size: The number of terms to fetch in each batch. Defaults to 100.
    :return: A dictionary mapping terms to their embeddings.
    """
    max_workers = 40
    request_interval = 60 / requests_per_minute
    term_embedding_map = {}

    def worker(batch):
        time.sleep(request_interval)
        return get_embeddings(client, batch, model)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Split terms into batches
        batches = [unique_terms[i:i + batch_size] for i in range(0, len(unique_terms), batch_size)]
        futures = [executor.submit(worker, batch) for batch in batches]
        for future in as_completed(futures):
            results = future.result()
            for term, embedding in results:
                term_embedding_map[term] = embedding

    return term_embedding_map


def store_embeddings_in_chunks(term_embedding_map, chunk_size=477, directory='embeddings'):
    """
    Stores the embeddings in smaller JSON files.
    :param term_embedding_map: The map of term embeddings to store.
    :param chunk_size: The size of each chunk.
    :param directory: The directory where to store the files.
    """
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    # Split the map into chunks
    items = list(term_embedding_map.items())
    for i in range(0, len(items), chunk_size):
        chunk = dict(items[i:i+chunk_size])
        with open(f'{directory}/embeddings_chunk_{i//chunk_size}.json', 'w') as file:
            json.dump(chunk, file)


def read_embeddings(directory='embeddings'):
    """
    Loads embeddings from multiple JSON files and combines them into a single map.
    :param directory: The directory from which to load the files.
    :return: The combined map of term embeddings.
    """
    combined_map = {}
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(f'{directory}/{filename}', 'r') as file:
                data = json.load(file)
                combined_map.update(data)
    return combined_map




