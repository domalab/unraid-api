"""Tests for the config resource."""
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from typing import Dict, Any

from unraid_api.resources.config import ConfigResource, AsyncConfigResource
from unraid_api.exceptions import APIError, OperationError


class TestConfigResource:
    """Tests for the ConfigResource class."""

    def setup_method(self):
        """Set up the test."""
        self.client = MagicMock()
        self.resource = ConfigResource(self.client)

    def test_init(self):
        """Test initialization."""
        assert self.resource.client == self.client

    def test_get_system_config(self):
        """Test get_system_config method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "systemConfig": {
                "hostname": "unraid-server",
                "description": "Test server",
                "model": "Custom Build",
                "version": "6.9.2",
                "motherboard": "ASUS ROG STRIX",
                "cpu": {
                    "model": "AMD Ryzen 9 5900X",
                    "cores": 12,
                    "threads": 24
                },
                "memory": {
                    "total": 32768,
                    "used": 8192,
                    "free": 24576
                },
                "network": {
                    "interfaces": [
                        {
                            "name": "eth0",
                            "mac": "00:11:22:33:44:55",
                            "ip": "192.168.1.100",
                            "netmask": "255.255.255.0",
                            "gateway": "192.168.1.1",
                            "up": True,
                            "speed": 1000,
                            "duplex": "full"
                        }
                    ],
                    "dnsServers": ["8.8.8.8", "8.8.4.4"],
                    "hostname": "unraid-server"
                }
            }
        }

        # Call the method
        result = self.resource.get_system_config()

        # Verify the result
        assert result == self.client.execute_query.return_value["systemConfig"]
        self.client.execute_query.assert_called_once()

    def test_get_system_config_error(self):
        """Test get_system_config method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing systemConfig field"):
            self.resource.get_system_config()

        self.client.execute_query.assert_called_once()

    def test_update_system_config(self):
        """Test update_system_config method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "updateSystemConfig": {
                "success": True,
                "message": "System config updated"
            }
        }

        # Call the method
        config = {
            "hostname": "new-unraid-server",
            "description": "Updated test server"
        }
        result = self.resource.update_system_config(config)

        # Verify the result
        assert result == self.client.execute_query.return_value["updateSystemConfig"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation UpdateSystemConfig($input: SystemConfigInput!) {
            updateSystemConfig(input: $input) {
                success
                message
            }
        }
        """,
            {"input": config}
        )

    def test_update_system_config_error(self):
        """Test update_system_config method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "updateSystemConfig": {
                "success": False,
                "message": "Invalid configuration"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to update system config: Invalid configuration"):
            self.resource.update_system_config({"hostname": "invalid-hostname"})

        self.client.execute_query.assert_called_once()

    def test_get_share_config(self):
        """Test get_share_config method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "shareConfig": {
                "name": "test-share",
                "comment": "Test share",
                "allocator": "highwater",
                "fsType": "xfs",
                "include": ["*.txt"],
                "exclude": ["*.tmp"],
                "useCache": True,
                "exportEnabled": True,
                "security": "public",
                "accessMode": "read-write",
                "ownership": "root",
                "diskIds": ["disk1", "disk2"]
            }
        }

        # Call the method
        result = self.resource.get_share_config("test-share")

        # Verify the result
        assert result == self.client.execute_query.return_value["shareConfig"]
        self.client.execute_query.assert_called_once_with(
            """
        query GetShareConfig($name: String!) {
            shareConfig(name: $name) {
                name
                comment
                allocator
                fsType
                include
                exclude
                useCache
                exportEnabled
                security
                accessMode
                ownership
                diskIds
            }
        }
        """,
            {"name": "test-share"}
        )

    def test_get_share_config_error(self):
        """Test get_share_config method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing shareConfig field"):
            self.resource.get_share_config("test-share")

        self.client.execute_query.assert_called_once()

    def test_update_share_config(self):
        """Test update_share_config method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "updateShareConfig": {
                "success": True,
                "message": "Share config updated"
            }
        }

        # Call the method
        config = {
            "comment": "Updated test share",
            "useCache": False
        }
        result = self.resource.update_share_config("test-share", config)

        # Verify the result
        assert result == self.client.execute_query.return_value["updateShareConfig"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation UpdateShareConfig($name: String!, $input: ShareConfigInput!) {
            updateShareConfig(name: $name, input: $input) {
                success
                message
            }
        }
        """,
            {"name": "test-share", "input": config}
        )

    def test_update_share_config_error(self):
        """Test update_share_config method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "updateShareConfig": {
                "success": False,
                "message": "Share not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to update share config: Share not found"):
            self.resource.update_share_config("nonexistent-share", {"comment": "Updated comment"})

        self.client.execute_query.assert_called_once()

    def test_create_share(self):
        """Test create_share method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "createShare": {
                "success": True,
                "message": "Share created"
            }
        }

        # Call the method
        config = {
            "comment": "New test share",
            "allocator": "highwater",
            "fsType": "xfs",
            "useCache": True,
            "exportEnabled": True,
            "security": "public",
            "accessMode": "read-write",
            "ownership": "root",
            "diskIds": ["disk1", "disk2"]
        }
        result = self.resource.create_share("new-share", config)

        # Verify the result
        assert result == self.client.execute_query.return_value["createShare"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation CreateShare($name: String!, $input: ShareConfigInput!) {
            createShare(name: $name, input: $input) {
                success
                message
            }
        }
        """,
            {"name": "new-share", "input": config}
        )

    def test_create_share_error(self):
        """Test create_share method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "createShare": {
                "success": False,
                "message": "Share already exists"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to create share: Share already exists"):
            self.resource.create_share("existing-share", {"comment": "New share"})

        self.client.execute_query.assert_called_once()

    def test_delete_share(self):
        """Test delete_share method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "deleteShare": {
                "success": True,
                "message": "Share deleted"
            }
        }

        # Call the method
        result = self.resource.delete_share("test-share")

        # Verify the result
        assert result == self.client.execute_query.return_value["deleteShare"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation DeleteShare($name: String!) {
            deleteShare(name: $name) {
                success
                message
            }
        }
        """,
            {"name": "test-share"}
        )

    def test_delete_share_error(self):
        """Test delete_share method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "deleteShare": {
                "success": False,
                "message": "Share not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to delete share: Share not found"):
            self.resource.delete_share("nonexistent-share")

        self.client.execute_query.assert_called_once()

    def test_get_plugin_config(self):
        """Test get_plugin_config method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "pluginConfig": {
                "name": "test-plugin",
                "version": "1.0.0",
                "author": "Test Author",
                "description": "Test plugin description",
                "support": "https://example.com/support",
                "icon": "icon.png",
                "settings": {
                    "enabled": True,
                    "port": 8080
                }
            }
        }

        # Call the method
        result = self.resource.get_plugin_config("test-plugin")

        # Verify the result
        assert result == self.client.execute_query.return_value["pluginConfig"]
        self.client.execute_query.assert_called_once_with(
            """
        query GetPluginConfig($name: String!) {
            pluginConfig(name: $name) {
                name
                version
                author
                description
                support
                icon
                settings
            }
        }
        """,
            {"name": "test-plugin"}
        )

    def test_get_plugin_config_error(self):
        """Test get_plugin_config method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing pluginConfig field"):
            self.resource.get_plugin_config("test-plugin")

        self.client.execute_query.assert_called_once()

    def test_update_plugin_config(self):
        """Test update_plugin_config method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "updatePluginConfig": {
                "success": True,
                "message": "Plugin config updated"
            }
        }

        # Call the method
        settings = {
            "enabled": False,
            "port": 9090
        }
        result = self.resource.update_plugin_config("test-plugin", settings)

        # Verify the result
        assert result == self.client.execute_query.return_value["updatePluginConfig"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation UpdatePluginConfig($name: String!, $settings: JSONObject!) {
            updatePluginConfig(name: $name, settings: $settings) {
                success
                message
            }
        }
        """,
            {"name": "test-plugin", "settings": settings}
        )

    def test_update_plugin_config_error(self):
        """Test update_plugin_config method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "updatePluginConfig": {
                "success": False,
                "message": "Plugin not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to update plugin config: Plugin not found"):
            self.resource.update_plugin_config("nonexistent-plugin", {"enabled": True})

        self.client.execute_query.assert_called_once()


@pytest.mark.asyncio
class TestAsyncConfigResource:
    """Tests for the AsyncConfigResource class."""

    def setup_method(self):
        """Set up the test."""
        self.client = MagicMock()
        # Make execute_query a coroutine
        self.client.execute_query = AsyncMock()
        self.resource = AsyncConfigResource(self.client)

    async def test_init(self):
        """Test initialization."""
        assert self.resource.client == self.client

    async def test_get_system_config(self):
        """Test get_system_config method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "systemConfig": {
                "hostname": "unraid-server",
                "description": "Test server",
                "model": "Custom Build",
                "version": "6.9.2",
                "motherboard": "ASUS ROG STRIX",
                "cpu": {
                    "model": "AMD Ryzen 9 5900X",
                    "cores": 12,
                    "threads": 24
                },
                "memory": {
                    "total": 32768,
                    "used": 8192,
                    "free": 24576
                },
                "network": {
                    "interfaces": [
                        {
                            "name": "eth0",
                            "mac": "00:11:22:33:44:55",
                            "ip": "192.168.1.100",
                            "netmask": "255.255.255.0",
                            "gateway": "192.168.1.1",
                            "up": True,
                            "speed": 1000,
                            "duplex": "full"
                        }
                    ],
                    "dnsServers": ["8.8.8.8", "8.8.4.4"],
                    "hostname": "unraid-server"
                }
            }
        }

        # Call the method
        result = await self.resource.get_system_config()

        # Verify the result
        assert result == self.client.execute_query.return_value["systemConfig"]
        self.client.execute_query.assert_called_once()

    async def test_get_system_config_error(self):
        """Test get_system_config method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing systemConfig field"):
            await self.resource.get_system_config()

        self.client.execute_query.assert_called_once()
