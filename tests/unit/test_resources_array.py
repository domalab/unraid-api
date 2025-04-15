"""Tests for the array resource module."""
import unittest
from unittest.mock import MagicMock

from unraid_api.exceptions import APIError, OperationError
from unraid_api.resources.array import ArrayResource


class TestArrayResource(unittest.TestCase):
    """Test the ArrayResource class."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = MagicMock()
        self.array_resource = ArrayResource(self.client)

    def test_init(self):
        """Test initialization of ArrayResource."""
        self.assertEqual(self.array_resource.client, self.client)

    def test_get_array_status(self):
        """Test get_array_status method."""
        # Mock the response
        self.client.execute_query.return_value = {"array": {"test": "value"}}

        # Call the method
        result = self.array_resource.get_array_status()

        # Verify the result
        self.assertEqual(result, {"test": "value"})

        # Verify the call to execute_query
        self.client.execute_query.assert_called_once()
        args, kwargs = self.client.execute_query.call_args
        self.assertIn("query", args[0])
        self.assertIn("array", args[0])

    def test_get_array_status_error(self):
        """Test get_array_status method with error."""
        # Mock the response
        self.client.execute_query.return_value = {"not_array": {}}

        # Call the method and verify it raises an exception
        with self.assertRaises(APIError):
            self.array_resource.get_array_status()

    def test_start_array(self):
        """Test start_array method."""
        # Mock the response
        self.client.execute_query.return_value = {
            "startArray": {"success": True, "message": "Array started"}
        }

        # Call the method
        result = self.array_resource.start_array()

        # Verify the result
        self.assertEqual(result, {"success": True, "message": "Array started"})

        # Verify the call to execute_query
        self.client.execute_query.assert_called_once()
        args, kwargs = self.client.execute_query.call_args
        self.assertIn("mutation", args[0])
        self.assertIn("startArray", args[0])

    def test_start_array_error(self):
        """Test start_array method with error."""
        # Mock the response
        self.client.execute_query.return_value = {
            "startArray": {"success": False, "message": "Error starting array"}
        }

        # Call the method and verify it raises an exception
        with self.assertRaises(OperationError):
            self.array_resource.start_array()

    def test_stop_array(self):
        """Test stop_array method."""
        # Mock the response
        self.client.execute_query.return_value = {
            "stopArray": {"success": True, "message": "Array stopped"}
        }

        # Call the method
        result = self.array_resource.stop_array()

        # Verify the result
        self.assertEqual(result, {"success": True, "message": "Array stopped"})

        # Verify the call to execute_query
        self.client.execute_query.assert_called_once()
        args, kwargs = self.client.execute_query.call_args
        self.assertIn("mutation", args[0])
        self.assertIn("stopArray", args[0])

    def test_stop_array_error(self):
        """Test stop_array method with error."""
        # Mock the response
        self.client.execute_query.return_value = {
            "stopArray": {"success": False, "message": "Error stopping array"}
        }

        # Call the method and verify it raises an exception
        with self.assertRaises(OperationError):
            self.array_resource.stop_array()


if __name__ == "__main__":
    unittest.main()
