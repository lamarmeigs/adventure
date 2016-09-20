from unittest import TestCase
from unittest.mock import patch
import json
import os

from adventure.loaders import GameLoader
from adventure.models import (
    Exit, Direction, Game, Gender, Item, Location, Person, Player
)


class GameLoaderTestCase(TestCase):
    def setUp(self):
        self.item = Item('thing')
        self.gender = Gender('dinosaur', 'it', 'rawr', 'grhm?')
        self.person = Person('Macbeth', 'Shifty guy', self.gender)
        self.location = Location('Place A', 'This is place A.')
        self.direction = Direction('backwards', 'b')
        self.exit = Exit(self.direction, self.location)
        self.player = Player(location=self.location)
        self.game = Game(
            'Serializable Game',
            'Once upon a time',
            player=self.player,
            locations=[self.location],
        )
        self.loader = GameLoader()


class InitTestCase(GameLoaderTestCase):
    def test_set_parameters(self):
        loader = GameLoader(directory='foo/bar/baz')
        self.assertEqual(loader.directory, os.path.abspath('foo/bar/baz'))

    def test_default_parameters(self):
        loader = GameLoader()
        self.assertEqual(loader.directory, os.path.abspath('.'))


class LoadTestCase(GameLoaderTestCase):
    @classmethod
    def setUpClass(cls):
        cls.file_contents = {'foo': 'bar'}
        cls.file_name = 'test_loadfile'
        cls.file_path = GameLoader().get_file_path(cls.file_name)
        with open(cls.file_path, 'w') as f:
            f.write(json.dumps(cls.file_contents))

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.file_path)

    def test_loads_json_from_file(self):
        with patch.object(
                self.loader,
                '_reconstitute_all_game_objects',
                return_value=self.game,
        ) as mock_reconstitute:
            loaded_game = self.loader.load(self.file_name)
        mock_reconstitute.assert_called_once_with(self.file_contents)
        self.assertEqual(loaded_game, self.game)


class GetFilePathTestCase(GameLoaderTestCase):
    def test_file_extension(self):
        file_path = self.loader.get_file_path('file_name')
        _, extension = os.path.splitext(file_path)
        self.assertEqual(extension, '.json')

    def test_includes_directory_path(self):
        file_path = self.loader.get_file_path('file_name')
        self.assertTrue(file_path.startswith(self.loader.directory))


class ReconstituteAllGameObjectsTestCase(GameLoaderTestCase):
    def setUp(self):
        super().setUp()
        self.serialized_objects = {
            'directions': [self.direction.serialize()],
            'genders': [self.gender.serialize()],
            'items': [self.item.serialize()],
            'game': self.game.serialize(),
            'player': self.player.serialize(),
            'people': [self.person.serialize()],
            'locations': [self.location.serialize()],
            'exits': [self.exit.serialize()],
        }

    def test_delegates_simple_and_complex_objects(self):
        mock_simple_objects = [[self.direction], [self.gender], [self.item]]
        mock_game = 'game'
        with patch.object(
                GameLoader,
                '_reconstitute_simple_objects',
                return_value=mock_simple_objects,
        ) as mock_simple_reconstitute:
            with patch.object(
                    GameLoader,
                    '_reconstitute_complex_objects',
                    return_value=mock_game,
            ) as mock_complex_reconstitute:
                rebuilt_game = self.loader._reconstitute_all_game_objects(
                    self.serialized_objects
                )
        self.assertEqual(rebuilt_game, mock_game)
        mock_simple_reconstitute.assert_called_once_with(
            self.serialized_objects['directions'],
            self.serialized_objects['genders'],
            self.serialized_objects['items']
        )
        mock_complex_reconstitute.assert_called_once_with(
            self.serialized_objects['game'],
            self.serialized_objects['player'],
            self.serialized_objects['people'],
            self.serialized_objects['locations'],
            self.serialized_objects['exits'],
            *mock_simple_objects
        )


class ReconstituteSimpleObjectsTestCase(GameLoaderTestCase):
    def test_creates_directions(self):
        directions, _, _ = GameLoader()._reconstitute_simple_objects(
            directions=[
                {'name': 'north', 'abbrev': 'n'},
                {'name': 'south', 'abbrev': 's'},
            ],
            genders=[],
            items=[],
        )
        self.assertEqual(len(directions), 2)
        self.assertEqual(directions[0].name, 'north')
        self.assertEqual(directions[0].abbrev, 'n')
        self.assertEqual(directions[1].name, 'south')
        self.assertEqual(directions[1].abbrev, 's')

    def test_creates_genders(self):
        _, genders, _ = GameLoader()._reconstitute_simple_objects(
            directions=[],
            genders=[
                {
                    'gender': 'creature',
                    'subject_pronoun': 'it',
                    'object_pronoun': 'it',
                    'possessive_pronoun': 'it',
                },
                {
                    'gender': 'unspecified',
                    'subject_pronoun': 'they',
                    'object_pronoun': 'them',
                    'possessive_pronoun': 'their',
                },
            ],
            items=[],
        )
        self.assertEqual(len(genders), 2)
        self.assertEqual(genders[0].gender, 'creature')
        self.assertEqual(genders[0].subject_pronoun, 'it')
        self.assertEqual(genders[0].object_pronoun, 'it')
        self.assertEqual(genders[0].possessive_pronoun, 'it')
        self.assertEqual(genders[1].gender, 'unspecified')
        self.assertEqual(genders[1].subject_pronoun, 'they')
        self.assertEqual(genders[1].object_pronoun, 'them')
        self.assertEqual(genders[1].possessive_pronoun, 'their')

    def test_creates_items(self):
        _, _, items = GameLoader()._reconstitute_simple_objects(
            directions=[],
            genders=[],
            items=[{'name': 'hammer'}, {'name': 'sickle'}],
        )
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].name, 'hammer')
        self.assertEqual(items[1].name, 'sickle')


class ReconstituteComplexObjectsTestCase(GameLoaderTestCase):
    def test_creates_game(self):
        game = GameLoader._reconstitute_complex_objects(
            self.game.serialize(),
            self.player.serialize(),
            [self.person.serialize()],
            [self.location.serialize()],
            [self.exit.serialize()],
            [self.direction],
            [self.gender],
            [self.item],
        )
        self.assertEqual(game, self.game)

    def test_creates_player(self):
        self.game.player = self.player
        game = GameLoader._reconstitute_complex_objects(
            self.game.serialize(),
            self.player.serialize(),
            [self.person.serialize()],
            [self.location.serialize()],
            [self.exit.serialize()],
            [self.direction],
            [self.gender],
            [self.item],
        )
        self.assertEqual(game.player, self.player)

    def test_creates_locations(self):
        self.game.locations = [self.location]
        game = GameLoader._reconstitute_complex_objects(
            self.game.serialize(),
            self.player.serialize(),
            [self.person.serialize()],
            [self.location.serialize()],
            [self.exit.serialize()],
            [self.direction],
            [self.gender],
            [self.item],
        )
        self.assertIn(self.location, game.locations)

    def test_creates_people(self):
        self.location.people = [self.person]
        self.game.locations = [self.location]
        game = GameLoader._reconstitute_complex_objects(
            self.game.serialize(),
            self.player.serialize(),
            [self.person.serialize()],
            [self.location.serialize()],
            [self.exit.serialize()],
            [self.direction],
            [self.gender],
            [self.item],
        )
        self.assertEqual(len(game.locations), 1)
        self.assertIn(self.person, game.locations[0].people)

    def test_creates_exits(self):
        self.location.exits = [self.exit]
        self.game.locations = [self.location]
        game = GameLoader._reconstitute_complex_objects(
            self.game.serialize(),
            self.player.serialize(),
            [self.person.serialize()],
            [self.location.serialize()],
            [self.exit.serialize()],
            [self.direction],
            [self.gender],
            [self.item],
        )
        self.assertEqual(len(game.locations), 1)
        self.assertIn(self.exit, game.locations[0].exits)

    def test_creates_items(self):
        self.location.items = [self.item]
        self.player.inventory = [self.item]
        self.game.locations = [self.location]
        self.game.player = self.player
        game = GameLoader._reconstitute_complex_objects(
            self.game.serialize(),
            self.player.serialize(),
            [self.person.serialize()],
            [self.location.serialize()],
            [self.exit.serialize()],
            [self.direction],
            [self.gender],
            [self.item],
        )
        self.assertIn(self.item, game.player.inventory)
        self.assertEqual(len(game.locations), 1)
        self.assertIn(self.item, game.locations[0].items)
