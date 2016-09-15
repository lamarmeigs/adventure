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
