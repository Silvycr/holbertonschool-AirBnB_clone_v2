#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
import models
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


if getenv("HBNB_TYPE_STORAGE") == 'db':

    class State(BaseModel, Base):
        """ Creating states class """
        
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref='state', 
                            cascade='all, delete')
else:
    name = ""

    @property
    def cities(self):
        """
        Getter - returns the list of City instances
        """
        from models import storage
        from models.city import City
        l_cities = []
        for city in storage.all('City').values():
            if city.state_id == self.id:
                l_cities.append(city)
        return l_cities
