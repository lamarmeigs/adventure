class Item:
    """An `Item` represents any object with which the player can interact.

    This defines a broad catch-all category for anything that has a specific
    description or actions -- anything that allows the Player to interact with
    it separate from other defined models.
    """

    def __init__(self, name, synonym_names=None, description=None,
                 is_gettable=False):
        """Creates a new `Item` instance.

        Arguments:
            name (str): the primary way to refer to this object.
            synonym_names (list of str): Any additional strings that can be
                substituted for `name`.
            description (str): a detailed description of the object.
            is_gettable (bool): indicates if the objects can be collected.
            kwargs (dict): any additional instance attributes to set
        """
        self.name = name
        self.synonym_names = synonym_names or []
        self.description = description or ''
        self.is_gettable = is_gettable

    def use(self, with_items=None):
        """Activate the item's inherent utility, or use it with other items.

        Arguments:
            with_items (list | None): an optional list of other items to
                combine with this item
        """
        pass
