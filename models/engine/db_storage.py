#!/usr/bin/python3
""" DBStorage Module for HBNB project """
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User

# Mapping from class names to classes
class_name_map = {
    'Amenity': Amenity,
    'City': City,
    'Place': Place,
    'State': State,
    'Review': Review,
    'User': User
}

class DBStorage:
    """This class manages storage of hbnb models in a MySQL database."""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the DBStorage instance."""
        user = os.getenv('HBNB_MYSQL_USER')
        passwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        
        # Database engine setup
        self.__engine = create_engine(f'mysql+mysqldb://{user}:{passwd}@{host}/{db}',
                                      pool_pre_ping=True)
        
        # Drop all tables if in test environment
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects in the database by class name; if no class specified, query all."""
        if cls and isinstance(cls, str):
            cls = class_name_map.get(cls, None)
        result_dict = {}
        if cls:
            for obj in self.__session.query(cls):
                key = f"{obj.__class__.__name__}.{obj.id}"
                result_dict[key] = obj
        else:
            for model_cls in class_name_map.values():
                for obj in self.__session.query(model_cls):
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    result_dict[key] = obj
        return result_dict

    def reload(self):
        """Create all tables in the database and initialize a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def new(self, obj):
        """Add the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object from the current database session if not None."""
        if obj:
            self.__session.delete(obj)

    def close(self):
        """Dispose of current session if active"""
        self.__session.remove()

    def get(self, cls, id):
        """Retrieve an object by class and id."""
        if cls and isinstance(cls, str) and id:
            cls = class_name_map.get(cls, None)
            return self.__session.query(cls).filter(cls.id == id).first()
        return None

    def count(self, cls=None):
        """Count number of objects in storage by class, or total if no class specified."""
        if cls and isinstance(cls, str):
            cls = class_name_map.get(cls, None)
            return self.__session.query(cls).count()
        elif cls is None:
            total = sum(self.__session.query(model_cls).count() for model_cls in class_name_map.values())
            return total
        return 0
