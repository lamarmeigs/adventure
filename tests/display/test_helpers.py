from unittest import TestCase

from adventure.display.helpers import concatenate_items


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
