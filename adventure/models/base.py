from abc import ABCMeta


class BaseModel(metaclass=ABCMeta):
    """A base model providing common functionality expected of all models."""

    # Class attribute to track the number of instantiated objects of this
    # particular class.
    COUNT = 0

    def __init__(self, *args, **kwargs):
        """Create a new instance of this class.

        Increment the COUNT for this class, and assign the latest value to the
        `_identifier` attribute. Though not guaranteed to be unique, this
        should function as a poor-man's auto-incrementing primary key.
        """
        self.__class__.COUNT += 1
        self._identifier = self.__class__.COUNT

    def serialize(self):
        """Transform this model object into a JSON-serializable dictionary.

        Return:
            a dictionary representation of self
        """
        raise NotImplementedError()
