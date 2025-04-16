"""Tests for the disk resource."""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from unraid_api.exceptions import APIError, OperationError
from unraid_api.resources.disk import AsyncDiskResource, DiskResource


class TestDiskResource:
    """Tests for the DiskResource class."""

    def setup_method(self):
        """Set up the test."""
        self.client = MagicMock()
        self.resource = DiskResource(self.client)

    def test_init(self):
        """Test initialization."""
        assert self.resource.client == self.client

    def test_get_disks(self):
        """Test get_disks method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "disks": [
                {
                    "id": "disk1",
                    "device": "/dev/sda",
                    "name": "disk1",
                    "size": 1000000,
                    "type": "sata",
                    "temperature": 35,
                    "smartStatus": "PASS"
                }
            ]
        }

        # Call the method
        result = self.resource.get_disks()

        # Verify the result
        assert result == self.client.execute_query.return_value["disks"]
        self.client.execute_query.assert_called_once_with(
            """
        query GetDisks {
            disks {
                id
                device
                name
                size
                type
                temperature
                smartStatus
            }
        }
        """
        )

    def test_get_disks_error(self):
        """Test get_disks method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing disks field"):
            self.resource.get_disks()

        self.client.execute_query.assert_called_once()

    def test_get_disk(self):
        """Test get_disk method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "disk": {
                "id": "disk1",
                "device": "/dev/sda",
                "deviceId": "sda",
                "deviceNode": "/dev/sda",
                "name": "disk1",
                "partitions": [
                    {
                        "number": 1,
                        "name": "sda1",
                        "fsType": "ext4",
                        "mountpoint": "/mnt/disk1",
                        "size": 1000000,
                        "used": 500000,
                        "free": 500000,
                        "color": "green",
                        "temp": 35,
                        "deviceId": "sda1",
                        "isArray": True
                    }
                ],
                "size": 1000000,
                "temp": 35,
                "status": "NORMAL",
                "interface": "SATA",
                "model": "WDC WD10EFRX",
                "protocol": "ATA",
                "rotationRate": 5400,
                "serial": "WD-WCC4E1234567",
                "type": "sata",
                "numReads": 1000,
                "numWrites": 500,
                "numErrors": 0,
                "color": "green",
                "rotational": True,
                "vendor": "Western Digital",
                "spindownStatus": "active",
                "lastSpindownTime": "2023-01-01T00:00:00Z"
            }
        }

        # Call the method
        result = self.resource.get_disk("disk1")

        # Verify the result
        assert result == self.client.execute_query.return_value["disk"]
        self.client.execute_query.assert_called_once()

    def test_get_disk_error(self):
        """Test get_disk method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing disk field"):
            self.resource.get_disk("disk1")

        self.client.execute_query.assert_called_once()

    def test_mount_disk(self):
        """Test mount_disk method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "mountDisk": {
                "success": True,
                "message": "Disk mounted"
            }
        }

        # Call the method
        result = self.resource.mount_disk("disk1")

        # Verify the result
        assert result == self.client.execute_query.return_value["mountDisk"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation MountDisk($id: String!) {
            mountDisk(id: $id) {
                success
                message
            }
        }
        """,
            {"id": "disk1"}
        )

    def test_mount_disk_error(self):
        """Test mount_disk method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "mountDisk": {
                "success": False,
                "message": "Disk already mounted"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to mount disk: Disk already mounted"):
            self.resource.mount_disk("disk1")

        self.client.execute_query.assert_called_once()

    def test_unmount_disk(self):
        """Test unmount_disk method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "unmountDisk": {
                "success": True,
                "message": "Disk unmounted"
            }
        }

        # Call the method
        result = self.resource.unmount_disk("disk1")

        # Verify the result
        assert result == self.client.execute_query.return_value["unmountDisk"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation UnmountDisk($id: String!) {
            unmountDisk(id: $id) {
                success
                message
            }
        }
        """,
            {"id": "disk1"}
        )

    def test_unmount_disk_error(self):
        """Test unmount_disk method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "unmountDisk": {
                "success": False,
                "message": "Disk not mounted"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to unmount disk: Disk not mounted"):
            self.resource.unmount_disk("disk1")

        self.client.execute_query.assert_called_once()

    def test_format_disk(self):
        """Test format_disk method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "formatDisk": {
                "success": True,
                "message": "Disk formatted"
            }
        }

        # Call the method
        result = self.resource.format_disk("disk1", "ext4")

        # Verify the result
        assert result == self.client.execute_query.return_value["formatDisk"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation FormatDisk($id: String!, $fsType: String!) {
            formatDisk(id: $id, fsType: $fsType) {
                success
                message
            }
        }
        """,
            {"id": "disk1", "fsType": "ext4"}
        )

    def test_format_disk_error(self):
        """Test format_disk method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "formatDisk": {
                "success": False,
                "message": "Disk in use"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to format disk: Disk in use"):
            self.resource.format_disk("disk1", "ext4")

        self.client.execute_query.assert_called_once()

    def test_clear_disk_statistics(self):
        """Test clear_disk_statistics method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "clearDiskStatistics": {
                "success": True,
                "message": "Disk statistics cleared"
            }
        }

        # Call the method
        result = self.resource.clear_disk_statistics("disk1")

        # Verify the result
        assert result == self.client.execute_query.return_value["clearDiskStatistics"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation ClearDiskStatistics($id: String!) {
            clearDiskStatistics(id: $id) {
                success
                message
            }
        }
        """,
            {"id": "disk1"}
        )

    def test_clear_disk_statistics_error(self):
        """Test clear_disk_statistics method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "clearDiskStatistics": {
                "success": False,
                "message": "Disk not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to clear disk statistics: Disk not found"):
            self.resource.clear_disk_statistics("disk1")

        self.client.execute_query.assert_called_once()

    def test_mount_array_disk(self):
        """Test mount_array_disk method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "mountArrayDisk": {
                "success": True,
                "message": "Array disk mounted"
            }
        }

        # Call the method
        result = self.resource.mount_array_disk("disk1")

        # Verify the result
        assert result == self.client.execute_query.return_value["mountArrayDisk"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation MountArrayDisk($slot: String!) {
            mountArrayDisk(slot: $slot) {
                success
                message
            }
        }
        """,
            {"slot": "disk1"}
        )

    def test_mount_array_disk_error(self):
        """Test mount_array_disk method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "mountArrayDisk": {
                "success": False,
                "message": "Array disk already mounted"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to mount array disk: Array disk already mounted"):
            self.resource.mount_array_disk("disk1")

        self.client.execute_query.assert_called_once()

    def test_unmount_array_disk(self):
        """Test unmount_array_disk method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "unmountArrayDisk": {
                "success": True,
                "message": "Array disk unmounted"
            }
        }

        # Call the method
        result = self.resource.unmount_array_disk("disk1")

        # Verify the result
        assert result == self.client.execute_query.return_value["unmountArrayDisk"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation UnmountArrayDisk($slot: String!) {
            unmountArrayDisk(slot: $slot) {
                success
                message
            }
        }
        """,
            {"slot": "disk1"}
        )

    def test_unmount_array_disk_error(self):
        """Test unmount_array_disk method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "unmountArrayDisk": {
                "success": False,
                "message": "Array disk not mounted"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to unmount array disk: Array disk not mounted"):
            self.resource.unmount_array_disk("disk1")

        self.client.execute_query.assert_called_once()

    def test_clear_array_disk_statistics(self):
        """Test clear_array_disk_statistics method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "clearArrayDiskStatistics": {
                "success": True,
                "message": "Array disk statistics cleared"
            }
        }

        # Call the method
        result = self.resource.clear_array_disk_statistics("disk1")

        # Verify the result
        assert result == self.client.execute_query.return_value["clearArrayDiskStatistics"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation ClearArrayDiskStatistics($slot: String!) {
            clearArrayDiskStatistics(slot: $slot) {
                success
                message
            }
        }
        """,
            {"slot": "disk1"}
        )

    def test_clear_array_disk_statistics_error(self):
        """Test clear_array_disk_statistics method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "clearArrayDiskStatistics": {
                "success": False,
                "message": "Array disk not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to clear array disk statistics: Array disk not found"):
            self.resource.clear_array_disk_statistics("disk1")

        self.client.execute_query.assert_called_once()

    def test_get_disk_smart(self):
        """Test get_disk_smart method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "disk": {
                "id": "disk1",
                "device": "/dev/sda",
                "name": "disk1",
                "smart": {
                    "supported": True,
                    "enabled": True,
                    "status": "PASS",
                    "temperature": 35,
                    "attributes": [
                        {
                            "id": 1,
                            "name": "Raw_Read_Error_Rate",
                            "value": 100,
                            "worst": 100,
                            "threshold": 50,
                            "raw": "0",
                            "status": "PASS"
                        }
                    ]
                }
            }
        }

        # Call the method
        result = self.resource.get_disk_smart("disk1")

        # Verify the result
        assert result == self.client.execute_query.return_value["disk"]["smart"]
        self.client.execute_query.assert_called_once_with(
            """
        query GetDiskSmart($id: String!) {
            disk(id: $id) {
                id
                device
                name
                smart {
                    supported
                    enabled
                    status
                    temperature
                    attributes {
                        id
                        name
                        value
                        worst
                        threshold
                        raw
                        status
                    }
                }
            }
        }
        """,
            {"id": "disk1"}
        )

    def test_get_disk_smart_error_missing_disk(self):
        """Test get_disk_smart method with error (missing disk field)."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing disk or smart field"):
            self.resource.get_disk_smart("disk1")

        self.client.execute_query.assert_called_once()

    def test_get_disk_smart_error_missing_smart(self):
        """Test get_disk_smart method with error (missing smart field)."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "disk": {
                "id": "disk1",
                "device": "/dev/sda",
                "name": "disk1"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing disk or smart field"):
            self.resource.get_disk_smart("disk1")

        self.client.execute_query.assert_called_once()


@pytest.mark.asyncio
class TestAsyncDiskResource:
    """Tests for the AsyncDiskResource class."""

    def setup_method(self):
        """Set up the test."""
        self.client = MagicMock()
        # Make execute_query a coroutine
        self.client.execute_query = AsyncMock()
        self.resource = AsyncDiskResource(self.client)

    async def test_init(self):
        """Test initialization."""
        assert self.resource.client == self.client

    async def test_get_disks(self):
        """Test get_disks method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "disks": [
                {
                    "id": "disk1",
                    "device": "/dev/sda",
                    "name": "disk1",
                    "size": 1000000,
                    "type": "sata",
                    "temperature": 35,
                    "smartStatus": "PASS"
                }
            ]
        }

        # Call the method
        result = await self.resource.get_disks()

        # Verify the result
        assert result == self.client.execute_query.return_value["disks"]
        self.client.execute_query.assert_called_once()

    async def test_get_disks_error(self):
        """Test get_disks method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing disks field"):
            await self.resource.get_disks()

        self.client.execute_query.assert_called_once()

    async def test_get_disk(self):
        """Test get_disk method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "disk": {
                "id": "disk1",
                "device": "/dev/sda",
                "deviceId": "sda",
                "deviceNode": "/dev/sda",
                "name": "disk1",
                "partitions": [
                    {
                        "number": 1,
                        "name": "sda1",
                        "fsType": "ext4",
                        "mountpoint": "/mnt/disk1",
                        "size": 1000000,
                        "used": 500000,
                        "free": 500000,
                        "color": "green",
                        "temp": 35,
                        "deviceId": "sda1",
                        "isArray": True
                    }
                ],
                "size": 1000000,
                "temp": 35,
                "status": "NORMAL",
                "interface": "SATA",
                "model": "WDC WD10EFRX",
                "protocol": "ATA",
                "rotationRate": 5400,
                "serial": "WD-WCC4E1234567",
                "type": "sata",
                "numReads": 1000,
                "numWrites": 500,
                "numErrors": 0,
                "color": "green",
                "rotational": True,
                "vendor": "Western Digital"
            }
        }

        # Call the method
        result = await self.resource.get_disk("disk1")

        # Verify the result
        assert result == self.client.execute_query.return_value["disk"]
        self.client.execute_query.assert_called_once()

    async def test_get_disk_error(self):
        """Test get_disk method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing disk field"):
            await self.resource.get_disk("disk1")

        self.client.execute_query.assert_called_once()

    async def test_mount_disk(self):
        """Test mount_disk method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "mountDisk": {
                "success": True,
                "message": "Disk mounted"
            }
        }

        # Call the method
        result = await self.resource.mount_disk("disk1")

        # Verify the result
        assert result == self.client.execute_query.return_value["mountDisk"]
        self.client.execute_query.assert_called_once()

    async def test_mount_disk_error(self):
        """Test mount_disk method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "mountDisk": {
                "success": False,
                "message": "Disk already mounted"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to mount disk: Disk already mounted"):
            await self.resource.mount_disk("disk1")

        self.client.execute_query.assert_called_once()

    async def test_unmount_disk(self):
        """Test unmount_disk method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "unmountDisk": {
                "success": True,
                "message": "Disk unmounted"
            }
        }

        # Call the method
        result = await self.resource.unmount_disk("disk1")

        # Verify the result
        assert result == self.client.execute_query.return_value["unmountDisk"]
        self.client.execute_query.assert_called_once()

    async def test_unmount_disk_error(self):
        """Test unmount_disk method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "unmountDisk": {
                "success": False,
                "message": "Disk not mounted"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to unmount disk: Disk not mounted"):
            await self.resource.unmount_disk("disk1")

        self.client.execute_query.assert_called_once()

    async def test_format_disk(self):
        """Test format_disk method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "formatDisk": {
                "success": True,
                "message": "Disk formatted"
            }
        }

        # Call the method
        result = await self.resource.format_disk("disk1", "ext4")

        # Verify the result
        assert result == self.client.execute_query.return_value["formatDisk"]
        self.client.execute_query.assert_called_once()

    async def test_format_disk_error(self):
        """Test format_disk method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "formatDisk": {
                "success": False,
                "message": "Disk in use"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to format disk: Disk in use"):
            await self.resource.format_disk("disk1", "ext4")

        self.client.execute_query.assert_called_once()

    async def test_clear_disk_statistics(self):
        """Test clear_disk_statistics method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "clearDiskStatistics": {
                "success": True,
                "message": "Disk statistics cleared"
            }
        }

        # Call the method
        result = await self.resource.clear_disk_statistics("disk1")

        # Verify the result
        assert result == self.client.execute_query.return_value["clearDiskStatistics"]
        self.client.execute_query.assert_called_once()

    async def test_clear_disk_statistics_error(self):
        """Test clear_disk_statistics method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "clearDiskStatistics": {
                "success": False,
                "message": "Disk not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to clear disk statistics: Disk not found"):
            await self.resource.clear_disk_statistics("disk1")

        self.client.execute_query.assert_called_once()

    async def test_mount_array_disk(self):
        """Test mount_array_disk method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "mountArrayDisk": {
                "success": True,
                "message": "Array disk mounted"
            }
        }

        # Call the method
        result = await self.resource.mount_array_disk("disk1")

        # Verify the result
        assert result == self.client.execute_query.return_value["mountArrayDisk"]
        self.client.execute_query.assert_called_once()

    async def test_mount_array_disk_error(self):
        """Test mount_array_disk method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "mountArrayDisk": {
                "success": False,
                "message": "Array disk already mounted"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to mount array disk: Array disk already mounted"):
            await self.resource.mount_array_disk("disk1")

        self.client.execute_query.assert_called_once()

    async def test_unmount_array_disk(self):
        """Test unmount_array_disk method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "unmountArrayDisk": {
                "success": True,
                "message": "Array disk unmounted"
            }
        }

        # Call the method
        result = await self.resource.unmount_array_disk("disk1")

        # Verify the result
        assert result == self.client.execute_query.return_value["unmountArrayDisk"]
        self.client.execute_query.assert_called_once()

    async def test_unmount_array_disk_error(self):
        """Test unmount_array_disk method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "unmountArrayDisk": {
                "success": False,
                "message": "Array disk not mounted"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to unmount array disk: Array disk not mounted"):
            await self.resource.unmount_array_disk("disk1")

        self.client.execute_query.assert_called_once()

    async def test_clear_array_disk_statistics(self):
        """Test clear_array_disk_statistics method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "clearArrayDiskStatistics": {
                "success": True,
                "message": "Array disk statistics cleared"
            }
        }

        # Call the method
        result = await self.resource.clear_array_disk_statistics("disk1")

        # Verify the result
        assert result == self.client.execute_query.return_value["clearArrayDiskStatistics"]
        self.client.execute_query.assert_called_once()

    async def test_clear_array_disk_statistics_error(self):
        """Test clear_array_disk_statistics method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "clearArrayDiskStatistics": {
                "success": False,
                "message": "Array disk not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to clear array disk statistics: Array disk not found"):
            await self.resource.clear_array_disk_statistics("disk1")

        self.client.execute_query.assert_called_once()

    async def test_get_disk_smart(self):
        """Test get_disk_smart method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "disk": {
                "id": "disk1",
                "device": "/dev/sda",
                "name": "disk1",
                "smart": {
                    "supported": True,
                    "enabled": True,
                    "status": "PASS",
                    "temperature": 35,
                    "attributes": [
                        {
                            "id": 1,
                            "name": "Raw_Read_Error_Rate",
                            "value": 100,
                            "worst": 100,
                            "threshold": 50,
                            "raw": "0",
                            "status": "PASS"
                        }
                    ]
                }
            }
        }

        # Call the method
        result = await self.resource.get_disk_smart("disk1")

        # Verify the result
        assert result == self.client.execute_query.return_value["disk"]["smart"]
        self.client.execute_query.assert_called_once()

    async def test_get_disk_smart_error_missing_disk(self):
        """Test get_disk_smart method with error (missing disk field)."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing disk or smart field"):
            await self.resource.get_disk_smart("disk1")

        self.client.execute_query.assert_called_once()

    async def test_get_disk_smart_error_missing_smart(self):
        """Test get_disk_smart method with error (missing smart field)."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "disk": {
                "id": "disk1",
                "device": "/dev/sda",
                "name": "disk1"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing disk or smart field"):
            await self.resource.get_disk_smart("disk1")

        self.client.execute_query.assert_called_once()
