#!/usr/bin/python3
""" Module holds class Amenity"""
import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class Amenity(BaseModel, Base):
    """Representation of Amenity"""
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128),
                      nullable=False)

    def __init__(self, *args, **kwargs):
        """Initializes Amenity."""
        super().__init__(*args, **kwargs)

