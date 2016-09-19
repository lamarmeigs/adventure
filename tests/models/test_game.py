from unittest import TestCase
from unittest.mock import patch

from adventure.models.game import Game
from adventure.models.location import Location
from adventure.models.player import Player


class GameTestCase(TestCase):
    def setUp(self):
        self.locations = [
            Location('The Beach', 'Sandy'),
            Location('The Tower', 'Cold'),
        ]
        self.player = Player(location=self.locations[0])

    def test_serialize(self):
        game = Game(
            'Serializable Game',
            'In the beginning... the end.',
            self.player,
            self.locations,
        )
        self.assertEqual(
            game.serialize(),
            {
                'title': game.title,
                'start_blurb': game.start_blurb,
                'player': game.player.reference,
                'locations': [l.reference for l in game.locations],
                '_identifier': game._identifier,
            }
        )

    def test_str(self):
        game = Game(
            'Printable Game',
            'Dullest Game Ever',
            self.player,
            self.locations,
            _identifier=99
        )
        self.assertEqual(str(game), '<Game 99: Printable Game>')


class GameInitTestCase(TestCase):
    def setUp(self):
        self.locations = [
            Location('The Beach', 'Sandy'),
            Location('The Tower', 'Cold'),
        ]
        self.player = Player(location=self.locations[0])

    def test_set_parameters(self):
        game = Game(
            title='Test Game',
            start_blurb='It was a dark and stormy night',
            player=self.player,
            locations=self.locations,
        )
        self.assertEqual(game.title, 'Test Game')
        self.assertEqual(game.start_blurb, 'It was a dark and stormy night')

    def test_default_parameters(self):
        game = Game(
            title='Test Game',
            start_blurb='It was a dark and stormy night',
            player=self.player,
            locations=self.locations,
        )
        self.assertFalse(game.is_over)
        self.assertFalse(game.is_won)

    def test_call_super_with_identifier(self):
        with patch('adventure.models.base.BaseModel.__init__') as mock_init:
            Game(
                title='Init Test',
                start_blurb='You wake up. Everything is dark',
                player=self.player,
                locations=self.locations,
                _identifier=9
            )
        mock_init.assert_called_once_with(_identifier=9)
