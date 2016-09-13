class Game:
    """Contains data concerning the overall game in progress."""

    def __init__(self, title, start_blurb):
        """Creates a new `Game` instance."""
        self.title = title
        self.start_blurb = start_blurb
        self.is_over = False
        self.is_won = False
