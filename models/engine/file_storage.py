#!/usr/bin/env python3
"""To store all objects"""

import json


class FileStorage():
    """serializes instances to a JSON file and
    deserializes JSON file to instances
        Args:
            file_path (string): defines the path to the json
            storage file
            objects (dict): contains the dictionary list
            of all the objects
        """
    __file_path = "./file.json"
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        total = FileStorage.__objects
        if cls:
            new_dict = {}
            for key, value in total.items():
                if self.classes()[value.to_dict()["__class__"]] == cls:
                    new_dict[key] = value
            return new_dict
        else:
            return (FileStorage.__objects)

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj
        return

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        new_dict = {}
        for key, value in FileStorage.__objects.items():
            new_dict[key] = value.to_dict()
        try:
            with open(FileStorage.__file_path, "w") as file:
                file.write(json.dumps(new_dict))
        except FileNotFoundError:
            return

    def classes(self):
        """Returns a dictionary of  valid classes and their references"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "Place": Place,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Review": Review}
        return classes

    def reload(self):
        """
        deserializes the JSON file to __objects (only if the JSON
        file (__file_path) exists ;
        otherwise, do nothing. If the file doesn’t exist,
        no exception should be raised)
        """
        try:
            with open(FileStorage.__file_path, "r") as file:
                content = file.read()
                content = json.loads(content)
                for key, value in content.items():
                    FileStorage.__objects[key] = self.classes()\
                    [value["__class__"]](**value)
        except FileNotFoundError:
            return

    def delete(self, obj=None):
        """delete obj from __objects if its
        inside and do nothing if obj is None"""
        if obj:
            content = self.all()
            for key, value in content.items():
                if value.to_dict()['id'] == obj.id:
                    content.pop(key)
                    break
            for key, value in content.items():
                self.new(value)
            return

    def close(self):
        """call reload() method for deserializing the
        JSON file to objects"""
        self.reload()
