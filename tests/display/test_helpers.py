from unittest import TestCase

from adventure.display.helpers import concatenate_items, guess_article


class ConcatenateItemsTestCase(TestCase):
    def test_no_items(self):
        text = concatenate_items([])
        self.assertEqual(text, '')

    def test_single_item(self):
        text = concatenate_items(['item'])
        self.assertEqual(text, 'item')

    def test_two_items(self):
        text = concatenate_items(['item1', 'item2'])
        self.assertEqual(text, 'item1 and item2')

    def test_multiple_items(self):
        text = concatenate_items(['item1', 'item2', 'item3', 'item4'])
        self.assertEqual(text, 'item1, item2, item3, and item4')

    def test_different_conjunction(self):
        text = concatenate_items(['item1', 'item2'], conjunction='or')
        self.assertEqual(text, 'item1 or item2')

        text = concatenate_items(['item1', 'item2', 'item3'], conjunction='or')
        self.assertEqual(text, 'item1, item2, or item3')


class GuessArticleTestCase(TestCase):
    def test_starts_with_vowel(self):
        self.assertEqual(guess_article('apple'), 'an')
        self.assertEqual(guess_article('Electron'), 'an')
        self.assertEqual(guess_article('ineluctable consequence'), 'an')
        self.assertEqual(guess_article('Ouroboros'), 'an')
        self.assertEqual(guess_article('Underdark passage'), 'an')

    def test_starts_with_consonant(self):
        self.assertEqual(guess_article('rotten apple'), 'a')
        self.assertEqual(guess_article('Proton'), 'a')
        self.assertEqual(guess_article('consequence'), 'a')
        self.assertEqual(guess_article('Snake'), 'a')
        self.assertEqual(guess_article('passage'), 'a')
