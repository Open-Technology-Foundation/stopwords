#!/usr/bin/env python3
import re
import sys
import string
from typing import List, Union
from nltk.corpus import stopwords  # type: ignore
from nltk.tokenize import word_tokenize  # type: ignore

# Supported languages by NLTK stopwords
SUPPORTED_LANGUAGES = set(stopwords.fileids())
DEFAULT_LANGUAGE = 'english'

def remove_stopwords(text: str, language: str = DEFAULT_LANGUAGE, 
                    punctuation: bool = False, list_words: bool = False) -> Union[str, List[str]]:
  """
  Remove stopwords from the input text.
  
  Args:
    text: Input text to process
    language: Language for stopwords (default: english)
    punctuation: If True, keep punctuation marks; if False, remove them
    list_words: If True, return list of words; if False, return string
    
  Returns:
    Filtered text as string or list of words
    
  Raises:
    ValueError: If language is not supported
  """
  # Validate inputs
  if not text:
    return [] if list_words else ""
    
  language = language.lower()
  if language not in SUPPORTED_LANGUAGES:
    sys.stderr.write(f"Language '{language}' not supported. Available languages: {', '.join(sorted(SUPPORTED_LANGUAGES))}\n")
    language = 'english'
#    raise ValueError(f"Language '{language}' not supported. Available languages: {', '.join(sorted(SUPPORTED_LANGUAGES))}")
  
  # Convert the string to lowercase
  text = text.lower()
  
  try:
    # Tokenize the string into words
    words = word_tokenize(text)
    # Get the list of stopwords for the specified language
    stop_words = set(stopwords.words(language))

    # Remove stopwords from the list of words
    if punctuation:
      filtered_words = [word for word in words if word not in stop_words]
    else:
      # Remove standard punctuation and stopwords
      filtered_words = [word for word in words if word not in stop_words and word not in string.punctuation]
      
      # Additional cleaning for non-punctuation mode:
      # 1. Remove special characters not in string.punctuation
      # 2. Remove possessive 's occurrences
      # 3. Filter out empty strings that might result from the cleaning
      special_chars = '`\'"-_’'  # Additional special characters to remove
      clean_words = []
      for word in filtered_words:
        # Remove possessive 's
        if word.endswith("'s"):
          word = word[:-2]
        
        # Remove additional special characters
        for char in special_chars:
          word = word.replace(char, '')
        
        # Only add non-empty words
        if word:
          clean_words.append(word)
      
      filtered_words = clean_words
            
    if list_words:
      return filtered_words
    else:
      # Join the filtered words back into a string
      filtered_text = ' '.join(filtered_words)
      # Remove duplicate spaces
      filtered_text = re.sub(r'\s+', ' ', filtered_text).strip()
      return filtered_text
  except LookupError as e:
    # Handle missing NLTK resources
    sys.stderr.write(f"NLTK resource error: {str(e)}\n")
    sys.stderr.write("You may need to download NLTK resources. Try: python -m nltk.downloader stopwords punkt\n")
    raise

def main():
  import argparse

  parser = argparse.ArgumentParser(description='Remove stopwords from text.')
  parser.add_argument('text', nargs='?', help='The input text. If not provided, read from stdin.')
  parser.add_argument('-l', '--language', default=DEFAULT_LANGUAGE, 
                     help=f'The language of the stopwords (default: {DEFAULT_LANGUAGE}). Available: {", ".join(sorted(SUPPORTED_LANGUAGES))}')
  parser.add_argument('-p', '--keep-punctuation', dest='punctuation', action='store_true', 
                     help='Keep punctuation marks (default: remove punctuation).')
  parser.add_argument('-w', '--list-words', action='store_true', 
                     help='Output the filtered words as a list (default: join words into a string).')
  args = parser.parse_args()

  # Handle input source
  if args.text is not None:
    text = args.text.strip()
  else:
    # Read input from stdin
#    text = sys.stdin.read().strip()
    # Read as binary first
    binary_data = sys.stdin.buffer.read()
    # Then try to decode
    try:
      text = binary_data.decode('utf-8')
    except UnicodeDecodeError:
      # Handle binary data or try different encoding
      sys.stderr.write("Warning: Input contains non-UTF-8 data\n")
      text = binary_data.decode('utf-8', errors='replace')

  try:
    filtered_text = remove_stopwords(
      text, 
      language=args.language, 
      punctuation=args.punctuation, 
      list_words=args.list_words
    )
    
    if args.list_words:
      for word in filtered_text:
        print(word)
    else:
      print(filtered_text)
  except ValueError as e:
    sys.stderr.write(f"Error: {str(e)}\n")
    sys.exit(1)
  except LookupError:
    # Already handled in the function
    sys.exit(1)
  except Exception as e:
    sys.stderr.write(f"An unexpected error occurred: {str(e)}\n")
    sys.exit(1)

if __name__ == '__main__':
  main()

#fin