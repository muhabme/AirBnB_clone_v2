#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, Integer, Float, Table, ForeignKey
from sqlalchemy.orm import relationship

# Configuration for many-to-many relationship in a database environment
if getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
                          Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False))

class Place(BaseModel, Base):
    """Representation of Place """
    __tablename__ = 'places' if getenv('HBNB_TYPE_STORAGE') == 'db' else None

    # Database-specific attributes
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False) if getenv('HBNB_TYPE_STORAGE') == 'db' else ""
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False) if getenv('HBNB_TYPE_STORAGE') == 'db' else ""
    name = Column(String(128), nullable=False) if getenv('HBNB_TYPE_STORAGE') == 'db' else ""
    description = Column(String(1024), nullable=True) if getenv('HBNB_TYPE_STORAGE') == 'db' else ""
    number_rooms = Column(Integer, default=0, nullable=False) if getenv('HBNB_TYPE_STORAGE') == 'db' else 0
    number_bathrooms = Column(Integer, default=0, nullable=False) if getenv('HBNB_TYPE_STORAGE') == 'db' else 0
    max_guest = Column(Integer, default=0, nullable=False) if getenv('HBNB_TYPE_STORAGE') == 'db' else 0
    price_by_night = Column(Integer, default=0, nullable=False) if getenv('HBNB_TYPE_STORAGE') == 'db' else 0
    latitude = Column(Float, nullable=True) if getenv('HBNB_TYPE_STORAGE') == 'db' else 0.0
    longitude = Column(Float, nullable=True) if getenv('HBNB_TYPE_STORAGE') == 'db' else 0.0
    reviews = relationship("Review", cascade="all, delete", backref="place") if getenv('HBNB_TYPE_STORAGE') == 'db' else []
    amenities = relationship("Amenity", secondary=place_amenity, viewonly=False, backref="place_amenities") if getenv('HBNB_TYPE_STORAGE') == 'db' else []

    def __init__(self, *args, **kwargs):
        """Initializes Place."""
        super().__init__(*args, **kwargs)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def reviews(self):
            """Returns the list of Review instances with place_id equals to the current Place.id."""
            return [review for review in models.storage.all("Review").values() if review.place_id == self.id]

        @property
        def amenities(self):
            """Returns the list of Amenity instances with place_id equals to the current Place.id."""
            return [amenity for amenity in models.storage.all("Amenity").values() if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """Manages addition of an amenity via amenity_ids."""
            if type(obj).__name__ == "Amenity":
                self.amenity_ids.append(obj.id)
