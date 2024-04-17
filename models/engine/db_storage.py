#!/usr/bin/python3
""" DBStorage Module for HBNB project """
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os import getenv

class DBStorage:
    """This class manages storage of hbnb models in a MySQL database."""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the DBStorage instance."""
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')

        # Database engine setup
        self.__engine = create_engine(f'mysql+mysqldb://{user}:{password}@{host}/{db}',
                                      pool_pre_ping=True)
        
        # Drop all tables if in test environment
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects in the database by class name; if no class specified, query all."""
        from models.base_model import Base
        from sqlalchemy.orm import joinedload
        result_dict = {}
        if cls:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = f"{obj.__class__.__name__}.{obj.id}"
                result_dict[key] = obj
        else:
            # List all classes that inherit from Base
            classes = Base._decl_class_registry.values()
            for cls in classes:
                objs = self.__session.query(cls).options(joinedload('*')).all()
                for obj in objs:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    result_dict[key] = obj
        return result_dict

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

    def reload(self):
        """Create all tables in the database and initialize a new session."""
        from models.base_model import Base
        # Import all necessary classes here
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        ScopedSession = scoped_session(session_factory)
        self.__session = ScopedSession()
