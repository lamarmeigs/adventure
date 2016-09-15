from unittest import TestCase
from unittest.mock import patch

from adventure.models import Item, Person
from adventure.models.location import Direction, Exit, Location


class DirectionTestCase(TestCase):
    def test_init_sets_lowercase_parameters(self):
        north = Direction(name='North', abbrev='N')
        self.assertEqual(north.name, 'north')
        self.assertEqual(north.abbrev, 'n')

    def test_init_calls_super_with_identifier(self):
        with patch('adventure.models.base.BaseModel.__init__') as mock_init:
            Direction(name='up', abbrev='u', _identifier=7)
        mock_init.assert_called_once_with(_identifier=7)

    def test_serialize(self):
        southwest = Direction(name='southwest', abbrev='sw')
        self.assertEqual(
            southwest.serialize(),
            {
                'name': 'southwest',
                'abbrev': 'sw',
                '_identifier': southwest._identifier,
            }
        )


class ExitTestCase(TestCase):
    def setUp(self):
        self.direction = Direction('left', 'l')
        self.destination = Location('backstage', "It's full of props")

    def test_init_sets_parameters(self):
        stage_left = Exit(
            direction=self.direction,
            destination=self.destination
        )
        self.assertEqual(stage_left.direction, self.direction)
        self.assertEqual(stage_left.destination, self.destination)

    def test_init_calls_super_with_identifier(self):
        with patch('adventure.models.base.BaseModel.__init__') as mock_init:
            Exit(self.direction, self.destination, _identifier=16)
        mock_init.assert_called_once_with(_identifier=16)

    def test_serialize(self):
        exit = Exit(
            direction=self.direction,
            destination=self.destination
        )
        self.assertEqual(
            exit.serialize(),
            {
                'direction': exit.direction.reference,
                'destination': exit.destination.reference,
                '_identifier': exit._identifier,
            }
        )


class LocationTestCase(TestCase):
    def test_serialize(self):
        some_exit = Exit(
            Direction('east', 'e'),
            Location('Outside', "It's painfully bright and full of people")
        )
        location = Location(
            name='Living Room',
            description="It's a mess",
            items=[Item('thing')],
            people=[Person('Bob', "It's Bob", 'unspecified')],
            exits=[some_exit]
        )
        self.assertEqual(
            location.serialize(),
            {
                'name': location.name,
                'description': location.description,
                'items': [item.reference for item in location.items],
                'people': [person.reference for person in location.people],
                'exits': [exit.reference for exit in location.exits],
                '_identifier': location._identifier,
            }
        )


class LocationInitTestCase(TestCase):
    def test_set_parameters(self):
        location = Location(
            name='Dark Cave',
            description="Don't get eaten by a grue",
            items=['rock', 'stalactite'],
            people=['Grue'],
            exits=['n', 'w'],
        )
        self.assertEqual(location.name, 'Dark Cave')
        self.assertEqual(location.description, "Don't get eaten by a grue")
        self.assertEqual(location.items, ['rock', 'stalactite'])
        self.assertEqual(location.people, ['Grue'])
        self.assertEqual(location.exits, ['n', 'w'])

    def test_default_parameters(self):
        location = Location(
            name='Empty Field',
            description="There's nothing here"
        )
        self.assertEqual(location.name, 'Empty Field')
        self.assertEqual(location.description, "There's nothing here")
        self.assertEqual(location.items, [])
        self.assertEqual(location.people, [])
        self.assertEqual(location.exits, [])

    def test_call_super_with_identifer(self):
        with patch('adventure.models.base.BaseModel.__init__') as mock_init:
            Location('Dungeon', 'Ew, was that a rat?', _identifier=27)
        mock_init.assert_called_once_with(_identifier=27)
