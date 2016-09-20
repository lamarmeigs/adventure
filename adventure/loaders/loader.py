import json
import os

from adventure.models import (
    Direction, Exit, Item, Game, Gender, Location, Person, Player
)


class GameLoader:
    """Manages read game data from a file."""

    def __init__(self, directory=None):
        """Creates a new `GameLoader` instance.

        Arguments:
            directory (str): an optional path to the directory from which to
                read files (by default, the current worker directory)
        """
        directory = directory or '.'
        self.directory = os.path.abspath(directory)

    def load(self, file_name):
        """Read & interpret serialized game data from a file.

        Arguments:
            file_name (str): name of the file to read (excluding extension)

        Return:
            a Game object
        """
        finalized_path = self.get_file_path(file_name)
        with open(finalized_path) as load_file:
            serialized_objs = json.loads(load_file.read())

        game = self._reconstitute_all_game_objects(serialized_objs)
        return game

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

    @classmethod
    def _reconstitute_all_game_objects(cls, serialized_objects):
        """Instantiate game objects from the contents of a given dict.

        Arguments:
            serialized_objects (dict): a dictionary containing all game data in
                the following keys: game, player, people, genders, items,
                locations, exits, directions

        Return:
            a Game object
        """
        directions, genders, items = cls._reconstitute_simple_objects(
            serialized_objects['directions'],
            serialized_objects['genders'],
            serialized_objects['items'],
        )
        game = cls._reconstitute_complex_objects(
            serialized_objects['game'],
            serialized_objects['player'],
            serialized_objects['people'],
            serialized_objects['locations'],
            serialized_objects['exits'],
            directions,
            genders,
            items
        )
        return game

    @staticmethod
    def _reconstitute_simple_objects(directions, genders, items):
        """Instantiate game objects that contain no serialized references.

        Arguments:
            directions (list): a list of serialized Direction objects
            genders (list): a list of serialized Gender objects
            items (list): a list of serialized Item objects

        Return:
            a 3-tuple of (list of Directions, list of Genders, list of Items)
        """
        directions = [Direction(**direction) for direction in directions]
        genders = [Gender(**gender) for gender in genders]
        items = [Item(**item) for item in items]
        return directions, genders, items

    @staticmethod
    def _reconstitute_complex_objects(
            serialized_game, serialized_player, serialized_people,
            serialized_locations, serialized_exits, directions, genders, items
    ):
        """Instantiate game objects that contain serialized references.

        Arguments:
            serialized_game (dict): a serialized game
            serialized_player (dict): a serialzied player
            serialized_people (list): a list of serialized persons
            serialized_locations (list): a list of serialized locations
            serialized_exits (list): a list of serialized exits
            directions (list): a list of instantiated Direction objects
            genders (list): a list of instantiated Gender objects
            items (list): a list of instantiated Item objects

        Return:
            an instantiation Game object
        """
        # Format instantiated objects in dictionaries for quick lookup
        directions = {d._identifier: d for d in directions}
        genders = {gender._identifier: gender for gender in genders}
        items = {item._identifier: item for item in items}

        people = {}
        for serialized_person in serialized_people:
            gender_reference = serialized_person.pop('gender')
            gender = genders.get(gender_reference['identifier'])
            person = Person(gender=gender, **serialized_person)
            people[person._identifier] = person

        exits = {}
        for serialized_exit in serialized_exits:
            direction_reference = serialized_exit.pop('direction')
            direction = directions.get(direction_reference['identifier'])
            exit = Exit(direction=direction, **serialized_exit)
            exits[exit._identifier] = exit

        locations = {}
        for serialized_location in serialized_locations:
            exit_refs = serialized_location.pop('exits')
            item_refs = serialized_location.pop('items')
            people_refs = serialized_location.pop('people')
            location_exits = [exits[ref['identifier']] for ref in exit_refs]
            location_items = [items[ref['identifier']] for ref in item_refs]
            location_people = [
                people[ref['identifier']] for ref in people_refs
            ]
            location = Location(
                exits=location_exits,
                items=location_items,
                people=location_people,
                **serialized_location
            )
            locations[location._identifier] = location

        for _, exit in exits.items():
            location_id = exit.destination['identifier']
            location = locations[location_id]
            exit.destination = location

        location_reference = serialized_player.pop('location')
        inventory_refs = serialized_player.pop('inventory')
        player_location = locations[location_reference['identifier']]
        player_inventory = [items[ref['identifier']] for ref in inventory_refs]
        player = Player(
            location=player_location,
            inventory=player_inventory,
            **serialized_player
        )

        serialized_game.pop('player')
        serialized_game.pop('locations')
        game = Game(
            player=player,
            locations=list(locations.values()),
            **serialized_game
        )
        return game
