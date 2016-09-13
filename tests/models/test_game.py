from unittest import TestCase

from adventure.models.game import Game


class GameTestCase(TestCase):
    pass


class InitTestCase(GameTestCase):
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
