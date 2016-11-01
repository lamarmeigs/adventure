from unittest import TestCase
from unittest.mock import patch

from adventure.display.basic_text import TextOutputter


@patch('builtins.print')
class TextOutputterTestCase(TestCase):
    def setUp(self):
        self.outputter = TextOutputter()

    def test_display_location_name(self, mock_print):
        self.outputter.display_location_name('location_name')
        mock_print.assert_called_once_with('location_name')

    def test_game_text(self, mock_print):
        self.outputter.display_game_text('This is some text')
        mock_print.assert_called_once_with('This is some text')

    def test_person_reaction(self, mock_print):
        self.outputter.display_person_reaction('Jane', 'Hello!')
        mock_print.assert_called_once_with('Hello!')
