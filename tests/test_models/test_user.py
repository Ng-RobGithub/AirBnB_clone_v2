#!/usr/bin/python3
"""Defines unittests for models/user.py.

Unittest classes:
    TestUser_instantiation
    TestUser_save
    TestUser_to_dict
"""

import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class TestConsole(unittest.TestCase):

    def setUp(self):
        """Set up for test."""
        self.console_output = StringIO()
        self.held_output = StringIO()
        self.held_output_value = ""

    def tearDown(self):
        """Tear down for test."""
        pass

    def create_console(self, server=None):
        """Create a new HBNBCommand."""
        return HBNBCommand(stdin=server, stdout=self.console_output)

    def capture_stdout(self):
        """Capture the output of stdout."""
        self.held_output_value = self.held_output.getvalue()
        self.held_output.truncate(0)
        self.held_output.seek(0)
        return self.held_output_value

    def run_test(self, server=None, cmd=None):
        """Run a test."""
        self.held_output = StringIO()
        console = self.create_console(server=server)
        if cmd:
            console.onecmd(cmd)
        return self.capture_stdout()

    def test_create(self):
        """Test create command."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.run_test(server="create BaseModel", cmd="create BaseModel")
            output = mock_stdout.getvalue().strip()
            self.assertRegex(output, r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")

    def test_show(self):
        """Test show command."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            obj = BaseModel()
            obj_id = obj.id
            self.run_test(server="show BaseModel {}".format(obj_id), cmd="show BaseModel {}".format(obj_id))
            output = mock_stdout.getvalue().strip()
            self.assertIn(obj_id, output)

    def test_destroy(self):
        """Test destroy command."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            obj = BaseModel()
            obj_id = obj.id
            self.run_test(server="destroy BaseModel {}".format(obj_id), cmd="destroy BaseModel {}".format(obj_id))
            self.assertFalse(hasattr(storage.all(), "BaseModel.{}".format(obj_id)))

    def test_all(self):
        """Test all command."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.run_test(server="all", cmd="all")
            output = mock_stdout.getvalue().strip()
            self.assertIn("BaseModel", output)

    def test_count(self):
        """Test count command."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.run_test(server="create BaseModel", cmd="create BaseModel")
            self.run_test(server="count BaseModel", cmd="count BaseModel")
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "1")

    def test_update(self):
        """Test update command."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            obj = BaseModel()
            obj_id = obj.id
            self.run_test(server="update BaseModel {} name John".format(obj_id), cmd="update BaseModel {} name John".format(obj_id))
            updated_obj = storage.all()["BaseModel.{}".format(obj_id)]
            self.assertEqual(updated_obj.name, "John")


if __name__ == '__main__':
    unittest.main()
