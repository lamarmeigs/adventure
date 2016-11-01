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


def concatenate_items(items, conjunction='and'):
    """Format a human-readable description of an iterable.

    Arguments:
        items (iterable): list of items to format
        conjunction (str): a conjunction for use in combining items

    Return:
        A text description of items, with appropriate comma and conjunctions
    """
    text = ''
    if not items:
        text = ''
    elif len(items) == 1:
        text = items[0]
    elif len(items) == 2:
        text = '{} {} {}'.format(items[0], conjunction, items[1])
    else:
        text = ', '.join(items[:-1])
        text += ', {} {}'.format(conjunction, items[-1])
    return text
