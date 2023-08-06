class NodeProperty:
    """Scinode property.

    When variable is saved to a database, the type of the variable will
    be lost. We use this Property Class to label the type of the data,
    thus we can restore the data from database.

    The identifier is also helpful for the Editor to show the data in the
    GUI.
    """

    identifier = "NodeProperty"

    def __init__(self, name, description="", default=None, update=None) -> None:
        """_summary_

        Args:
            name (str): name of the varible
            options (list, optional): options of the varible. Defaults to [].
            description (str, optional): _description_. Defaults to "".
            default (_type_, optional): _description_. Defaults to None.
            extra (dict, optional): extra data, e.g. size for a vector. Defaults to {}.
            update (function, optional): The callback function when
                udpate the item. Defaults to None.
        """
        self.name = name
        self.description = description
        self.default = default
        self.update = update
        self._value = self.default

    def to_dict(self):
        """Data to be saved to database."""
        data = {
            "value": self.value,
            "name": self.name,
            "identifier": self.identifier,
            "serialize": self.get_serialize(),
            "deserialize": self.get_deserialize(),
            "metadata": self.get_metadata(),
        }
        return data

    def get_metadata(self):
        metadata = {"default": self.default}
        return metadata

    @classmethod
    def from_dict(cls, data):
        p = cls(data["name"])
        p.identifier = data["identifier"]
        p.value = data["value"]
        return p

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self.set_value(value)

    def set_value(self, value):
        # run the callback function
        self._value = value
        if self.update is not None:
            self.update()

    def copy(self):
        p = self.__class__(self.name, self.description, self.value, self.update)
        p.value = self.value
        return p

    def __str__(self):
        return '{}(name="{}", value={})'.format(
            self.__class__.__name__, self.name, self._value
        )

    def __repr__(self):
        return '{}(name="{}", value={})'.format(
            self.__class__.__name__, self.name, self._value
        )
