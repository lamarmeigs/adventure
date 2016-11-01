from unittest import TestCase

from adventure.display.base import BaseOutputter, concatenate_items


class DummyOutputter(BaseOutputter):
    def display_location_name(self, location_name):
        super().display_location_name(location_name)

    def display_game_text(self, text):
        super().display_game_text(text)

    def display_person_reaction(self, person_name, text):
        super().display_person_reaction(person_name, text)


class BaseOutputterTestCase(TestCase):
    def setUp(self):
        self.dummy = DummyOutputter()

    def test_display_location_name_raises_error(self):
        with self.assertRaises(NotImplementedError):
            self.dummy.display_location_name('location_name')

    def test_display_game_text_raises_error(self):
        with self.assertRaises(NotImplementedError):
            self.dummy.display_game_text('This is some text')

    def test_display_person_reaction(self):
        with self.assertRaises(NotImplementedError):
            self.dummy.display_person_reaction('Jane', 'Hello!')


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
