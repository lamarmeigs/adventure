from adventure.models.base import BaseModel


class Game(BaseModel):
    """Contains data concerning the overall game in progress."""

    def __init__(self, title, start_blurb, player, locations,
                 _identifier=None):
        """Creates a new `Game` instance.

        Arguments:
            title (str): the title of this game
            start_blurb (str): the opening scroll text to display at the start
                of a new game
            player (Player): a player object
            locations (list): all locations involved with this game
            _identifier (int): an optional unique identifier
        """
        self.title = title
        self.start_blurb = start_blurb
        self.player = player
        self.locations = locations
        self.is_over = False
        self.is_won = False
        super().__init__(_identifier=_identifier)

    def serialize(self):
        """Transform this game object into a JSON-serializable dictionary.

        Return:
            a dictionary representation of self
        """
        return {
            'title': self.title,
            'start_blurb': self.start_blurb,
            'player': self.player.reference,
            'locations': [location.reference for location in self.locations],
            '_identifier': self._identifier,
        }

    def __str__(self):
        return '<Game {}: {}>'.format(self._identifier, self.title)
