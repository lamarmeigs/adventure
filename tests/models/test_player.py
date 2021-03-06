from unittest import TestCase
from unittest.mock import patch

from adventure.models import Person, Player, Location, Item


class PlayerTestCase(TestCase):
    def setUp(self):
        self.location = Location('a hole in the ground', "It's dark")

    def test_serialize(self):
        player = Player(
            location=self.location,
            inventory=[Item('torch', "It's off")],
            score=11
        )
        self.assertEqual(
            player.serialize(),
            {
                'location': player.location.reference,
                'inventory': [item.reference for item in player.inventory],
                'score': player.score,
                '_identifier': player._identifier,
            }
        )

    def test_str(self):
        player = Player(self.location, _identifier=4)
        self.assertEqual(str(player), '<Player 4>')


class InitTestCase(TestCase):
    def setUp(self):
        self.location = Location('bedroom', "It's dark")
        self.item_1 = Item('robe', 'a well-worn bathrobe')
        self.item_2 = Item('analgesic', 'a pill')

    def test_set_parameters(self):
        player = Player(
            location=self.location,
            inventory=[self.item_1, self.item_2],
            score=50
        )
        self.assertEqual(player.location, self.location)
        self.assertEqual(player.inventory, [self.item_1, self.item_2])
        self.assertEqual(player.score, 50)

    def test_default_parameters(self):
        player = Player(location=self.location)
        self.assertEqual(player.location, self.location)
        self.assertEqual(player.inventory, [])
        self.assertEqual(player.score, 0)

    def test_call_super_with_identifier(self):
        with patch('adventure.models.base.BaseModel.__init__') as mock_init:
            Player(location=self.location, _identifier=12)
        mock_init.assert_called_once_with(_identifier=12)


class FindVisibleObjectTestCase(TestCase):
    def setUp(self):
        self.location_item = Item(
            'location_item',
            synonym_names=['location_item_synonym']
        )
        self.inventory_item = Item(
            'inventory_item',
            synonym_names=['inventory_item_synonym']
        )
        self.location_person = Person('Jane', '', None)
        self.location = Location(
            name='Empty Office',
            description='Very quiet',
            people=[self.location_person],
            items=[self.location_item],
        )
        self.player = Player(
            location=self.location,
            inventory=[self.inventory_item]
        )

    def test_object_not_visible(self):
        obj = self.player.find_visible_object('not an object')
        self.assertIsNone(obj)

    def test_object_is_location(self):
        obj = self.player.find_visible_object(self.location.name)
        self.assertEqual(obj, self.location)

    def test_object_is_person_in_location(self):
        obj = self.player.find_visible_object(self.location_person.name)
        self.assertEqual(obj, self.location_person)

    def test_object_is_inventory_item(self):
        obj = self.player.find_visible_object(self.inventory_item.name)
        self.assertEqual(obj, self.inventory_item)

        obj = self.player.find_visible_object(
            self.inventory_item.synonym_names[0]
        )
        self.assertEqual(obj, self.inventory_item)

    def test_object_is_location_item(self):
        obj = self.player.find_visible_object(self.location_item.name)
        self.assertEqual(obj, self.location_item)

        obj = self.player.find_visible_object(
            self.location_item.synonym_names[0]
        )
        self.assertEqual(obj, self.location_item)
