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
```bash
git clone https://github.com/yourusername/stopwords.git
cd stopwords
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

4. Download required NLTK resources:
```bash
python -m nltk.downloader stopwords punkt
```

5. Make the script executable (if not already):
```bash
chmod +x stopwords
```

## Usage

### Command Line

```bash
# Basic usage
./stopwords "Text to process and remove stopwords from"

# Read from stdin
cat somefile.txt | ./stopwords
echo "Some text here" | ./stopwords

# Keep punctuation
./stopwords --keep-punctuation "Keep the punctuation, just remove stopwords!"
./stopwords -p "Keep the punctuation, just remove stopwords!"

# Output as list of words
./stopwords --list-words "Output each word on a separate line"
./stopwords -w "Output each word on a separate line"

# Use different language stopwords
./stopwords --language spanish "Hola cómo estás hoy"
./stopwords -l spanish "Hola cómo estás hoy"

# Combine options
./stopwords -l french -p -w "Voici du texte en français!"
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

The script supports all languages available in NLTK's stopwords corpus. To see the full list of available languages, the script will display them if you specify an unsupported language.

Common languages include:
- arabic
- azerbaijani
- basque
- bengali
- catalan
- chinese
- danish
- dutch
- english (default)
- finnish
- french
- german
- greek
- hebrew
- hinglish
- hungarian
- indonesian
- italian
- kazakh
- nepali
- norwegian
- portuguese
- romanian
- russian
- slovene
- spanish
- swedish
- tajik
- tamil
- turkish

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.
