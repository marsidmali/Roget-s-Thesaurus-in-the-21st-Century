## Overview
In this notebook, we delve into the use of Machine Learning techniques, particularly word embeddings, to examine the categorization of words within Roget's Thesaurus. We begin with a historical overview of Roget's Thesaurus and its structured organization, setting the stage for our investigation into the relationship between these traditional categories and the semantic meanings of English words as captured by modern Machine Learning methods.

## Key Sections

### 1. Acquiring Roget's Thesaurus Classification
We describe the process of obtaining Roget's Thesaurus classification, utilizing Python libraries such as `requests`, `BeautifulSoup`, `json`, and `pandas` for web scraping and data management. For more details, refer to utils README.md.

### 2. Analysis of Thesaurus Categories
We conduct an analysis on the distribution of words across Roget's Thesaurus categories, noting significant imbalances and the dominance of certain parts of speech. Our methodology for categorization data storage and processing is aimed at efficiency and accuracy.

### 3. Rethinking Preprocessing Practices for Word Embeddings
Contrary to commonly used text preprocessing steps for word embeddings, we advocate for preserving punctuation, case sensitivity, and other textual nuances. This section outlines a customized approach to preprocessing, tailored to the specific requirements of our project.

### 4. Deduplication of Terms
To effectively manage the dataset size before generating embeddings, we implement a deduplication step, demonstrating careful data handling.

### 5. Generating Word Embeddings
Following term deduplication, we proceed to generate word embeddings for Roget's Thesaurus's unique terms. This crucial phase involves:
- **Selecting the Embedding Model**: After evaluating various models, we select the OpenAI API's 'text-embedding-3-large' model for its capacity to produce 3072-dimensional embeddings, offering detailed semantic representations.
- **Efficiently Fetching Embeddings**: We introduce a rate-limited fetching mechanism to manage the task scale without exceeding API usage limits, ensuring an efficient and cost-effective approach.
- **Storing Embeddings**: Opting for a practical data storage method, we save embeddings in chunks for straightforward management and access, and provide a method for loading pre-generated embeddings to enhance analysis flexibility.

### 6. Clustering 

With our high-dimensional embeddings prepared, we shift our focus to utilizing unsupervised Machine Learning methods to explore if natural word groupings, comparable to Roget's Thesaurus classifications, can be identified.
- **Dimensionality Reduction**: Due to the embeddings' high dimensionality, we apply Principal Component Analysis (PCA) to reduce the dataset size while preserving significant variance. We identify an elbow in the scree plot around 350 components, suggesting this as an optimal balance for explanatory power, accounting for roughly 80% of the variance.
- **KMeans Clustering**: We employ KMeans clustering on the reduced dataset, selecting six clusters to reflect the class-level organization in Roget's Thesaurus, aiming to discern natural groupings based on semantic similarity.
- **Visual Analysis**: Clusters, reduced to two and three dimensions for visualization, offer an intuitive view of the data segmentation. Centroid markers in these visualizations aid in clearly defining each cluster.

#### Classification Alignment
To evaluate how well our machine-generated clusters align with the classes defined in Roget's Thesaurus, we undertake the following steps:
- **Contingency Matrix Construction**: We create a contingency matrix for a cross-tabulation of classes within each cluster, serving as a foundational tool for further analysis.
- **Purity Calculation**: The purity of our clustering is calculated, providing a direct measure of alignment quality. Initial results indicate a moderate alignment level, highlighting potential areas for refinement in accurately capturing Roget's categorizations.
- **Optimal Matching**: Utilizing the Hungarian algorithm, we optimally match clusters to classes. This method considers the dataset's imbalanced nature and seeks to optimize alignment using a cost matrix derived from the contingency matrix.
- **Evaluation Metrics**: Precision, recall, and F1 scores are determined for each cluster-class pairing to offer a detailed perspective on the effectiveness of our clustering. These metrics unveil various alignment degrees, with certain clusters demonstrating stronger correlations to specific classes.

#### Hierarchical Clustering and Division/Section Analysis
We delve deeper than class-level analysis by applying hierarchical clustering within each primary cluster to identify sub-groupings that may correspond with Roget's divisions/sections.
- **Subcluster Identification**: Hierarchical clustering is conducted on the embeddings for each cluster, aiming to reveal subclusters potentially aligned with the Thesaurus's finer divisions/sections.
- **Evaluation at Division/Section Level**: These subclusters are then matched to actual division/section labels through the Hungarian algorithm. Precision, recall, and F1 scores are calculated for each match, providing insight into the clustering's accuracy at capturing the detailed categorizations within Roget's Thesaurus.

### 7. Class Prediction
Switching to supervised Machine Learning, we aim to predict a word's class or its section/division, necessitating two distinct models.
- **Dataset Reduction**: For classification tasks, we reduce our dataset to 100 components using PCA, followed by standard scaling.

#### Initial Model: Random Forest
- **Implementation**: We employ a Random Forest model to predict classes, achieving an overall accuracy of 51.5%. The model shows varying effectiveness across classes, with notable performance in identifying `CLASS V` and `CLASS IV`.

#### Advanced Model: XGBoost
- **Performance**: An XGBoost model improves overall accuracy to 54.94%. It demonstrates consistent precision, recall, and F1-scores across classes, with slight advantages in `Class 3` and `Class 5`.

#### Neural Network Approach

#### Model Architecture
We employ Sequential models from Keras with the following layers:
- Dense layers for learning non-linear relationships.
- Dropout for regularization to prevent overfitting.
- BatchNormalization to maintain the mean output close to 0 and the output standard deviation close to 1.

#### Compilation and Training
- **Optimizer**: Adam with a learning rate of 0.001.
- **Loss Function**: Categorical Crossentropy, suitable for multi-class classification.
- **Metrics**: Accuracy, Precision, and Recall to evaluate model performance.
- **Callbacks**: EarlyStopping to halt training when the validation loss ceases to decrease, and ModelCheckpoint to save the best model weights.

#### Model Evaluation
Post-training, the model is evaluated on a test set, and metrics such as Loss, Accuracy, Precision, and Recall are reported to assess its performance.

#### Observations and Results
- The implementation of class weights to address data imbalance was explored. However, contrary to expectations, models trained with class weights did not always perform better in terms of accuracy, precision, and recall.
- Visualization of training and validation metrics over epochs indicated a robust learning process, with the models achieving stability and demonstrating balanced performance metrics.
