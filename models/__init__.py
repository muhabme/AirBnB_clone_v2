#!/usr/bin/python3
"""This module instantiates an object of the selected storage class based on an environment variable"""
from os import getenv

# Determine the type of storage to use based on the environment variable
if getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
