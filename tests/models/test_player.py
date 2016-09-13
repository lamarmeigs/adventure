from unittest import TestCase

from adventure.models import Player


class PlayerTestCase(TestCase):
    pass


class InitTestCase(PlayerTestCase):
    def test_set_parameters(self):
        player = Player(
            location='bedroom',
            inventory=['a dime', 'some lint'],
            score=50
        )
        self.assertEqual(player.location, 'bedroom')
        self.assertEqual(player.inventory, ['a dime', 'some lint'])
        self.assertEqual(player.score, 50)

    def test_default_parameters(self):
        player = Player(location='bedroom')
        self.assertEqual(player.location, 'bedroom')
        self.assertEqual(player.inventory, [])
        self.assertEqual(player.score, 0)
