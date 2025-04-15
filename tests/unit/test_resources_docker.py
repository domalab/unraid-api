"""Tests for the docker resource module."""
import unittest
from unittest.mock import MagicMock

from unraid_api.exceptions import APIError, OperationError
from unraid_api.resources.docker import DockerResource


class TestDockerResource(unittest.TestCase):
    """Test the DockerResource class."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = MagicMock()
        self.docker_resource = DockerResource(self.client)

    def test_init(self):
        """Test initialization of DockerResource."""
        self.assertEqual(self.docker_resource.client, self.client)

    def test_get_containers(self):
        """Test get_containers method."""
        # Mock the response with the expected structure
        self.client.execute_query.return_value = {"docker": {"containers": [{"name": "container1"}]}}

        # Call the method
        result = self.docker_resource.get_containers()

        # Verify the result
        self.assertEqual(result, [{"name": "container1"}])

        # Verify the call to execute_query
        self.client.execute_query.assert_called_once()
        args = self.client.execute_query.call_args[0]
        self.assertIn("query", args[0])
        self.assertIn("containers", args[0])

    def test_get_containers_error(self):
        """Test get_containers method with error."""
        # Mock the response
        self.client.execute_query.return_value = {"not_containers": []}

        # Call the method and verify it raises an exception
        with self.assertRaises(APIError):
            self.docker_resource.get_containers()

    def test_get_container(self):
        """Test get_container method."""
        # Mock the response with the expected structure
        self.client.execute_query.return_value = {"dockerContainer": {"name": "container1"}}

        # Call the method
        result = self.docker_resource.get_container("container1")

        # Verify the result
        self.assertEqual(result, {"name": "container1"})

        # Verify the call to execute_query
        self.client.execute_query.assert_called_once()
        args = self.client.execute_query.call_args[0]
        self.assertIn("query", args[0])
        self.assertIn("dockerContainer", args[0])

    def test_get_container_error(self):
        """Test get_container method with error."""
        # Mock the response
        self.client.execute_query.return_value = {"not_container": {}}

        # Call the method and verify it raises an exception
        with self.assertRaises(APIError):
            self.docker_resource.get_container("container1")

    def test_start_container(self):
        """Test start_container method."""
        # Mock the response
        self.client.execute_query.return_value = {
            "startContainer": {"success": True, "message": "Container started"}
        }

        # Call the method
        result = self.docker_resource.start_container("container1")

        # Verify the result
        self.assertEqual(result, {"success": True, "message": "Container started"})

        # Verify the call to execute_query
        self.client.execute_query.assert_called_once()
        args = self.client.execute_query.call_args[0]
        self.assertIn("mutation", args[0])
        self.assertIn("startContainer", args[0])

    def test_start_container_error(self):
        """Test start_container method with error."""
        # Mock the response
        self.client.execute_query.return_value = {
            "startContainer": {"success": False, "message": "Error starting container"}
        }

        # Call the method and verify it raises an exception
        with self.assertRaises(OperationError):
            self.docker_resource.start_container("container1")

    def test_stop_container(self):
        """Test stop_container method."""
        # Mock the response
        self.client.execute_query.return_value = {
            "stopContainer": {"success": True, "message": "Container stopped"}
        }

        # Call the method
        result = self.docker_resource.stop_container("container1")

        # Verify the result
        self.assertEqual(result, {"success": True, "message": "Container stopped"})

        # Verify the call to execute_query
        self.client.execute_query.assert_called_once()
        args = self.client.execute_query.call_args[0]
        self.assertIn("mutation", args[0])
        self.assertIn("stopContainer", args[0])

    def test_stop_container_error(self):
        """Test stop_container method with error."""
        # Mock the response
        self.client.execute_query.return_value = {
            "stopContainer": {"success": False, "message": "Error stopping container"}
        }

        # Call the method and verify it raises an exception
        with self.assertRaises(OperationError):
            self.docker_resource.stop_container("container1")

    def test_restart_container(self):
        """Test restart_container method."""
        # Mock the response
        self.client.execute_query.return_value = {
            "restartContainer": {"success": True, "message": "Container restarted"}
        }

        # Call the method
        result = self.docker_resource.restart_container("container1")

        # Verify the result
        self.assertEqual(result, {"success": True, "message": "Container restarted"})

        # Verify the call to execute_query
        self.client.execute_query.assert_called_once()
        args = self.client.execute_query.call_args[0]
        self.assertIn("mutation", args[0])
        self.assertIn("restartContainer", args[0])

    def test_restart_container_error(self):
        """Test restart_container method with error."""
        # Mock the response
        self.client.execute_query.return_value = {
            "restartContainer": {"success": False, "message": "Error restarting container"}
        }

        # Call the method and verify it raises an exception
        with self.assertRaises(OperationError):
            self.docker_resource.restart_container("container1")

    def test_get_container_logs(self):
        """Test get_container_logs method."""
        # Mock the response
        self.client.execute_query.return_value = {"containerLogs": "test logs"}

        # Call the method
        result = self.docker_resource.get_container_logs("container1")

        # Verify the result
        self.assertEqual(result, "test logs")

        # Verify the call to execute_query
        self.client.execute_query.assert_called_once()
        args = self.client.execute_query.call_args[0]
        self.assertIn("query", args[0])
        self.assertIn("containerLogs", args[0])

    def test_get_container_logs_with_tail(self):
        """Test get_container_logs method with custom tail."""
        # Mock the response
        self.client.execute_query.return_value = {"containerLogs": "test logs"}

        # Call the method
        result = self.docker_resource.get_container_logs("container1", tail=50)

        # Verify the result
        self.assertEqual(result, "test logs")

        # Verify the call to execute_query
        self.client.execute_query.assert_called_once()
        args = self.client.execute_query.call_args[0]
        self.assertIn("query", args[0])
        self.assertIn("containerLogs", args[0])

    def test_get_container_logs_error(self):
        """Test get_container_logs method with error."""
        # Mock the response
        self.client.execute_query.return_value = {"not_containerLogs": ""}

        # Call the method and verify it raises an exception
        with self.assertRaises(APIError):
            self.docker_resource.get_container_logs("container1")


if __name__ == "__main__":
    unittest.main()
