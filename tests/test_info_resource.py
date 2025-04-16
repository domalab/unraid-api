"""Tests for the info resource."""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from unraid_api.exceptions import APIError, OperationError
from unraid_api.resources.info import AsyncInfoResource, InfoResource


class TestInfoResource:
    """Tests for the InfoResource class."""

    def setup_method(self):
        """Set up the test."""
        self.client = MagicMock()
        self.resource = InfoResource(self.client)

    def test_init(self):
        """Test initialization."""
        assert self.resource.client == self.client

    def test_get_system_info(self):
        """Test get_system_info method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "info": {
                "os": {
                    "platform": "linux",
                    "distro": "unraid",
                    "release": "6.12.0",
                    "kernel": "5.15.0",
                    "uptime": 86400
                },
                "cpu": {
                    "manufacturer": "Intel",
                    "brand": "Intel(R) Core(TM) i7-10700K",
                    "cores": 8,
                    "threads": 16
                },
                "memory": {
                    "total": 34359738368,
                    "free": 17179869184,
                    "used": 17179869184
                },
                "system": {
                    "manufacturer": "Custom",
                    "model": "Custom Build"
                }
            }
        }

        # Call the method
        result = self.resource.get_system_info()

        # Verify the result
        assert result == self.client.execute_query.return_value["info"]
        self.client.execute_query.assert_called_once()

    def test_get_system_info_error(self):
        """Test get_system_info method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing info field"):
            self.resource.get_system_info()

        self.client.execute_query.assert_called_once()

    def test_reboot(self):
        """Test reboot method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "reboot": {
                "success": True,
                "message": "Rebooting..."
            }
        }

        # Call the method
        result = self.resource.reboot()

        # Verify the result
        assert result == self.client.execute_query.return_value["reboot"]
        self.client.execute_query.assert_called_once()

    def test_reboot_error(self):
        """Test reboot method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "reboot": {
                "success": False,
                "message": "Permission denied"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to reboot: Permission denied"):
            self.resource.reboot()

        self.client.execute_query.assert_called_once()

    def test_shutdown(self):
        """Test shutdown method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "shutdown": {
                "success": True,
                "message": "Shutting down..."
            }
        }

        # Call the method
        result = self.resource.shutdown()

        # Verify the result
        assert result == self.client.execute_query.return_value["shutdown"]
        self.client.execute_query.assert_called_once()

    def test_shutdown_error(self):
        """Test shutdown method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "shutdown": {
                "success": False,
                "message": "Permission denied"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to shutdown: Permission denied"):
            self.resource.shutdown()

        self.client.execute_query.assert_called_once()

    def test_get_spindown_delay(self):
        """Test get_spindown_delay method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "vars": {
                "spindownDelay": "15"
            }
        }

        # Call the method
        result = self.resource.get_spindown_delay()

        # Verify the result
        assert result == "15"
        self.client.execute_query.assert_called_once()

    def test_get_spindown_delay_error(self):
        """Test get_spindown_delay method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing vars.spindownDelay field"):
            self.resource.get_spindown_delay()

        self.client.execute_query.assert_called_once()

    def test_get_docker_info(self):
        """Test get_docker_info method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "dockerInfo": {
                "enabled": True,
                "version": "20.10.12",
                "status": "running",
                "rootPath": "/var/lib/docker",
                "configPath": "/etc/docker",
                "imagePath": "/mnt/user/docker",
                "autostart": True,
                "networkDefault": "bridge",
                "customNetworks": ["custom_network"],
                "privileged": False,
                "logRotation": True
            }
        }

        # Call the method
        result = self.resource.get_docker_info()

        # Verify the result
        assert result == self.client.execute_query.return_value["dockerInfo"]
        self.client.execute_query.assert_called_once()

    def test_get_docker_info_error(self):
        """Test get_docker_info method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing dockerInfo field"):
            self.resource.get_docker_info()

        self.client.execute_query.assert_called_once()

    def test_get_vm_info(self):
        """Test get_vm_info method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "vmInfo": {
                "enabled": True,
                "version": "8.0.0",
                "status": "running",
                "corePath": "/usr/local/libvirt",
                "configPath": "/etc/libvirt",
                "imagePath": "/mnt/user/vms",
                "autostart": True,
                "winVmCount": 1,
                "linuxVmCount": 2,
                "otherVmCount": 0,
                "CPUisolatedCores": "0,1",
                "PCIeiommuGroups": ["1", "2", "3"]
            }
        }

        # Call the method
        result = self.resource.get_vm_info()

        # Verify the result
        assert result == self.client.execute_query.return_value["vmInfo"]
        self.client.execute_query.assert_called_once()

    def test_get_vm_info_error(self):
        """Test get_vm_info method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing vmInfo field"):
            self.resource.get_vm_info()

        self.client.execute_query.assert_called_once()


@pytest.mark.asyncio
class TestAsyncInfoResource:
    """Tests for the AsyncInfoResource class."""

    def setup_method(self):
        """Set up the test."""
        self.client = MagicMock()
        # Make execute_query a coroutine
        self.client.execute_query = AsyncMock()
        self.resource = AsyncInfoResource(self.client)

    async def test_init(self):
        """Test initialization."""
        assert self.resource.client == self.client

    async def test_get_system_info(self):
        """Test get_system_info method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "info": {
                "os": {
                    "platform": "linux",
                    "distro": "unraid",
                    "release": "6.12.0",
                    "kernel": "5.15.0",
                    "uptime": 86400
                },
                "cpu": {
                    "manufacturer": "Intel",
                    "brand": "Intel(R) Core(TM) i7-10700K",
                    "cores": 8,
                    "threads": 16
                },
                "memory": {
                    "total": 34359738368,
                    "free": 17179869184,
                    "used": 17179869184
                },
                "system": {
                    "manufacturer": "Custom",
                    "model": "Custom Build"
                }
            }
        }

        # Call the method
        result = await self.resource.get_system_info()

        # Verify the result
        assert result == self.client.execute_query.return_value["info"]
        self.client.execute_query.assert_called_once()

    async def test_get_system_info_error(self):
        """Test get_system_info method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing info field"):
            await self.resource.get_system_info()

        self.client.execute_query.assert_called_once()

    async def test_reboot(self):
        """Test reboot method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "reboot": {
                "success": True,
                "message": "Rebooting..."
            }
        }

        # Call the method
        result = await self.resource.reboot()

        # Verify the result
        assert result == self.client.execute_query.return_value["reboot"]
        self.client.execute_query.assert_called_once()

    async def test_reboot_error(self):
        """Test reboot method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "reboot": {
                "success": False,
                "message": "Permission denied"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to reboot: Permission denied"):
            await self.resource.reboot()

        self.client.execute_query.assert_called_once()

    async def test_shutdown(self):
        """Test shutdown method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "shutdown": {
                "success": True,
                "message": "Shutting down..."
            }
        }

        # Call the method
        result = await self.resource.shutdown()

        # Verify the result
        assert result == self.client.execute_query.return_value["shutdown"]
        self.client.execute_query.assert_called_once()

    async def test_shutdown_error(self):
        """Test shutdown method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "shutdown": {
                "success": False,
                "message": "Permission denied"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to shutdown: Permission denied"):
            await self.resource.shutdown()

        self.client.execute_query.assert_called_once()

    async def test_get_spindown_delay(self):
        """Test get_spindown_delay method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "vars": {
                "spindownDelay": "15"
            }
        }

        # Call the method
        result = await self.resource.get_spindown_delay()

        # Verify the result
        assert result == "15"
        self.client.execute_query.assert_called_once()

    async def test_get_spindown_delay_error(self):
        """Test get_spindown_delay method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing vars.spindownDelay field"):
            await self.resource.get_spindown_delay()

        self.client.execute_query.assert_called_once()

    async def test_get_docker_info(self):
        """Test get_docker_info method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "dockerInfo": {
                "enabled": True,
                "version": "20.10.12",
                "status": "running",
                "rootPath": "/var/lib/docker",
                "configPath": "/etc/docker",
                "imagePath": "/mnt/user/docker",
                "autostart": True,
                "networkDefault": "bridge",
                "customNetworks": ["custom_network"],
                "privileged": False,
                "logRotation": True
            }
        }

        # Call the method
        result = await self.resource.get_docker_info()

        # Verify the result
        assert result == self.client.execute_query.return_value["dockerInfo"]
        self.client.execute_query.assert_called_once()

    async def test_get_docker_info_error(self):
        """Test get_docker_info method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing dockerInfo field"):
            await self.resource.get_docker_info()

        self.client.execute_query.assert_called_once()

    async def test_get_vm_info(self):
        """Test get_vm_info method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "vmInfo": {
                "enabled": True,
                "version": "8.0.0",
                "status": "running",
                "corePath": "/usr/local/libvirt",
                "configPath": "/etc/libvirt",
                "imagePath": "/mnt/user/vms",
                "autostart": True,
                "winVmCount": 1,
                "linuxVmCount": 2,
                "otherVmCount": 0,
                "CPUisolatedCores": "0,1",
                "PCIeiommuGroups": ["1", "2", "3"]
            }
        }

        # Call the method
        result = await self.resource.get_vm_info()

        # Verify the result
        assert result == self.client.execute_query.return_value["vmInfo"]
        self.client.execute_query.assert_called_once()

    async def test_get_vm_info_error(self):
        """Test get_vm_info method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing vmInfo field"):
            await self.resource.get_vm_info()

        self.client.execute_query.assert_called_once()
        self.client.execute_query.assert_called_once()
