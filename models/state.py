#!/usr/bin/python3
"""
Defines the State class
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from os import getenv
import models


class State(BaseModel, Base):
    """
    Represents a state
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """
            Getter for cities
            """
            cities = models.storage.all(models.City)
            return [city for city in cities.values() if
                    city.state_id == self.id]
