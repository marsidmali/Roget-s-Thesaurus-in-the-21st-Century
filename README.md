# 📚 Roget's Thesaurus in the 21st Century

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?logo=TensorFlow&logoColor=white)](https://tensorflow.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An investigation into how modern machine learning techniques align with Roget's classical thesaurus categorization system from 1852. This project explores whether contemporary word embeddings can validate or challenge the historical classification principles. 🤖

## ✨ Features

1. **Data Collection & Processing**
   - Web scraping of Roget's Thesaurus
   - Hierarchical parsing of classes, divisions, sections, and terms
   - Custom preprocessing preserving linguistic nuances

2. **Word Embeddings**
   - OpenAI's text-embedding-3-large model
   - Parallel processing for efficient embedding generation
   - Chunked storage system for large-scale embeddings

3. **Unsupervised Learning**
   - Clustering analysis at both class and division/section levels
   - Comparison between discovered clusters and Roget's classification
   - Hungarian algorithm for optimal cluster matching

4. **Supervised Classification**
   - Two-level prediction models (class and division/section)
   - Neural networks, Random Forest and XGBoost implementations
   - Performance evaluation with multiple metrics

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/marsidmali/Roget-s-Thesaurus-in-the-21st-Century.git
cd Roget-s-Thesaurus-in-the-21st-Century
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key

## 📁 Project Structure

```plaintext
Roget-s-Thesaurus-in-the-21st-Century/
│
├── notebooks/           # Jupyter notebooks
│   └── rogets_thesaurus_analysis.ipynb
│   └── assigment_3.ipynb
├── utils/               # Utility functions
│   └── thesaurus_parser.py
│   └── parallelized_embeddings_fetcher.py 
├── embeddings/          # Embeddings storage  
├── requirements.txt     # Dependencies
└── README.md            # Documentation
```

## 🚀 Usage

1. Launch Jupyter Notebook:
```bash
jupyter notebook
```

2. Open `rogets_thesaurus_analysis.ipynb`
3. Run all cells to perform the analysis

## ⚙️ Configuration

Create a `.env` file with your OpenAI API key:
```plaintext
OPENAI_API_KEY=your_api_key_here
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

