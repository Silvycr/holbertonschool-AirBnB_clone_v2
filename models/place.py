#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv

    
if getenv("HBNB_TYPE_STORAGE") == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                           Column('place_id', String(60),
                                   ForeignKey('places.id'),
                                   primary_key=True, nullable=False),
                            Column('amenity_id', String(60),
                                    ForeignKey('amenities.id'),
                                    primary_key=True, nullable=False))
        
    class Place(BaseModel, Base):
        
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", backref='place',
                                cascade='all, delete, delete-orphan')
        amenities = relationship("Amenity", secondary=place_amenity, 
                                  back_populates="place_amenities",
                                  viewonly=False)
else:
    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
    
    @property
    def reviews(self):
        """
        the getter attribute reviews returns
        the list of Review.
        """
        from models.review import Review
        from models import storage
        r = []
        all_reviews = storage.all(Review)
        for v in all_reviews.values():
            if v.place_id == self.id:
                r.append(v)
        return r

    @property
    def amenities(self):
        """
        Getter attribute amenities that returns the list of Amenity instances
        based on the attribute amenity id.
        """

        return self._amenities

    @amenities.setter
    def amenities(self, obj):
        if obj.__class__.__name__ == "Amenity":
            amenity_ids.append(obj.id)
        else:
            pass
