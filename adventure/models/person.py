from adventure.exc import UnknownGenderError


class Person:
    """Represents any living being with whom the player can interact."""
    _allowed_genders = ['male', 'female', 'unspecified', 'creature']
    _pronouns = {
        'male': {
            'subject': 'he',
            'object': 'him',
            'possessive': 'his',
        },
        'female': {
            'subject': 'she',
            'object': 'her',
            'possessive': 'her',
        },
        'unspecified': {
            'subject': 'they',
            'object': 'them',
            'possessive': 'their',
        },
        'creature': {
            'subject': 'it',
            'object': 'it',
            'possessive': 'its',
        },
    }

    def __init__(self, name, description, gender, synonym_names=None):
        """Creates a new `Person` instance.

        Arguments:
            name (str): the person's identifying name
            description (str): a detailed description of this person
            gender (str): the person's gender (for accurate pronoun usage)
            synonym_names (list | None): any additional strings that can be
                substituted for name
        """
        self.name = name
        self.description = description
        self.gender = gender
        self.synonym_names = synonym_names or []

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender):
        if gender not in self._allowed_genders:
            raise UnknownGenderError(
                gender,
                context='person "{}"'.format(self.name),
                allowed_genders=self._allowed_genders
            )
        self._gender = gender

    @property
    def subject_pronoun(self):
        return self._pronouns[self.gender]['subject']

    @property
    def object_pronoun(self):
        return self._pronouns[self.gender]['object']

    @property
    def possessive_pronoun(self):
        return self._pronouns[self.gender]['possessive']

    def talk(self, subject=None):
        """Trigger a basic speech prompt.

        Arguments:
            subject (str): an optional subject matter to discuss
        """
        pass
