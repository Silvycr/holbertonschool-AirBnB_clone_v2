#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
import models
from os import getenv
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel:
    """A base class for all hbnb models"""
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        id = Column(String(60), primary_key=True, nullable=False,
                    default=lambda: str(uuid.uuid4()))
        created_at = Column(DateTime, default=datetime.utcnow,
                            nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow,
                            nullable=False)
    else:
        def __init__(self, *args, **kwargs):
            """Instatntiates a new model"""
            if not kwargs:
                self.id = str(uuid.uuid4())
                self.created_at = datetime.now()
                self.updated_at = datetime.now()
            else:
                if kwargs.get("created_at"):
                    kwargs["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.created_at = datetime.now()
                if kwargs.get("updated_at"):
                    kwargs["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.updated_at = datetime.now()
                for key, value in kwargs.items():
                    if "__class__" == key:
                        continue
                    if "id" == key:
                        self.id = value
                    else:
                        self.id = str(uuid.uuid4())
                    setattr(self, key, value)
                
                
    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in dictionary.keys():
            dictionary.pop('_sa_instance_state', None)
        return dictionary
        
    def delete(self):
        """Delete the current instance from the storage"""
        models.storage.delete(self)
