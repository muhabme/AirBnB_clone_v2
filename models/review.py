#!/usr/bin/python3
""" Review Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class Review(BaseModel, Base):
    """Representation of Review"""
    __tablename__ = 'reviews' if getenv('HBNB_TYPE_STORAGE') == 'db' else None

    # Attributes definition based on storage type
    text = Column(String(1024), nullable=False) if getenv('HBNB_TYPE_STORAGE') == 'db' else ""
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False) if getenv('HBNB_TYPE_STORAGE') == 'db' else ""
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False) if getenv('HBNB_TYPE_STORAGE') == 'db' else ""

    def __init__(self, *args, **kwargs):
        """Initializes Review."""
        super().__init__(*args, **kwargs)
