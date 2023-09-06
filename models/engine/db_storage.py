#!/usr/bin/python3
"""
Defines a new engine of storage
Database mode, to be used with SQLAlchemy
"""
from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session, sessionmaker, scoped_session


class DBStorage:
    """
    Create our database with SQLAlchemy
    Alchemy is our best friend!
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Starting the engine
        """
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, pwd, host, db),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Perform query on the current database session
        # Must return a dictionary with all objects according
        to class name passed in cls argument
        """
        obj_dict = {}
        if cls is not None:
            objs = self.__session.query(cls).all()
        else:
            objs = self.__session.query(Amenity)
            # We could have used extend() list method too,
            # but would have needed another way to code also
            objs += self.__session.query(City)
            objs += self.__session.query(Place)
            objs += self.__session.query(Review)
            objs += self.__session.query(State)
            objs += self.__session.query(User)
        return {"{}.{}".format(obj.__class__.__name__, obj.id): obj
                for obj in objs}

    def new(self, obj):
        """Adds the object to the current db session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to current db session"""
        self.__session.commit()

    def delete(self, obj):
        """ Delete obj of current db session """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        Commit all changes in database after
        the changings
        """

        from models.base_model import BaseModel, Base
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

        Base.metadata.create_all(self.__engine)

    def close(self):
        """close session, proper ending"""
        DBStorage.__session.remove()
