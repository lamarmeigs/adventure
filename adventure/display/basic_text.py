from adventure.display.base import BaseOutputter


class TextOutputter(BaseOutputter):
    """A basic text renderer that prints parameters to stdout"""

    def display_location_name(self, location_name):
        print(location_name)

    def display_game_text(self, text):
        print(text)

    def display_person_reaction(self, person_name, text):
        print(text)
