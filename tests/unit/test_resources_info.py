"""Tests for the info resource module."""
import unittest
from unittest.mock import MagicMock

from unraid_api.exceptions import APIError, OperationError
from unraid_api.resources.info import InfoResource


class TestInfoResource(unittest.TestCase):
    """Test the InfoResource class."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = MagicMock()
        self.info_resource = InfoResource(self.client)

    def test_init(self):
        """Test initialization of InfoResource."""
        self.assertEqual(self.info_resource.client, self.client)

    def test_get_system_info(self):
        """Test get_system_info method."""
        # Mock the response with the expected structure
        self.client.execute_query.return_value = {"info": {"os": {"platform": "linux"}, "cpu": {}, "memory": {}, "system": {}}}

        # Call the method
        result = self.info_resource.get_system_info()

        # Verify the result
        self.assertEqual(result, {"os": {"platform": "linux"}, "cpu": {}, "memory": {}, "system": {}})

        # Verify the call to execute_query
        self.client.execute_query.assert_called_once()
        args = self.client.execute_query.call_args[0]
        self.assertIn("query", args[0])
        self.assertIn("info", args[0])

    def test_get_system_info_error(self):
        """Test get_system_info method with error."""
        # Mock the response
        self.client.execute_query.return_value = {"not_systemInfo": {}}

        # Call the method and verify it raises an exception
        with self.assertRaises(APIError):
            self.info_resource.get_system_info()

    def test_get_docker_info(self):
        """Test get_docker_info method."""
        # Mock the response
        self.client.execute_query.return_value = {"dockerInfo": {"enabled": True}}

        # Call the method
        result = self.info_resource.get_docker_info()

        # Verify the result
        self.assertEqual(result, {"enabled": True})

        # Verify the call to execute_query
        self.client.execute_query.assert_called_once()
        args = self.client.execute_query.call_args[0]
        self.assertIn("query", args[0])
        self.assertIn("dockerInfo", args[0])

    def test_get_docker_info_error(self):
        """Test get_docker_info method with error."""
        # Mock the response
        self.client.execute_query.return_value = {"not_dockerInfo": {}}

        # Call the method and verify it raises an exception
        with self.assertRaises(APIError):
            self.info_resource.get_docker_info()

    def test_get_vm_info(self):
        """Test get_vm_info method."""
        # Mock the response
        self.client.execute_query.return_value = {"vmInfo": {"enabled": True}}

        # Call the method
        result = self.info_resource.get_vm_info()

        # Verify the result
        self.assertEqual(result, {"enabled": True})

        # Verify the call to execute_query
        self.client.execute_query.assert_called_once()
        args = self.client.execute_query.call_args[0]
        self.assertIn("query", args[0])
        self.assertIn("vmInfo", args[0])

    def test_get_vm_info_error(self):
        """Test get_vm_info method with error."""
        # Mock the response
        self.client.execute_query.return_value = {"not_vmInfo": {}}

        # Call the method and verify it raises an exception
        with self.assertRaises(APIError):
            self.info_resource.get_vm_info()

    def test_reboot(self):
        """Test reboot method."""
        # Mock the response
        self.client.execute_query.return_value = {"reboot": {"success": True, "message": "Rebooting"}}

        # Call the method
        result = self.info_resource.reboot()

        # Verify the result
        self.assertEqual(result, {"success": True, "message": "Rebooting"})

        # Verify the call to execute_query
        self.client.execute_query.assert_called_once()
        args = self.client.execute_query.call_args[0]
        self.assertIn("mutation", args[0])
        self.assertIn("reboot", args[0])

    def test_reboot_error(self):
        """Test reboot method with error."""
        # Mock the response
        self.client.execute_query.return_value = {"reboot": {"success": False, "message": "Error"}}

        # Call the method and verify it raises an exception
        with self.assertRaises(OperationError):
            self.info_resource.reboot()

    def test_get_spindown_delay(self):
        """Test get_spindown_delay method."""
        # Mock the response with the expected structure
        self.client.execute_query.return_value = {"vars": {"spindownDelay": "15"}}

        # Call the method
        result = self.info_resource.get_spindown_delay()

        # Verify the result
        self.assertEqual(result, "15")

        # Verify the call to execute_query
        self.client.execute_query.assert_called_once()
        args = self.client.execute_query.call_args[0]
        self.assertIn("query", args[0])
        self.assertIn("spindownDelay", args[0])

    def test_get_spindown_delay_error(self):
        """Test get_spindown_delay method with error."""
        # Mock the response
        self.client.execute_query.return_value = {"not_spindownDelay": {}}

        # Call the method and verify it raises an exception
        with self.assertRaises(APIError):
            self.info_resource.get_spindown_delay()


if __name__ == "__main__":
    unittest.main()
