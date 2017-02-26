from adventure.models.base import BaseModel


class Player(BaseModel):
    """Contains all data concerning the current player."""

    def __init__(self, location, inventory=None, score=None, _identifier=None):
        """Creates a new `Player` instance.

        Arguments:
            location (`Location`): the current location of the player
            inventory (list | None): an optional list of Item objects
            score (int | None): an optional score (default: 0)
        """
        self.location = location
        self.inventory = inventory or []
        self.score = score or 0
        super().__init__(_identifier=_identifier)

    def find_visible_object(self, obj_name):
        """Given the name of an object, return the object if it is visible.

        Arguments:
            obj_name (str): name of an object visible to the player

        Returns:
            the object matching obj_name or None
        """
        visible_people = self.location.people
        visible_items = self.inventory + self.location.items

        named_people = {}
        for person in visible_people:
            named_people[person.name] = person
            named_people.update(
                {name: person for name in person.synonym_names}
            )

        named_items = {}
        for item in visible_items:
            named_items[item.name] = item
            named_items.update({name: item for name in item.synonym_names})

        obj = None
        if obj_name == self.location.name:
            obj = self.location
        elif obj_name in named_people.keys():
            obj = named_people[obj_name]
        elif obj_name in named_items.keys():
            obj = named_items[obj_name]
        return obj

    def serialize(self):
        """Transform this player object into a JSON-serializable dictionary.

        Return:
            a dictionary representation of self
        """
        return {
            'location': self.location.reference,
            'inventory': [item.reference for item in self.inventory],
            'score': self.score,
            '_identifier': self._identifier,
        }

    def __str__(self):
        return '<Player {}>'.format(self._identifier)
