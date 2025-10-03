#!/bin/bash
#shellcheck disable=SC2011
# Remove stopwords from text
set -euo pipefail

# Shell options
shopt -s inherit_errexit shift_verbose extglob nullglob

# Script metadata
VERSION='1.0.0'
SCRIPT_PATH=$(readlink -en -- "$0") 
SCRIPT_DIR=${SCRIPT_PATH%/*}        
SCRIPT_NAME=${SCRIPT_PATH##*/}      
readonly -- VERSION SCRIPT_PATH SCRIPT_DIR SCRIPT_NAME

# Global constants
readonly -- DEFAULT_LANGUAGE='english'

# Global variables
declare -- LANGUAGE="$DEFAULT_LANGUAGE"
declare -i KEEP_PUNCTUATION=0
declare -i LIST_WORDS=0
declare -- INPUT_TEXT=''

# --------------------------------------------------------------------------------
# Utility functions
# --------------------------------------------------------------------------------

# Error message to stderr
error() {
  local -- msg
  for msg in "$@"; do
    >&2 printf '%s: %s\n' "$SCRIPT_NAME" "$msg"
  done
}

# Exit with error message
die() {
  (($# > 1)) && error "${@:2}"
  exit "${1:-0}"
}

# --------------------------------------------------------------------------------
# Business logic functions
# --------------------------------------------------------------------------------

# Show usage information
usage() {
  cat <<EOT
$SCRIPT_NAME $VERSION - Remove stopwords from text

Filters stopwords from input text based on the selected language.

Usage: $SCRIPT_NAME [OPTIONS] [TEXT]

Arguments:
  TEXT                   The input text. If not provided, read from stdin.

Options:
  -l|--language LANG     The language of the stopwords (default: english)
  -p|--keep-punctuation  Keep punctuation marks (default: remove punctuation)
  -w|--list-words        Output the filtered words as a list (one per line)
  -V|--version           Show version information
  -h|--help              Show this help message

Available languages:
  $(ls "$SCRIPT_DIR/data"/*.txt 2>/dev/null | xargs -n1 basename | sed 's/.txt$//' | tr '\n' ',' | sed 's/,/, /g' | sed 's/, $//')

Examples:
  # Filter stopwords from text
  $SCRIPT_NAME 'the quick brown fox jumps over the lazy dog'

  # Read from stdin
  echo 'the quick brown fox' | $SCRIPT_NAME

  # Use Spanish stopwords
  $SCRIPT_NAME -l spanish 'el rápido zorro marrón'

  # Keep punctuation
  $SCRIPT_NAME -p 'Hello, world!'

  # Output as list
  $SCRIPT_NAME -w 'the quick brown fox'
EOT
  exit "${1:-0}"
}

# --------------------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------------------

main() {
  local -i exitcode=0

  # Parse command-line arguments
  while (($#)); do
    case $1 in
      -l|--language)
        [[ -n ${2:-} ]] || die 2 "Missing argument for option '$1'"
        LANGUAGE="$2"
        shift 2
        ;;
      -p|--keep-punctuation)
        KEEP_PUNCTUATION=1
        shift
        ;;
      -w|--list-words)
        LIST_WORDS=1
        shift
        ;;
      -V|--version)
        echo "$SCRIPT_NAME $VERSION"
        exit 0
        ;;
      -h|--help)
        usage 0
        ;;
      -[lpwVh]*) #shellcheck disable=SC2046 #split up single options
        set -- '' $(printf -- "-%c " $(grep -o . <<<"${1:1}")) "${@:2}"
        ;;
      -*)
        die 22 "Invalid option '$1'"
        ;;
      *)
        INPUT_TEXT+="$1 "
        shift
        ;;
    esac
  done

  # Validate language
  local -- stopwords_file="$SCRIPT_DIR/data/${LANGUAGE}.txt"
  if [[ ! -f "$stopwords_file" ]]; then
    error "Language '${LANGUAGE}' not supported."
    >&2 echo 'Available languages:'
    >&2 ls "$SCRIPT_DIR/data"/*.txt 2>/dev/null | xargs -n1 basename | sed 's/.txt$//' | tr '\n' ',' | sed 's/,/, /g' | sed 's/, $//'
    >&2 echo ''
    error "Falling back to 'english'"
    LANGUAGE='english'
    stopwords_file="$SCRIPT_DIR/data/${LANGUAGE}.txt"
  fi

  # Load stopwords into associative array
  local -A stopwords
  local -- word
  while IFS= read -r word; do
    # Store lowercase version for case-insensitive matching
    stopwords["${word,,}"]=1
  done < "$stopwords_file"

  # Get input text
  if [[ -z "$INPUT_TEXT" ]]; then
    # Read from stdin
    INPUT_TEXT=$(cat)
  fi

  # Exit early if input is empty
  [[ -z "$INPUT_TEXT" ]] && return 0

  # Convert to lowercase for processing
  local -- lower_text="${INPUT_TEXT,,}"

  # Tokenize and filter
  local -a filtered_words=()

  if ((KEEP_PUNCTUATION)); then
    # Keep punctuation: split on whitespace only
    # Replace multiple spaces/tabs/newlines with single space
    lower_text=$(echo "$lower_text" | tr -s '[:space:]' ' ')

    # Split into words
    for word in $lower_text; do
      # Check if word is not a stopword
      if [[ ! -v stopwords["$word"] ]]; then
        filtered_words+=("$word")
      fi
    done
  else
    # Remove punctuation: replace punctuation with spaces, then split
    # First, handle possessive 's by removing it
    #shellcheck disable=SC2001
    lower_text=$(echo "$lower_text" | sed "s/'s\b/ /g")

    # Replace punctuation and special characters with spaces
    # This includes standard punctuation and additional special chars
    lower_text=$(echo "$lower_text" | tr '[:punct:]' ' ' | tr '\n\t' ' ')

    # Collapse multiple spaces
    lower_text=$(echo "$lower_text" | tr -s ' ')

    # Split into words and filter
    for word in $lower_text; do
      # Skip empty words
      [[ -z "$word" ]] && continue

      # Additional cleaning for special characters that might remain
      word=$(echo "$word" | tr -d '\`"_''')

      # Skip if word is now empty after cleaning
      [[ -z "$word" ]] && continue

      # Check if word is not a stopword
      if [[ ! -v stopwords["$word"] ]]; then
        filtered_words+=("$word")
      fi
    done
  fi

  # Output results
  if ((LIST_WORDS)); then
    # Output one word per line
    printf '%s\n' "${filtered_words[@]}"
  else
    # Output as a single line with spaces
    if ((${#filtered_words[@]} > 0)); then
      echo "${filtered_words[*]}"
    fi
  fi

  return "$exitcode"
}

# Call main with all arguments
main "$@"

#fin
