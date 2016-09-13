from unittest import TestCase

from adventure.models.location import Direction, Exit, Location


class DirectionTestCase(TestCase):
    def test_init_sets_lowercase_parameters(self):
        north = Direction(name='North', abbrev='N')
        self.assertEqual(north.name, 'north')
        self.assertEqual(north.abbrev, 'n')


class ExitTestCase(TestCase):
    def test_init_sets_parameters(self):
        left = Direction('left', 'l')
        backstage = Location('backstage', "It's full of props")
        stage_left = Exit(direction=left, destination=backstage)
        self.assertEqual(stage_left.direction, left)
        self.assertEqual(stage_left.destination, backstage)


class LocationTestCase(TestCase):
    pass


class InitTestCase(LocationTestCase):
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
