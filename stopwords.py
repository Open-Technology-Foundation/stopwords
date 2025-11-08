#!/usr/bin/env python3
"""
Stopwords Removal Utility (Python 3.12+)

A modern Python module for removing stopwords and cleaning text using NLTK.
Supports 32+ languages and provides flexible output formats.

For small documents (<2000 words), consider the Bash version:
https://github.com/Open-Technology-Foundation/stopwords.bash

Functions:
    remove_stopwords: Remove stopwords from text with language support
    main: CLI entry point for command-line usage

Constants:
    __version__: Current version string
    SUPPORTED_LANGUAGES: Set of available language codes from NLTK
    DEFAULT_LANGUAGE: Default language for stopword removal
"""
import re
import sys
import string
from nltk.corpus import stopwords  # type: ignore
from nltk.tokenize import word_tokenize  # type: ignore

# Version (semantic versioning: MAJOR.MINOR.PATCH)
__version__ = "1.0.0"

# Language support (dynamically loaded from NLTK stopwords corpus - 32+ languages)
SUPPORTED_LANGUAGES = set(stopwords.fileids())
# Default language used when unsupported language is specified (with fallback warning)
DEFAULT_LANGUAGE = "english"


def remove_stopwords(
    text: str,
    language: str = DEFAULT_LANGUAGE,
    punctuation: bool = False,
    list_words: bool = False,
) -> str | list[str]:
    """
    Remove stopwords from the input text.

    Args:
        text: Input text to process
        language: Language for stopwords (default: english)
        punctuation: If True, keep punctuation marks; if False, remove them
        list_words: If True, return list of words; if False, return string

    Returns:
        Filtered text as string (default) or list of words (if list_words=True)

    Raises:
        LookupError: If NLTK stopwords or punkt resources are not downloaded

    Note:
        Unsupported languages automatically fall back to English with a warning
        message to stderr. Empty input returns empty string or empty list.
    """
    # === INPUT VALIDATION ===
    # Return early for empty input (preserves output type)
    if not text:
        return [] if list_words else ""

    # Normalize language code and validate against supported languages
    language = language.lower()
    if language not in SUPPORTED_LANGUAGES:
        sys.stderr.write(
            f"Language '{language}' not supported. Available languages: {', '.join(sorted(SUPPORTED_LANGUAGES))}\n"
        )
        # Fallback to English when unsupported language specified
        language = "english"

    # === TEXT PREPROCESSING ===
    # Normalize to lowercase for consistent stopword matching
    text = text.lower()

    try:
        # Tokenize text into individual words using NLTK
        words = word_tokenize(text)

        # === STOPWORD FILTERING ===
        # Load stopwords for specified language (cached by NLTK)
        stop_words = set(stopwords.words(language))

        # Filter based on punctuation preservation mode
        if punctuation:
            filtered_words = [word for word in words if word not in stop_words]
        else:
            # Remove both stopwords and standard punctuation
            filtered_words = [
                word
                for word in words
                if word not in stop_words and word not in string.punctuation
            ]

            # === SPECIAL CHARACTER CLEANING ===
            # Additional cleaning beyond standard punctuation:
            # 1. Remove possessive 's endings (e.g., "John's" → "john")
            # 2. Remove special characters: backticks, quotes, hyphens, curly quotes
            # 3. Filter out empty strings resulting from cleaning
            special_chars = (
                "`'\"-_'"  # Backtick, quotes, hyphen, underscore, curly quote
            )
            clean_words = []
            for word in filtered_words:
                # Remove possessive 's
                if word.endswith("'s"):
                    word = word[:-2]

                # Remove additional special characters
                for char in special_chars:
                    word = word.replace(char, "")

                # Only add non-empty words
                if word:
                    clean_words.append(word)

            filtered_words = clean_words

        # === OUTPUT FORMATTING ===
        if list_words:
            # Return as list of individual words
            return filtered_words
        else:
            # Join words into single string with spaces
            filtered_text = " ".join(filtered_words)
            # Normalize whitespace (collapse multiple spaces, trim edges)
            filtered_text = re.sub(r"\s+", " ", filtered_text).strip()
            return filtered_text

    # === ERROR HANDLING ===
    except LookupError as e:
        # Missing NLTK data (stopwords or punkt tokenizer)
        sys.stderr.write(f"NLTK resource error: {str(e)}\n")
        sys.stderr.write(
            "You may need to download NLTK resources. Try: python -m nltk.downloader stopwords punkt\n"
        )
        raise


def main() -> None:
    """
    CLI entry point for stopwords removal.

    Handles command-line arguments, reads input from arguments or stdin,
    processes text through remove_stopwords(), and outputs results to stdout.

    Exit codes:
        0: Success
        1: Error (ValueError, LookupError, or unexpected exception)
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Remove stopwords from text in 32+ languages. Supports stdin/stdout piping.",
        epilog="""
Examples:
  %(prog)s "Remove stopwords from this text"
  echo "Some text" | %(prog)s
  %(prog)s -l spanish "Texto en español"
  cat file.txt | %(prog)s -w > words.txt
  %(prog)s -l french -p "Texte avec ponctuation!"

For more help: %(prog)s --help
For version: %(prog)s --version
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "text",
        nargs="?",
        help="Input text to process (if omitted, reads from stdin for piping)",
    )
    parser.add_argument(
        "-l",
        "--language",
        default=DEFAULT_LANGUAGE,
        metavar="LANG",
        help="Stopword language: english, spanish, french, german, etc. (default: %(default)s)",
    )
    parser.add_argument(
        "-p",
        "--keep-punctuation",
        dest="punctuation",
        action="store_true",
        help="Preserve punctuation marks in output (default: remove all punctuation)",
    )
    parser.add_argument(
        "-w",
        "--list-words",
        action="store_true",
        help="Output one word per line instead of joined text (useful for piping/scripting)",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"stopwords {__version__}",
    )
    args = parser.parse_args()

    # === INPUT SOURCE HANDLING ===
    if args.text is not None:
        # Text provided as command-line argument
        text = args.text.strip()
    else:
        # Read from stdin (for piping: cat file.txt | stopwords)
        # Read as binary first for safe UTF-8 handling
        binary_data = sys.stdin.buffer.read()

        # Decode to UTF-8 text
        try:
            text = binary_data.decode("utf-8")
        except UnicodeDecodeError:
            # Gracefully handle non-UTF-8 input (replace invalid bytes with �)
            sys.stderr.write("Warning: Input contains non-UTF-8 data\n")
            text = binary_data.decode("utf-8", errors="replace")

    # === TEXT PROCESSING ===
    try:
        filtered_text = remove_stopwords(
            text,
            language=args.language,
            punctuation=args.punctuation,
            list_words=args.list_words,
        )

        # === OUTPUT ===
        if args.list_words:
            # Output one word per line (list mode)
            for word in filtered_text:
                print(word)
        else:
            # Output as single joined string (default mode)
            print(filtered_text)

    # === ERROR HANDLING ===
    except ValueError as e:
        # Invalid input or parameters
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.exit(1)
    except LookupError:
        # NLTK resources missing (error message already printed in remove_stopwords)
        sys.exit(1)
    except Exception as e:
        # Unexpected errors
        sys.stderr.write(f"An unexpected error occurred: {str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()

# fin
