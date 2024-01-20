#!/usr/bin/python3
"""Defines the Amenity class."""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Represent an amenity.

    Attributes:
        name (str): The name of the amenity.
    """

    def __init__(self, *args, **kwargs):
        """Initialize a new Amenity.

        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        super().__init__(*args, **kwargs)
        self.name = ""

    def to_dict(self):
        """Return the dictionary of the Amenity instance.

        Includes the key/value pair __class__ representing
        the class name of the object.
        """
        rdict = super().to_dict()
        rdict["name"] = self.name
        return rdict

    def __str__(self):
        """Return the print/str representation of the Amenity instance."""
        clname = self.__class__.__name__
        return "[{}] ({}) {}".format(clname, self.id, self.__dict__)
