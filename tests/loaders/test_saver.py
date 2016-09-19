from unittest import TestCase
from unittest.mock import patch

import json
import os

from adventure.loaders import GameSaver
from adventure.models import (
    Exit, Direction, Game, Gender, Item, Location, Person, Player
)


class GameSaverTestCase(TestCase):
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
        self.game_saver = GameSaver(self.game)


class InitTestCase(GameSaverTestCase):
    def test_set_parameters(self):
        game_saver = GameSaver(self.game, directory='foo/bar/baz')
        self.assertEqual(game_saver.game, self.game)
        self.assertEqual(game_saver.directory, os.path.abspath('foo/bar/baz'))

    def test_default_parameters(self):
        game_saver = GameSaver(self.game)
        self.assertEqual(game_saver.game, self.game)
        self.assertEqual(game_saver.directory, os.path.abspath('.'))


class SaveTestCase(GameSaverTestCase):
    def setUp(self):
        super().setUp()
        self.file_name = 'savefile_name'

    def tearDown(self):
        os.remove(self.game_saver.get_file_path(self.file_name))

    def test_writes_serialized_objects(self):
        mock_serialized_objs = {'foo': 'bar'}
        with patch.object(
                self.game_saver,
                '_serialize_game_objects',
                return_value=mock_serialized_objs,
        ):
            self.game_saver.save(self.file_name)
        with open(self.game_saver.get_file_path(self.file_name)) as f:
            written_data = f.read()
        self.assertEqual(written_data, json.dumps(mock_serialized_objs))


class GetFilePathTestCase(GameSaverTestCase):
    def test_file_extension(self):
        file_path = self.game_saver.get_file_path('savefile_name')
        _, extension = os.path.splitext(file_path)
        self.assertEqual(extension, '.json')

    def test_includes_directory_path(self):
        file_path = self.game_saver.get_file_path('savefile_name')
        self.assertTrue(file_path.startswith(self.game_saver.directory))


class ExtractAllGameObjectsTestCase(GameSaverTestCase):
    def test_extracts_objects(self):
        self.location.items = [self.item]
        self.location.exits = [self.exit]
        self.location.people = [self.person]
        game_objects = self.game_saver._extract_all_game_objects()
        self.assertEqual(
            game_objects,
            {
                'player': self.player,
                'people': [self.person],
                'genders': [self.gender],
                'items': [self.item],
                'locations': [self.location],
                'exits': [self.exit],
                'directions': [self.direction]
            }
        )

    def test_unique_genders(self):
        gender_1 = Gender('gender 1', '1', '1', '1')
        gender_2 = Gender('gender 2', '2', '2', '2')
        person_g1 = Person('Person 1', 'Person 1', gender_1)
        person_g1_2 = Person('Person 2', 'Person 2', gender_1)
        person_g2 = Person('Person 3', 'Person 3', gender_2)
        self.location.people = [person_g1, person_g1_2, person_g2]
        game_objects = self.game_saver._extract_all_game_objects()
        self.assertEqual(game_objects['genders'], [gender_1, gender_2])

    def test_unique_directions(self):
        direction_1 = Direction('up', 'u')
        direction_2 = Direction('down', 'd')
        exit_1 = Exit(direction_1, self.location)
        exit_2 = Exit(direction_1, self.location)
        exit_3 = Exit(direction_2, self.location)
        self.location.exits = [exit_1, exit_2, exit_3]
        game_objects = self.game_saver._extract_all_game_objects()
        self.assertEqual(
            game_objects['directions'],
            [direction_1, direction_2]
        )


class SerializeGameObjectTestCase(GameSaverTestCase):
    def test_serialized_objects(self):
        serialized = GameSaver._serialize_game_objects(
            self.game, self.player, [self.person], [self.gender], [self.item],
            [self.location], [self.exit], [self.direction]
        )
        self.assertEqual(
            serialized,
            {
                'game': self.game.serialize(),
                'player': self.player.serialize(),
                'people': [self.person.serialize()],
                'genders': [self.gender.serialize()],
                'items': [self.item.serialize()],
                'locations': [self.location.serialize()],
                'exits': [self.exit.serialize()],
                'directions': [self.direction.serialize()],
            }
        )
