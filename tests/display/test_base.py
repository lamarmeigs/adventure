from unittest import TestCase

from adventure.display.base import BaseOutputter


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
