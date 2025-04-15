"""Tests for the disk resource module."""
import unittest
from unittest.mock import MagicMock

from unraid_api.exceptions import APIError
from unraid_api.resources.disk import DiskResource


class TestDiskResource(unittest.TestCase):
    """Test the DiskResource class."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = MagicMock()
        self.disk_resource = DiskResource(self.client)

    def test_init(self):
        """Test initialization of DiskResource."""
        self.assertEqual(self.disk_resource.client, self.client)

    def test_get_disks(self):
        """Test get_disks method."""
        # Mock the response
        self.client.execute_query.return_value = {"disks": [{"id": "sda"}]}

        # Call the method
        result = self.disk_resource.get_disks()

        # Verify the result
        self.assertEqual(result, [{"id": "sda"}])

        # Verify the call to execute_query
        self.client.execute_query.assert_called_once()
        args = self.client.execute_query.call_args[0]
        self.assertIn("query", args[0])
        self.assertIn("disks", args[0])

    def test_get_disks_error(self):
        """Test get_disks method with error."""
        # Mock the response
        self.client.execute_query.return_value = {"not_disks": []}

        # Call the method and verify it raises an exception
        with self.assertRaises(APIError):
            self.disk_resource.get_disks()

    def test_get_disk(self):
        """Test get_disk method."""
        # Mock the response
        self.client.execute_query.return_value = {"disk": {"id": "sda"}}

        # Call the method
        result = self.disk_resource.get_disk("sda")

        # Verify the result
        self.assertEqual(result, {"id": "sda"})

        # Verify the call to execute_query
        self.client.execute_query.assert_called_once()
        args = self.client.execute_query.call_args[0]
        self.assertIn("query", args[0])
        self.assertIn("disk", args[0])

    def test_get_disk_error(self):
        """Test get_disk method with error."""
        # Mock the response
        self.client.execute_query.return_value = {"not_disk": {}}

        # Call the method and verify it raises an exception
        with self.assertRaises(APIError):
            self.disk_resource.get_disk("sda")

    def test_get_disk_smart(self):
        """Test get_disk_smart method."""
        # Mock the response with the expected structure
        self.client.execute_query.return_value = {"disk": {"smart": {"attributes": []}}}

        # Call the method
        result = self.disk_resource.get_disk_smart("sda")

        # Verify the result
        self.assertEqual(result, {"attributes": []})

        # Verify the call to execute_query
        self.client.execute_query.assert_called_once()
        args = self.client.execute_query.call_args[0]
        self.assertIn("query", args[0])
        self.assertIn("smart", args[0])

    def test_get_disk_smart_error(self):
        """Test get_disk_smart method with error."""
        # Mock the response
        self.client.execute_query.return_value = {"not_diskSmart": {}}

        # Call the method and verify it raises an exception
        with self.assertRaises(APIError):
            self.disk_resource.get_disk_smart("sda")




if __name__ == "__main__":
    unittest.main()
