#!/usr/bin/python3
"""Defines unittests for models/base_model.py.

Unittest classes:
    TestBaseModel_instantiation
    TestBaseModel_save
    TestBaseModel_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModelInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the BaseModel class."""

    def test_no_args_instantiates(self):
        self.assertIsInstance(BaseModel(), BaseModel)

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_types_of_attributes(self):
        base_model = BaseModel()
        self.assertIsInstance(base_model.id, str)
        self.assertIsInstance(base_model.created_at, datetime)
        self.assertIsInstance(base_model.updated_at, datetime)

    def test_two_models_unique_ids(self):
        model1, model2 = BaseModel(), BaseModel()
        self.assertNotEqual(model1.id, model2.id)

    def test_two_models_different_created_at(self):
        model1, model2 = BaseModel(), BaseModel()
        self.assertLess(model1.created_at, model2.created_at)

    def test_two_models_different_updated_at(self):
        model1, model2 = BaseModel(), BaseModel()
        self.assertLess(model1.updated_at, model2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        base_model = BaseModel()
        base_model.id = "123456"
        base_model.created_at = base_model.updated_at = dt
        base_model_str = base_model.__str__()
        self.assertIn("[BaseModel] (123456)", base_model_str)
        self.assertIn("'id': '123456'", base_model_str)
        self.assertIn("'created_at': " + dt_repr, base_model_str)
        self.assertIn("'updated_at': " + dt_repr, base_model_str)

    def test_args_unused(self):
        base_model = BaseModel(None)
        self.assertNotIn(None, base_model.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        base_model = BaseModel(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(base_model.id, "345")
        self.assertEqual(base_model.created_at, dt)
        self.assertEqual(base_model.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        base_model = BaseModel("12", id="345",
                               created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(base_model.id, "345")
        self.assertEqual(base_model.created_at, dt)
        self.assertEqual(base_model.updated_at, dt)


class TestBaseModelSave(unittest.TestCase):
    """Unittests for testing save method of the BaseModel class."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        base_model = BaseModel()
        sleep(0.05)
        first_updated_at = base_model.updated_at
        base_model.save()
        self.assertLess(first_updated_at, base_model.updated_at)

    def test_two_saves(self):
        base_model = BaseModel()
        sleep(0.05)
        first_updated_at = base_model.updated_at
        base_model.save()
        second_updated_at = base_model.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        base_model.save()
        self.assertLess(second_updated_at, base_model.updated_at)

    def test_save_with_arg(self):
        base_model = BaseModel()
        with self.assertRaises(TypeError):
            base_model.save(None)

    def test_save_updates_file(self):
        base_model = BaseModel()
        base_model.save()
        base_model_id = "BaseModel." + base_model.id
        with open("file.json", "r") as f:
            self.assertIn(base_model_id, f.read())


class TestBaseModelToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the BaseModel class."""

    def test_to_dict_type(self):
        base_model = BaseModel()
        self.assertIsInstance(base_model.to_dict(), dict)

    def test_to_dict_contains_correct_keys(self):
        base_model = BaseModel()
        self.assertIn("id", base_model.to_dict())
        self.assertIn("created_at", base_model.to_dict())
        self.assertIn("updated_at", base_model.to_dict())
        self.assertIn("__class__", base_model.to_dict())

    def test_to_dict_contains_added_attributes(self):
        base_model = BaseModel()
        base_model.name = "Holberton"
        base_model.my_number = 98
        self.assertIn("name", base_model.to_dict())
        self.assertIn("my_number", base_model.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        base_model = BaseModel()
        base_model_dict = base_model.to_dict()
        self.assertEqual(str, type(base_model_dict["created_at"]))
        self.assertEqual(str, type(base_model_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        base_model = BaseModel()
        base_model.id = "123456"
        base_model.created_at = base_model.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        self.assertDictEqual(base_model.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        base_model = BaseModel()
        self.assertNotEqual(base_model.to_dict(), base_model.__dict__)

    def test_to_dict_with_arg(self):
        base_model = BaseModel()
        with self.assertRaises(TypeError):
            base_model.to_dict(None)


if __name__ == "__main__":
    unittest.main()
