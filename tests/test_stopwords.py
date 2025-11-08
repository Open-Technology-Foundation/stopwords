#!/usr/bin/env python3
"""
Unit tests for stopwords module.

Tests cover all major functionality including:
- Empty input handling
- Stopword removal in different languages
- Punctuation handling
- Output format options (string vs list)
- Error handling and edge cases
"""
import unittest
from stopwords import remove_stopwords, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE, __version__


class TestRemoveStopwords(unittest.TestCase):
    """Test the remove_stopwords function."""

    def test_empty_string_returns_empty_string(self) -> None:
        """Empty input should return empty string."""
        result = remove_stopwords("")
        self.assertEqual(result, "")

    def test_empty_string_returns_empty_list_when_list_words_true(self) -> None:
        """Empty input should return empty list in list mode."""
        result = remove_stopwords("", list_words=True)
        self.assertEqual(result, [])
        self.assertIsInstance(result, list)

    def test_removes_english_stopwords(self) -> None:
        """Should remove common English stopwords."""
        text = "This is a test of the stopwords removal system"
        result = remove_stopwords(text, list_words=True)

        # These are stopwords and should be removed
        self.assertNotIn("is", result)
        self.assertNotIn("a", result)
        self.assertNotIn("the", result)
        self.assertNotIn("this", result)
        self.assertNotIn("of", result)

        # These are content words and should remain
        self.assertIn("test", result)
        self.assertIn("stopwords", result)
        self.assertIn("removal", result)
        self.assertIn("system", result)

    def test_removes_punctuation_by_default(self) -> None:
        """Should remove punctuation by default."""
        text = "Hello, world! How are you?"
        result = remove_stopwords(text, list_words=True)
        self.assertNotIn(",", result)
        self.assertNotIn("!", result)
        self.assertNotIn("?", result)

    def test_keeps_punctuation_when_flag_set(self) -> None:
        """Should keep punctuation when punctuation=True."""
        text = "Hello, world!"
        result = remove_stopwords(text, punctuation=True, list_words=True)
        # Punctuation should be present
        self.assertIn(",", result)
        self.assertIn("!", result)

    def test_returns_list_when_list_words_true(self) -> None:
        """Should return list when list_words=True."""
        text = "Hello world test"
        result = remove_stopwords(text, list_words=True)
        self.assertIsInstance(result, list)
        self.assertIn("hello", result)
        self.assertIn("world", result)
        self.assertIn("test", result)

    def test_returns_string_by_default(self) -> None:
        """Should return string by default."""
        text = "Hello world test"
        result = remove_stopwords(text)
        self.assertIsInstance(result, str)
        self.assertIn("hello", result)
        self.assertIn("world", result)

    def test_unsupported_language_falls_back_to_english(self) -> None:
        """Unsupported language should fall back to English without raising."""
        text = "test message content"
        # Should not raise, should use English stopwords
        result = remove_stopwords(text, language="klingon")
        self.assertIsInstance(result, str)
        # Should have removed English stopwords (no exception raised)
        self.assertEqual(result, "test message content")

    def test_case_insensitive_processing(self) -> None:
        """Should convert to lowercase for processing."""
        text = "HELLO WORLD TEST"
        result = remove_stopwords(text)
        self.assertEqual(result, result.lower())
        self.assertIn("hello", result)
        self.assertIn("world", result)

    def test_removes_possessive_s(self) -> None:
        """Should remove possessive 's."""
        text = "John's book Mary's pen"
        result = remove_stopwords(text, list_words=True)
        # Should have 'john' and 'mary' without possessive
        self.assertIn("john", result)
        self.assertIn("mary", result)
        # Should not have the possessive forms
        self.assertNotIn("john's", result)
        self.assertNotIn("mary's", result)

    def test_supported_languages_constant_is_set(self) -> None:
        """SUPPORTED_LANGUAGES should be populated."""
        self.assertIsInstance(SUPPORTED_LANGUAGES, set)
        self.assertGreater(len(SUPPORTED_LANGUAGES), 0)
        self.assertIn("english", SUPPORTED_LANGUAGES)

    def test_default_language_is_english(self) -> None:
        """DEFAULT_LANGUAGE should be 'english'."""
        self.assertEqual(DEFAULT_LANGUAGE, "english")

    def test_multiple_spaces_normalized(self) -> None:
        """Multiple consecutive spaces should be normalized to single space."""
        text = "hello    world     test"
        result = remove_stopwords(text)
        # Should not have multiple spaces
        self.assertNotIn("  ", result)
        self.assertEqual(result, "hello world test")

    def test_special_characters_removed(self) -> None:
        """Special characters should be removed by default."""
        text = "hello-world `test` 'quote' \"double\""
        result = remove_stopwords(text, list_words=True)
        # Should have cleaned words
        self.assertIn("helloworld", result)
        self.assertIn("test", result)
        self.assertIn("quote", result)
        self.assertIn("double", result)

    def test_language_case_insensitive(self) -> None:
        """Language parameter should be case-insensitive."""
        text = "test message"
        result1 = remove_stopwords(text, language="ENGLISH")
        result2 = remove_stopwords(text, language="english")
        result3 = remove_stopwords(text, language="English")
        # All should produce the same result
        self.assertEqual(result1, result2)
        self.assertEqual(result2, result3)

    def test_whitespace_handling(self) -> None:
        """Should handle leading/trailing whitespace correctly."""
        text = "   hello world test   "
        result = remove_stopwords(text)
        # Should be stripped
        self.assertEqual(result, "hello world test")
        self.assertFalse(result.startswith(" "))
        self.assertFalse(result.endswith(" "))

    def test_list_output_has_no_empty_strings(self) -> None:
        """List output should not contain empty strings."""
        text = "hello,,,world...test!!!"
        result = remove_stopwords(text, list_words=True)
        self.assertNotIn("", result)
        # All items should be non-empty
        for word in result:
            self.assertTrue(len(word) > 0)


class TestCLIIntegration(unittest.TestCase):
    """Test CLI functionality."""

    def test_main_function_exists(self) -> None:
        """main() function should be callable."""
        from stopwords import main

        self.assertTrue(callable(main))

    def test_main_function_has_correct_return_type(self) -> None:
        """main() should have return type annotation of None."""
        from stopwords import main

        self.assertEqual(main.__annotations__.get("return"), None)

    def test_version_constant_exists(self) -> None:
        """__version__ constant should exist and be valid semver."""
        self.assertIsInstance(__version__, str)
        self.assertTrue(len(__version__) > 0)
        # Check basic semver format (X.Y.Z)
        parts = __version__.split(".")
        self.assertEqual(len(parts), 3, "Version should be in X.Y.Z format")
        for part in parts:
            self.assertTrue(part.isdigit(), f"Version part '{part}' should be numeric")


if __name__ == "__main__":
    unittest.main()

#fin
