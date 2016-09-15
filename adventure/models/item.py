from adventure.models.base import BaseModel


class Item(BaseModel):
    """An `Item` represents any object with which the player can interact.

    This defines a broad catch-all category for anything that has a specific
    description or actions -- anything that allows the Player to interact with
    it, separate from other defined models.
    """

    def __init__(self, name, synonym_names=None, description=None,
                 is_gettable=False, _identifier=None):
        """Creates a new `Item` instance.

        Arguments:
            name (str): the primary way to refer to this object.
            synonym_names (list of str): Any additional strings that can be
                substituted for `name`.
            description (str): a detailed description of the object.
            is_gettable (bool): indicates if the objects can be collected.
            _identifier (int): an optional unique identifier
        """
        self.name = name
        self.synonym_names = synonym_names or []
        self.description = description or ''
        self.is_gettable = is_gettable
        super().__init__(_identifier=_identifier)

    def use(self, with_items=None):
        """Activate the item's inherent utility, or use it with other items.

        Arguments:
            with_items (list | None): an optional list of other items to
                combine with this item
        """
        pass

    def serialize(self):
        """Transform this Item into a JSON-serializable dictionary.

        Return:
            a dictionary representation of self
        """
        return self.__dict__
