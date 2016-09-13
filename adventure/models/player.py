class Player:
    """Contains all data concerning the current player."""

    def __init__(self, location, inventory=None, score=None):
        """Creates a new `Player` instance.

        Arguments:
            location (`Location`):
            inventory (list | None):
            score (int | None):
        """
        self.location = location
        self.inventory = inventory or []
        self.score = score or 0
