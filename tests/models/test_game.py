from unittest import TestCase
from unittest.mock import patch

from adventure.models.game import Game


class GameTestCase(TestCase):
    def test_serialize(self):
        game = Game('Serializable Game', 'In the beginning... the end.')
        self.assertEqual(
            game.serialize(),
            {
                'title': game.title,
                'start_blurb': game.start_blurb,
                '_identifier': game._identifier,
            }
        )

    def test_str(self):
        game = Game('Printable Game', 'Dullest Game Ever', _identifier=99)
        self.assertEqual(str(game), '<Game 99: Printable Game>')


class InitTestCase(TestCase):
    def test_set_parameters(self):
        game = Game(
            title='Test Game',
            start_blurb='It was a dark and stormy night'
        )
        self.assertEqual(game.title, 'Test Game')
        self.assertEqual(game.start_blurb, 'It was a dark and stormy night')

    def test_default_parameters(self):
        game = Game(
            title='Test Game',
            start_blurb='It was a dark and stormy night'
        )
        self.assertFalse(game.is_over)
        self.assertFalse(game.is_won)

    def test_call_super_with_identifier(self):
        with patch('adventure.models.base.BaseModel.__init__') as mock_init:
            Game(
                title='Init Test',
                start_blurb='You wake up. Everything is dark',
                _identifier=9
            )
        mock_init.assert_called_once_with(_identifier=9)
