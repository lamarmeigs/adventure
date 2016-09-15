from adventure.models.base import BaseModel


class Game(BaseModel):
    """Contains data concerning the overall game in progress."""

    def __init__(self, title, start_blurb, _identifier=None):
        """Creates a new `Game` instance.

        Arguments:
            title (str): the title of this game
            start_blurb (str): the opening scroll text to display at the start
                of a new game
            _identifier (int): an optional unique identifier
        """
        self.title = title
        self.start_blurb = start_blurb
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
            '_identifier': self._identifier,
        }
