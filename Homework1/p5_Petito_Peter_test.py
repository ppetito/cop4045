"""Unit tests for the Caesar cipher program."""

import unittest

from p5_Petito_Peter import caesar_cipher, caesar_decipher, letter_frequency


class CaesarCipherTest(unittest.TestCase):
    """Test Caesar cipher encryption and decryption."""

    def test_basic_shifting(self):
        """Encrypts letters by the requested number of positions."""
        self.assertEqual(caesar_cipher("abc", 3), "def")

    def test_wrapping_around_alphabet(self):
        """Wraps letters past z back to the start of the alphabet."""
        self.assertEqual(caesar_cipher("xyz", 3), "abc")

    def test_preserves_casing(self):
        """Keeps uppercase and lowercase letters in their original case."""
        self.assertEqual(caesar_cipher("AbC", 2), "CdE")

    def test_preserves_spaces_and_punctuation(self):
        """Leaves non-alphabetic characters unchanged."""
        self.assertEqual(caesar_cipher("Hello, world! 123", 1),
                         "Ifmmp, xpsme! 123")

    def test_decipher_reverses_cipher(self):
        """Decrypts text encrypted with the same shift value."""
        message = "Meet me at 8:00!"
        self.assertEqual(caesar_decipher(caesar_cipher(message, 7), 7),
                         message)


class LetterFrequencyTest(unittest.TestCase):
    """Test letter frequency counting."""

    def test_counts_letters_case_insensitively(self):
        """Counts uppercase and lowercase versions of a letter together."""
        frequencies = letter_frequency("Apple aPPle")
        self.assertEqual(frequencies["a"], 2)
        self.assertEqual(frequencies["p"], 4)
        self.assertEqual(frequencies["l"], 2)
        self.assertEqual(frequencies["e"], 2)

    def test_ignores_non_alphabetic_characters(self):
        """Does not count spaces, punctuation, or numbers."""
        frequencies = letter_frequency("A! a? 123")
        self.assertEqual(frequencies["a"], 2)
        self.assertEqual(sum(frequencies.values()), 2)

    def test_empty_string(self):
        """Returns zero counts for every letter when text is empty."""
        frequencies = letter_frequency("")
        self.assertEqual(len(frequencies), 26)
        self.assertTrue(all(count == 0 for count in frequencies.values()))


if __name__ == "__main__":
    unittest.main()
