import json
import os
from copy import copy


class GameSaver:
    """Manages writing game data to a file."""

    def __init__(self, game, directory=None):
        """Creates a new `GameSaver` instance.

        Arguments:
            game (`Game`): the game object to be saved
            directory (str): an optional path to the directory in which to
                write files (by default, the current working directory)
        """
        self.game = game
        directory = directory or '.'
        self.directory = os.path.abspath(directory)

    def save(self, file_name):
        """Write the game state to the given file_path.

        Arguments:
            file_name (str): the name of file to write (extension excluded)
        """
        game_objs = self._extract_all_game_objects()
        serialized_objs = self._serialize_game_objects(self.game, *game_objs)

        finalized_path = self.get_file_path(file_name)
        with open(finalized_path, 'w') as save_file:
            save_file.write(json.dumps(serialized_objs))

    def get_file_path(self, file_name):
        """Return the full file path to a file with the given name.

        Arguments:
            file_name (str): name of the file whose path to return

        Return:
            a str representing the path to the named file
        """
        finalized_file_name = '{}.json'.format(file_name)
        finalized_path = os.path.join(self.directory, finalized_file_name)
        return finalized_path

    def _extract_all_game_objects(self):
        """Recurse through the game object, extracting all related objects.

        Return:
            a flat dictionary containing all objects associated with game
        """
        items = copy(self.game.player.inventory)
        people = []
        exits = []
        for location in self.game.locations:
            items += location.items
            exits += location.exits
            people += location.people
        genders = list(set([person.gender for person in people]))
        directions = list(set([exit.direction for exit in exits]))
        return {
            'player': self.game.player,
            'people': people,
            'genders': genders,
            'items': items,
            'locations': self.game.locations,
            'exits': exits,
            'directions': directions,
        }

    @staticmethod
    def _serialize_game_objects(
            game, player, people, genders, items, locations, exits, directions
    ):
        """Serialize all the given objects into a single dict.

        Arguments:
            game (`Game`): a game object
            player (`Player`): a player object
            genders (list): a list of gender objects
            items (list): a list of Item objects
            locations (list): a list of Location objects
            exits (list): a list of Exit objects
            direction (list): a list of Direction objects

        Return:
            a dict with the serialized representations of all objects
        """
        content = {
            'game': game.serialize(),
            'player': player.serialize(),
            'people': [person.serialize() for person in people],
            'genders': [gender.serialize() for gender in genders],
            'items': [item.serialize() for item in items],
            'locations': [location.serialize() for location in locations],
            'exits': [exit.serialize() for exit in exits],
            'directions': [direction.serialize() for direction in directions],
        }
        return content
