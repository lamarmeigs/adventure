class Direction:
    """Describes a direction (either cardinal or relative) to place exits."""

    def __init__(self, name, abbrev):
        """Creates a new `Direction` instance.

        Arguments:
            name (str): the primary way to references this direction (eg.
                "north," "southwest," "up")
            abbrev (str): an abbreviation of the name (eg. "n", "sw", "u")
        """
        self.name = name.lower()
        self.abbrev = abbrev.lower()


class Exit:
    """Represents a connection from one location to another."""

    def __init__(self, direction, destination):
        """Creates a new `Exit` instance.

        Arguments:
            direction (`Direction`): the direction from the player where this
                exit can be found
            destination (`Location`): the location to which this exit leads
        """
        self.direction = direction
        self.destination = destination


class Location:
    """A `Location` represents a single area on a map."""

    def __init__(self, name, description, items=None, people=None, exits=None):
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
        """
        self.name = name
        self.description = description
        self.items = items or []
        self.people = people or []
        self.exits = exits or []
