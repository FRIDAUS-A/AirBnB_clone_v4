#!/usr/bin/env python3
from os import environ

storage_t = environ['HBNB_TYPE_STORAGE']
if 'HBNB_TYPE_STORAGE' in environ and storage_t == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
