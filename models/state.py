#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from os import getenv

class State(BaseModel, Base):
    """ State class, represents a geographical state in the database. """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        # DBStorage
        cities = relationship("City", backref="state", cascade="all, delete, delete-orphan")
    else:
        # FileStorage
        @property
        def cities(self):
            """Returns the list of City instances with state_id equals to the current State.id"""
            from models import storage
            all_cities = storage.all("City")
            cities_list = []
            for city in all_cities:
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

