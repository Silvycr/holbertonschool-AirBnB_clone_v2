#!/usr/bin/python3
from sqlalchemy import (create_engine)
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from os import getenv
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity

class DBStorage:
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

        """DROP ALL TABLES"""
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Perform query on the current database session
        """
        new_dic = {}
        types_mod = [State, City, User, Place, Amenity, Review]
        if type(cls) == str:
            return new_dic
        if cls is not None and cls in types_mod:
            query_list = self.__session.query(cls).all()
            for x in query_list:
                key = "{}.{}".format(type(x).__name__, x.id)
                new_dic[key] = x
        else:
            for z in types_mod:
                query_list2 = self.__session.query(z)
                for el in query_list2:
                    key = "{}.{}".format(type(x).__name__, x.id)
                    new_dic[key] = x
        return new_dic

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
        """Create all tables in the database and create
        current database session"""
        self.__session = Base.metadata.create_all(self.__engine)
        session_a = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_a)
        self.__session = Session()

    def close(self):
        """close session, proper ending"""
        DBStorage.__session.close()
