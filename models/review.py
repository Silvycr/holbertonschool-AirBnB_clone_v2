#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


if getenv("HBNB_TYPE_STORAGE") == 'db':
    class Review(BaseModel, Base):
        """ Review classto store review information """
        __tablename__ = "reviews"

        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        text = Column(String(1024), nullable=False)
else:
    class Review(BaseModel):
        place_id = ""
        user_id = ""
        text = ""
