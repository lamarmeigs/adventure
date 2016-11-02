from abc import ABCMeta, abstractmethod


class BaseOutputter(metaclass=ABCMeta):
    """An abstract base class to establish outputter methods"""

    @abstractmethod
    def display_location_name(self, location_name):
        """Display the name of the player's current location"""
        raise NotImplementedError()

    @abstractmethod
    def display_game_text(self, text):
        """Display generic, non-specific game text"""
        raise NotImplementedError()

    @abstractmethod
    def display_person_reaction(self, person_name, text):
        """Display speech from the named person"""
        raise NotImplementedError()
