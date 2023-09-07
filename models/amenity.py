#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import os

HBNB_TYPE_STORAGE = os.getenv('HBNB_TYPE_STORAGE')

class Amenity(BaseModel, Base if HBNB_TYPE_STORAGE == 'db' else object):
    if HBNB_TYPE_STORAGE == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
        place_amenities = relationship(
            "Place",
            secondary="place_amenity",
            viewonly=False,
            back_populates="amenities"
        )
    
    else:
        name = ""
