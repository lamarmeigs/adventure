from adventure.models.base import BaseModel


class Direction(BaseModel):
    """Describes a direction (either cardinal or relative) to place exits."""

    def __init__(self, name, abbrev, _identifier=None):
        """Creates a new `Direction` instance.

        Arguments:
            name (str): the primary way to references this direction (eg.
                "north," "southwest," "up")
            abbrev (str): an abbreviation of the name (eg. "n", "sw", "u")
            _identifier (int): an optional unique identifier
        """
        self.name = name.lower()
        self.abbrev = abbrev.lower()
        super().__init__(_identifier=_identifier)

    def serialize(self):
        """Transform this direction into a JSON-serializable dictionary.

        Return:
            a dictionary representation of self
        """
        return self.__dict__


class Exit(BaseModel):
    """Represents a connection from one location to another."""

    def __init__(self, direction, destination, _identifier=None):
        """Creates a new `Exit` instance.

        Arguments:
            direction (`Direction`): the direction from the player where this
                exit can be found
            destination (`Location`): the location to which this exit leads
            _identifier (int): an optional unique identifier
        """
        self.direction = direction
        self.destination = destination
        super().__init__(_identifier=_identifier)

    def serialize(self):
        """Transform this exit into a JSON-serializable dictionary.

        Return:
            a dictionary representation of self
        """
        return {
            'direction': self.direction.reference,
            'destination': self.destination.reference,
            '_identifier': self._identifier
        }


class Location(BaseModel):
    """A `Location` represents a single area on a map."""

    def __init__(self, name, description, items=None, people=None, exits=None,
                 _identifier=None):
        """Creates a new `Location` instance.

        Arguments:
            name (str): the primary title to refer to this location
            description (str): a simple, cursory description of the location
            items (list | None): an optional list of Item objects that can be
                found at this location
            people (list | None): an optional list of Person objects that can
                be found at this location
            exits (list | None): an optional list of Exit objects, detailing
                how to leave this location for another
            _identifier (int): an optional unique identifier
        """
        self.name = name
        self.description = description
        self.items = items or []
        self.people = people or []
        self.exits = exits or []
        super().__init__(_identifier=_identifier)

    def serialize(self):
        """Transform this location object into a JSON-serializable dictionary.

        Return:
            a dictionary representation of self
        """
        return {
            'name': self.name,
            'description': self.description,
            'items': [item.reference for item in self.items],
            'people': [person.reference for person in self.people],
            'exits': [exit.reference for exit in self.exits],
            '_identifier': self._identifier,
        }
