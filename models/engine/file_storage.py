#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User


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
    """Deserializes the JSON file to __objects"""
    try:
        with open(self.__file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            for key, value in json_data.items():
                key_split = key.split(".")
                class_name = key_split[0]
                models = {"BaseModel": BaseModel, "User": User}
                class_obj = models.classes[class_name]
                obj = class_obj(**value)
                self.__objects[key] = obj

    except FileNotFoundError:
        pass
