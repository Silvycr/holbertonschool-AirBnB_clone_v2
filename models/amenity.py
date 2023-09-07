#!/usr/bin/python3
""" State Module for HBNB project """
import sqlalchemy
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """
    Amenity inherits from BaseModel and Base (respect the order)
    """
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    places_amenities = relationship(
        "Place",
        secondary="place_amenity")
