"""Tests for the vm resource module."""
import unittest
from unittest.mock import MagicMock

from unraid_api.exceptions import APIError, OperationError
from unraid_api.resources.vm import VMResource


class TestVMResource(unittest.TestCase):
    """Test the VMResource class."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = MagicMock()
        self.vm_resource = VMResource(self.client)

    def test_init(self):
        """Test initialization of VMResource."""
        self.assertEqual(self.vm_resource.client, self.client)

    def test_get_vms(self):
        """Test get_vms method."""
        # Mock the response
        self.client.execute_query.return_value = {"vms": [{"name": "vm1"}]}

        # Call the method
        result = self.vm_resource.get_vms()

        # Verify the result
        self.assertEqual(result, [{"name": "vm1"}])

        # Verify the call to execute_query
        self.client.execute_query.assert_called_once()
        args = self.client.execute_query.call_args[0]
        self.assertIn("query", args[0])
        self.assertIn("vms", args[0])

    def test_get_vms_error(self):
        """Test get_vms method with error."""
        # Mock the response
        self.client.execute_query.return_value = {"not_vms": []}

        # Call the method and verify it raises an exception
        with self.assertRaises(APIError):
            self.vm_resource.get_vms()

    def test_get_vm(self):
        """Test get_vm method."""
        # Mock the response
        self.client.execute_query.return_value = {"vm": {"name": "vm1"}}

        # Call the method
        result = self.vm_resource.get_vm("vm1")

        # Verify the result
        self.assertEqual(result, {"name": "vm1"})

        # Verify the call to execute_query
        self.client.execute_query.assert_called_once()
        args = self.client.execute_query.call_args[0]
        self.assertIn("query", args[0])
        self.assertIn("vm", args[0])

    def test_get_vm_error(self):
        """Test get_vm method with error."""
        # Mock the response
        self.client.execute_query.return_value = {"not_vm": {}}

        # Call the method and verify it raises an exception
        with self.assertRaises(APIError):
            self.vm_resource.get_vm("vm1")

    def test_start_vm(self):
        """Test start_vm method."""
        # Mock the response
        self.client.execute_query.return_value = {
            "startVM": {"success": True, "message": "VM started"}
        }

        # Call the method
        result = self.vm_resource.start_vm("vm1")

        # Verify the result
        self.assertEqual(result, {"success": True, "message": "VM started"})

        # Verify the call to execute_query
        self.client.execute_query.assert_called_once()
        args = self.client.execute_query.call_args[0]
        self.assertIn("mutation", args[0])
        self.assertIn("startVM", args[0])

    def test_start_vm_error(self):
        """Test start_vm method with error."""
        # Mock the response
        self.client.execute_query.return_value = {
            "startVM": {"success": False, "message": "Error starting VM"}
        }

        # Call the method and verify it raises an exception
        with self.assertRaises(OperationError):
            self.vm_resource.start_vm("vm1")

    def test_stop_vm(self):
        """Test stop_vm method."""
        # Mock the response
        self.client.execute_query.return_value = {
            "stopVM": {"success": True, "message": "VM stopped"}
        }

        # Call the method
        result = self.vm_resource.stop_vm("vm1")

        # Verify the result
        self.assertEqual(result, {"success": True, "message": "VM stopped"})

        # Verify the call to execute_query
        self.client.execute_query.assert_called_once()
        args = self.client.execute_query.call_args[0]
        self.assertIn("mutation", args[0])
        self.assertIn("stopVM", args[0])

    def test_stop_vm_error(self):
        """Test stop_vm method with error."""
        # Mock the response
        self.client.execute_query.return_value = {
            "stopVM": {"success": False, "message": "Error stopping VM"}
        }

        # Call the method and verify it raises an exception
        with self.assertRaises(OperationError):
            self.vm_resource.stop_vm("vm1")

    def test_pause_vm(self):
        """Test pause_vm method."""
        # Mock the response
        self.client.execute_query.return_value = {
            "pauseVM": {"success": True, "message": "VM paused"}
        }

        # Call the method
        result = self.vm_resource.pause_vm("vm1")

        # Verify the result
        self.assertEqual(result, {"success": True, "message": "VM paused"})

        # Verify the call to execute_query
        self.client.execute_query.assert_called_once()
        args = self.client.execute_query.call_args[0]
        self.assertIn("mutation", args[0])
        self.assertIn("pauseVM", args[0])

    def test_pause_vm_error(self):
        """Test pause_vm method with error."""
        # Mock the response
        self.client.execute_query.return_value = {
            "pauseVM": {"success": False, "message": "Error pausing VM"}
        }

        # Call the method and verify it raises an exception
        with self.assertRaises(OperationError):
            self.vm_resource.pause_vm("vm1")

    def test_resume_vm(self):
        """Test resume_vm method."""
        # Mock the response
        self.client.execute_query.return_value = {
            "resumeVM": {"success": True, "message": "VM resumed"}
        }

        # Call the method
        result = self.vm_resource.resume_vm("vm1")

        # Verify the result
        self.assertEqual(result, {"success": True, "message": "VM resumed"})

        # Verify the call to execute_query
        self.client.execute_query.assert_called_once()
        args = self.client.execute_query.call_args[0]
        self.assertIn("mutation", args[0])
        self.assertIn("resumeVM", args[0])

    def test_resume_vm_error(self):
        """Test resume_vm method with error."""
        # Mock the response
        self.client.execute_query.return_value = {
            "resumeVM": {"success": False, "message": "Error resuming VM"}
        }

        # Call the method and verify it raises an exception
        with self.assertRaises(OperationError):
            self.vm_resource.resume_vm("vm1")




if __name__ == "__main__":
    unittest.main()
