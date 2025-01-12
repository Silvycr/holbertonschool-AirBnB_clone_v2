#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv
import models


if getenv('HBNB_TYPE_STORAGE') == 'db':
    class State(BaseModel, Base):
        """
        Establish a relationship with the class City
        """
        __tablename__ = 'states'

        name = Column(String(128), nullable=False)
        cities = relationship('City', cascade='all, delete', backref='state')
else:
    class State(BaseModel):
        name = ""

        @property
        def cities(self):
            """
            Getter - returns the list of City instances
            """
            from models.city import City
            l_cities = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    l_cities.append(city)
            return l_cities
