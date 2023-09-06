#!/usr/bin/python3
""" Place Module for HBNB project """
from models import storage
from models.place import Place
from models.city import City
from models.user import User

city_id = '<existing city id>'
user_id = '<existing user id>'

place_attrs = {
    'city_id': city_id,
    'user_id': user_id,
    'name': 'House',
    'description': 'des',
    'number_rooms': 4,
    'number_bathrooms': 2,
    'max_guest': 6,
    'price_by_night': 100,
    'latitude': 1.3,
    'longitude': 2.3
}

new_place = Place(**place_attrs)

storage.new(new_place)
storage.save()
