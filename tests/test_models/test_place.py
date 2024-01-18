#!/usr/bin/python3
"""Defines unittests for models/place.py.

Unittest classes:
    TestPlace_instantiation
    TestPlace_save
    TestPlace_to_dict
"""

import os
import models
import unittest
from datetime import datetime, timedelta
from time import sleep
from models.place import Place


class TestPlaceInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Place class."""

    def test_no_args_instantiates(self):
        self.assertIsInstance(Place(), Place)

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_types_of_attributes(self):
        place = Place()
        self.assertIsInstance(place.id, str)
        self.assertIsInstance(place.created_at, datetime)
        self.assertIsInstance(place.updated_at, datetime)
        self.assertIsInstance(Place.city_id, str)
        self.assertIn("city_id", dir(place))
        self.assertNotIn("city_id", place.__dict__)
        self.assertIsInstance(Place.user_id, str)
        self.assertIn("user_id", dir(place))
        self.assertNotIn("user_id", place.__dict__)
        self.assertIsInstance(Place.name, str)
        self.assertIn("name", dir(place))
        self.assertNotIn("name", place.__dict__)
        self.assertIsInstance(Place.description, str)
        self.assertIn("description", dir(place))
        self.assertNotIn("description", place.__dict__)
        self.assertIsInstance(Place.number_rooms, int)
        self.assertIn("number_rooms", dir(place))
        self.assertNotIn("number_rooms", place.__dict__)
        self.assertIsInstance(Place.number_bathrooms, int)
        self.assertIn("number_bathrooms", dir(place))
        self.assertNotIn("number_bathrooms", place.__dict__)
        self.assertIsInstance(Place.max_guest, int)
        self.assertIn("max_guest", dir(place))
        self.assertNotIn("max_guest", place.__dict__)
        self.assertIsInstance(Place.price_by_night, int)
        self.assertIn("price_by_night", dir(place))
        self.assertNotIn("price_by_night", place.__dict__)
        self.assertIsInstance(Place.latitude, float)
        self.assertIn("latitude", dir(place))
        self.assertNotIn("latitude", place.__dict__)
        self.assertIsInstance(Place.longitude, float)
        self.assertIn("longitude", dir(place))
        self.assertNotIn("longitude", place.__dict__)
        self.assertIsInstance(Place.amenity_ids, list)
        self.assertIn("amenity_ids", dir(place))
        self.assertNotIn("amenity_ids", place.__dict__)

    def test_two_places_unique_ids(self):
        place1, place2 = Place(), Place()
        self.assertNotEqual(place1.id, place2.id)

    def test_two_places_different_created_at(self):
        place1, place2 = Place(), Place()
        self.assertLess(place1.created_at, place2.created_at)

    def test_two_places_different_updated_at(self):
        place1, place2 = Place(), Place()
        self.assertLess(place1.updated_at, place2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        place = Place()
        place.id = "123456"
        place.created_at = place.updated_at = dt
        place_str = place.__str__()
        self.assertIn("[Place] (123456)", place_str)
        self.assertIn("'id': '123456'", place_str)
        self.assertIn("'created_at': " + dt_repr, place_str)
        self.assertIn("'updated_at': " + dt_repr, place_str)

    def test_args_unused(self):
        place = Place(None)
        self.assertNotIn(None, place.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        place = Place(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(place.id, "345")
        self.assertEqual(place.created_at, dt)
        self.assertEqual(place.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlaceSave(unittest.TestCase):
    """Unittests for testing save method of the Place class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        place = Place()
        sleep(0.05)
        first_updated_at = place.updated_at
        place.save()
        self.assertLess(first_updated_at, place.updated_at)

    def test_two_saves(self):
        place = Place()
        sleep(0.05)
        first_updated_at = place.updated_at
        place.save()
        second_updated_at = place.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        place.save()
        self.assertLess(second_updated_at, place.updated_at)

    def test_save_with_arg(self):
        place = Place()
        with self.assertRaises(TypeError):
            place.save(None)

    def test_save_updates_file(self):
        place = Place()
        place.save()
        place_id = "Place." + place.id
        with open("file.json", "r") as f:
            self.assertIn(place_id, f.read())


class TestPlaceToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the Place class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Place().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        place = Place()
        self.assertIn("id", place.to_dict())
        self.assertIn("created_at", place.to_dict())
        self.assertIn("updated_at", place.to_dict())
        self.assertIn("__class__", place.to_dict())

    def test_to_dict_contains_added_attributes(self):
        place = Place()
        place.middle_name = "Holberton"
        place.my_number = 98
        self.assertEqual("Holberton", place.middle_name)
        self.assertIn("my_number", place.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        place = Place()
        place_dict = place.to_dict()
        self.assertEqual(str, type(place_dict["id"]))
        self.assertEqual(str, type(place_dict["created_at"]))
        self.assertEqual(str, type(place_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        place = Place()
        place.id = "123456"
        place.created_at = place.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(place.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        place = Place()
        self.assertNotEqual(place.to_dict(), place.__dict__)

    def test_to_dict_with_arg(self):
        place = Place()
        with self.assertRaises(TypeError):
            place.to_dict(None)


if __name__ == "__main__":
    unittest.main()
