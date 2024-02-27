#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.engine import file_storage


class FileStorage:
    """
    Represent an abstracted storage engine.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}


def all(self):
    """Return the dictionary __objects."""
    return FileStorage.__objects


def new(self, obj):
    """Set in __objects obj with key <obj_class_name>.id"""
    key = "{}.{}".format(obj.__class__.__name__, obj.id)
    FileStorage.__objects[key] = obj


def save(self):
    """Serialize __objects to the JSON file __file_path."""
    objdict = {key: obj.to_dict()
               for key, obj in FileStorage.__objects.items()}
    with open(FileStorage.__file_path, "w") as f:
        json.dump(objdict, f)


def get(self, cls, id):
    """
    Retrieve one object.
    """
    key = "{}.{}".format(cls.__name__, id)
    return self.__objects.get(key, None)


def count(self, cls=None):
    """
    Count the number of objects in storage.
    """
    if cls:
        return len([obj for obj in self.__objects.values()
                   if isinstance(obj, cls)])
    else:
        return len(self.__objects)


def reload(self):
    """Deserialize the JSON file __file_path to __objects, if it exists."""
    try:
        with open(FileStorage.__file_path) as f:
            objdict = json.load(f)
            for key, value in objdict.items():
                cls_name = value["__class__"]
                file_storage.py = value["__class__"]
                self.new(eval(cls_name)(**value))

    except FileNotFoundError:
        return
