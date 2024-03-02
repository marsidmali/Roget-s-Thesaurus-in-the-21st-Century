# Thesaurus Data Processing Utilities 

## Overview

The utility scripts, `thesaurus_parser.py` and `parallelized_embeddings_fetcher.py`, form a comprehensive toolkit designed for the processing and analysis of Roget's Thesaurus. These scripts facilitate the structured parsing, cleaning, categorization, and embedding retrieval for terms within the Thesaurus, leveraging advanced programming techniques to handle large datasets efficiently.

- `thesaurus_parser.py` focuses on transforming raw textual data from Roget's Thesaurus into a structured format, enabling further analysis. It employs precise string manipulation to extract and clean terms according to their hierarchical categorization within the Thesaurus.

- `parallelized_embeddings_fetcher.py` addresses the subsequent step of fetching word embeddings for the cleaned and structured terms. It utilizes concurrent execution to efficiently manage API rate limits and batch processing, ensuring an optimized retrieval of embeddings. The script also includes functionality for chunk-wise storage and retrieval of embedding data, facilitating easier handling of large volumes of data.

## Scripts Descriptions

### `thesaurus_parser.py`

This Python script tackles the challenge of parsing a complex dataset, where textual lines must be accurately interpreted and categorized. Given the nuanced structure of Roget's Thesaurus, which includes hierarchical classifications such as classes, divisions, and sections, the script employs a precise methodology to ensure data integrity and usefulness.

### Key Features

### Cleaning Terms: `clean_term` Function

- **Purpose**: Cleanses terms by eliminating content within brackets and parentheses, trims extraneous punctuation, and excludes terms based on predefined criteria (e.g., numerical terms or those with specific unwanted characters).
- **Implementation**: This function uses Python string operations to accurately remove unwanted text and characters from each term, proving more reliable than regex for this dataset's specific nuances.

### Parsing Text: `parser` Function

- **Purpose**: Iterates through the dataset line by line to identify and extract information related to thesaurus classifications (classes, divisions, sections) and terms. It organizes this information into a structured pandas DataFrame.
- **Implementation Details**: 
  - **Class, Division, and Section Identification**: The script identifies headings for classes, divisions, and sections through line prefix analysis (e.g., starts with "CLASS"). It captures the associated descriptive text and updates the current context for subsequent terms.
  - **Term Extraction and Categorization**: Terms are extracted following the structural cues from the thesaurus, cleaned using the `clean_term` function, and categorized based on the current context (class/division/section).
  - **Data Structuring**: Extracted data is compiled into a pandas DataFrame, facilitating further analysis or storage.
- **Accuracy Consideration**: While HTML parsing techniques could theoretically be employed for this task, this script's approach was chosen as the most accurate method to parse and categorize terms, given the specific format and complexity of the dataset.

## Dependencies

- **pandas**: Essential for data manipulation, enabling the transformation of parsed and cleaned data into a DataFrame.
# Parallelized Embeddings Fetcher Documentation

### `parallelized_embeddings_fetcher.py`

The script focuses on overcoming the challenges associated with fetching large volumes of word embeddings from APIs, such as rate limiting and data management. It ensures efficient and reliable retrieval of embeddings, organizing them for easy access and analysis.

## Key Functions

### get_embeddings

- **Purpose**: Retrieves embeddings for a specific batch of terms using the chosen model.
- **Implementation**: Utilizes the `client` object to interact with the embeddings API, fetching embeddings for the batched terms. It returns a list of tuples, each containing a term and its corresponding embedding, ensuring that each term's embedding is accurately captured.

### fetch_embeddings_with_rate_limit

- **Purpose**: Addresses API rate limits by fetching embeddings in batches with controlled timing, preventing quota exceedance.
- **Implementation**: Splits the terms into batches and uses a `ThreadPoolExecutor` for concurrent fetching, adhering to the specified rate limit (`requests_per_minute`). This function maintains efficiency and compliance with API usage policies, returning a comprehensive map of terms to embeddings.

### store_embeddings_in_chunks

- **Purpose**: Manages file size and handling by storing the fetched embeddings in smaller, manageable JSON files.
- **Implementation**: Divides the term-embedding map into chunks, storing each in a separate JSON file within the specified directory. This approach facilitates easier data management and access, particularly for large datasets.

### read_embeddings

- **Purpose**: Aggregates embeddings from multiple JSON files into a single map, simplifying further processing or analysis.
- **Implementation**: Reads embeddings from all JSON files in the specified directory, combining them into a unified map. This function ensures that all fetched embeddings are easily accessible for subsequent analysis steps.

## Dependencies

- **concurrent.futures**: Enables concurrent execution, crucial for efficient batch processing.
- **time**: Used to manage request timing for rate limiting.
- **json**: Facilitates storage and retrieval of embeddings in JSON format.
- **os**: Assists in directory and file management operations.


