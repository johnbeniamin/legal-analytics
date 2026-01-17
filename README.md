# Legal Keyword Extractor (LKE)

A Python-based NLP tool designed to extract meaningful legal concepts from large Arabic legal texts.

## Features
- **Statistical Filtering:** Uses frequency density analysis (Zipf's Law logic) to identify significant keywords.
- **Noise Reduction:** Automatically removes common Arabic stop words and punctuation.
- **N-gram Analysis:** Extracts both single keywords and compound legal phrases (Bigrams).

## How to Use
1. Place your text in `data.txt` inside the project folder.
2. Run the analysis script:
   ```bash
   python3 analysis.py