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


class SerializedReference(dict):
    """Abstracts the assignment of one object to another.

    This allows for simpler de/serialization, as any objects existing in
    multiple locations do not need to be redundantly de/serialized. Instead,
    the object can be handled independently, while any of that object's
    assignments are represented by a SerializedReferrence.
    """

    def __init__(self, model_ref, identifier):
        """Creates a new `SerializedReference` instance.

        Arguments:
            model_ref (str): a dot-delimited path to the class being referenced
            identifier (str): a unique identifier for the object referenced
        """
        self['model_ref'] = model_ref
        self['identifier'] = identifier

    def __str__(self):
        return '<SerializedReference: {model_ref} {identifier}>'.format(
            model_ref=self['model_ref'],
            identifier=self['identifier']
        )
