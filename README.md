# Stopwords Remover

A simple command-line utility to remove stopwords and clean text.

## Overview

This utility removes common stopwords (such as "the", "a", "is") from text, optionally removes punctuation and special characters, and provides clean output for natural language processing tasks.

## Features

- Remove language-specific stopwords (supports multiple languages via NLTK)
- Remove punctuation marks and special characters 
- Clean up possessive forms and normalize spacing
- Output as joined text or list of individual words
- Read from command line arguments or stdin

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/stopwords.git
cd stopwords
```

2. Create and activate a virtual environment:
```
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install required dependencies:
```
pip install -r requirements.txt
```

4. Download required NLTK resources:
```
python -m nltk.downloader stopwords punkt
```

5. Make the script executable:
```
chmod +x stopwords
```

## Usage

### Command Line

```
# Basic usage
./stopwords "Text to process and remove stopwords from"

# Read from stdin
cat somefile.txt | ./stopwords

# Keep punctuation 
./stopwords -p "Keep the punctuation, just remove stopwords!"

# Output as list of words
./stopwords -w "Output each word on a separate line"

# Use different language stopwords
./stopwords -l spanish "Hola cómo estás hoy"
```

### Python Module

```python
from stopwords import remove_stopwords

# Basic usage
text = "This is some sample text with stopwords to remove."
filtered_text = remove_stopwords(text)
print(filtered_text)  # "sample text stopwords remove"

# Keep punctuation
filtered_text = remove_stopwords("Keep the, punctuation!", punctuation=True)

# Get list of words
word_list = remove_stopwords("Get a list of words", list_words=True)

# Different language
spanish_text = remove_stopwords("Hola cómo estás", language="spanish")
```

## Supported Languages

The script supports all languages available in NLTK's stopwords corpus, including:
- english
- spanish
- french
- german
- italian
- portuguese
- and many more

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.
