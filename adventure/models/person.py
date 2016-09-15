from adventure.models.base import BaseModel


class Gender(BaseModel):
    """Associates a gender with its gendered pronouns."""

    def __init__(self, gender, subject_pronoun, object_pronoun,
                 possessive_pronoun, _identifier=None):
        """Creates a new `Gender` instance.

        Arguments:
            gender (str): a simple gender descriptor (eg. male, female)
            subject_pronoun (str): pronoun to use when person is the subject of
                a sentence (eg. he, she, it, they)
            object_pronoun (str): pronoun to use when person is the object of a
                sentence (eg. him, her, it, them)
            possessive_pronoun (str): pronoun to use to describe possession of
                a noun (eg. his, her, its, their)
        """
        self.gender = gender
        self.subject_pronoun = subject_pronoun
        self.object_pronoun = object_pronoun
        self.possessive_pronoun = possessive_pronoun
        super().__init__(_identifier=_identifier)

    def serialize(self):
        """Transform this gender object into a JSON-serializable dictionary.

        Return:
            a dictionary representation of self
        """
        return self.__dict__

    def __str__(self):
        return '<Gender: {}>'.format(self.gender)


class Person(BaseModel):
    """Represents any living being with whom the player can interact."""

    def __init__(self, name, description, gender, synonym_names=None,
                 _identifier=None):
        """Creates a new `Person` instance.

        Arguments:
            name (str): the person's identifying name
            description (str): a detailed description of this person
            gender (Gender): the person's gender (for accurate pronoun usage)
            synonym_names (list | None): any additional strings that can be
                substituted for name
            _identifier (int): an optional unique identifier
        """
        self.name = name
        self.description = description
        self.gender = gender
        self.synonym_names = synonym_names or []
        super().__init__(_identifier=_identifier)

    def talk(self, subject=None):
        """Trigger a basic speech prompt.

        Arguments:
            subject (str): an optional subject matter to discuss
        """
        pass

    def serialize(self):
        """Transform this person object into a JSON-serializable dictionary.

        Return:
            a dictionary representation of self
        """
        return {
            'name': self.name,
            'description': self.description,
            'gender': self.gender.reference,
            'synonym_names': self.synonym_names,
            '_identifier': self._identifier,
        }
