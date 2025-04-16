"""Tests for the array resource."""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from unraid_api.exceptions import APIError, OperationError
from unraid_api.resources.array import ArrayResource, AsyncArrayResource


class TestArrayResource:
    """Tests for the ArrayResource class."""

    def setup_method(self):
        """Set up the test."""
        self.client = MagicMock()
        self.resource = ArrayResource(self.client)

    def test_init(self):
        """Test initialization."""
        assert self.resource.client == self.client

    def test_start_array(self):
        """Test start_array method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "startArray": {
                "success": True,
                "message": "Array started"
            }
        }

        # Call the method
        result = self.resource.start_array()

        # Verify the result
        assert result == self.client.execute_query.return_value["startArray"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation StartArray {
            startArray {
                success
                message
            }
        }
        """
        )

    def test_start_array_error(self):
        """Test start_array method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "startArray": {
                "success": False,
                "message": "Array already started"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to start array: Array already started"):
            self.resource.start_array()

        self.client.execute_query.assert_called_once()

    def test_stop_array(self):
        """Test stop_array method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "stopArray": {
                "success": True,
                "message": "Array stopped"
            }
        }

        # Call the method
        result = self.resource.stop_array()

        # Verify the result
        assert result == self.client.execute_query.return_value["stopArray"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation StopArray {
            stopArray {
                success
                message
            }
        }
        """
        )

    def test_stop_array_error(self):
        """Test stop_array method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "stopArray": {
                "success": False,
                "message": "Array already stopped"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to stop array: Array already stopped"):
            self.resource.stop_array()

        self.client.execute_query.assert_called_once()

    def test_get_array_status(self):
        """Test get_array_status method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "array": {
                "state": "STARTED",
                "capacity": {
                    "kilobytes": {
                        "free": 1000000,
                        "used": 2000000,
                        "total": 3000000
                    }
                },
                "boot": {
                    "id": "boot",
                    "device": "/dev/sda1",
                    "name": "boot",
                    "size": 100000,
                    "status": "NORMAL",
                    "type": "boot",
                    "fsType": "ext4"
                },
                "parities": [
                    {
                        "id": "parity1",
                        "size": 1000000,
                        "status": "NORMAL"
                    }
                ],
                "disks": [
                    {
                        "id": "disk1",
                        "size": 1000000,
                        "status": "NORMAL",
                        "fsType": "xfs"
                    }
                ],
                "caches": [
                    {
                        "id": "cache1",
                        "size": 500000,
                        "status": "NORMAL",
                        "fsType": "btrfs"
                    }
                ]
            }
        }

        # Call the method
        result = self.resource.get_array_status()

        # Verify the result
        assert result == self.client.execute_query.return_value["array"]
        self.client.execute_query.assert_called_once()

    def test_get_array_status_error(self):
        """Test get_array_status method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing array field"):
            self.resource.get_array_status()

        self.client.execute_query.assert_called_once()

    def test_add_disk_to_array(self):
        """Test add_disk_to_array method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "addDiskToArray": {
                "success": True,
                "message": "Disk added to array"
            }
        }

        # Call the method
        result = self.resource.add_disk_to_array("disk1", "/dev/sdb")

        # Verify the result
        assert result == self.client.execute_query.return_value["addDiskToArray"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation AddDiskToArray($slot: String!, $device: String!) {
            addDiskToArray(slot: $slot, device: $device) {
                success
                message
            }
        }
        """,
            {"slot": "disk1", "device": "/dev/sdb"}
        )

    def test_add_disk_to_array_error(self):
        """Test add_disk_to_array method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "addDiskToArray": {
                "success": False,
                "message": "Disk already in array"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to add disk to array: Disk already in array"):
            self.resource.add_disk_to_array("disk1", "/dev/sdb")

        self.client.execute_query.assert_called_once()

    def test_remove_disk_from_array(self):
        """Test remove_disk_from_array method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "removeDiskFromArray": {
                "success": True,
                "message": "Disk removed from array"
            }
        }

        # Call the method
        result = self.resource.remove_disk_from_array("disk1")

        # Verify the result
        assert result == self.client.execute_query.return_value["removeDiskFromArray"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation RemoveDiskFromArray($slot: String!) {
            removeDiskFromArray(slot: $slot) {
                success
                message
            }
        }
        """,
            {"slot": "disk1"}
        )

    def test_remove_disk_from_array_error(self):
        """Test remove_disk_from_array method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "removeDiskFromArray": {
                "success": False,
                "message": "Disk not in array"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to remove disk from array: Disk not in array"):
            self.resource.remove_disk_from_array("disk1")

        self.client.execute_query.assert_called_once()

    def test_start_parity_check(self):
        """Test start_parity_check method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "startParityCheck": {
                "success": True,
                "message": "Parity check started"
            }
        }

        # Call the method
        result = self.resource.start_parity_check()

        # Verify the result
        assert result == self.client.execute_query.return_value["startParityCheck"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation StartParityCheck($correcting: Boolean) {
            startParityCheck(correcting: $correcting) {
                success
                message
            }
        }
        """,
            {"correcting": True}
        )

    def test_start_parity_check_no_correcting(self):
        """Test start_parity_check method with correcting=False."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "startParityCheck": {
                "success": True,
                "message": "Parity check started"
            }
        }

        # Call the method
        result = self.resource.start_parity_check(correcting=False)

        # Verify the result
        assert result == self.client.execute_query.return_value["startParityCheck"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation StartParityCheck($correcting: Boolean) {
            startParityCheck(correcting: $correcting) {
                success
                message
            }
        }
        """,
            {"correcting": False}
        )

    def test_start_parity_check_error(self):
        """Test start_parity_check method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "startParityCheck": {
                "success": False,
                "message": "Parity check already running"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to start parity check: Parity check already running"):
            self.resource.start_parity_check()

        self.client.execute_query.assert_called_once()

    def test_pause_parity_check(self):
        """Test pause_parity_check method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "pauseParityCheck": {
                "success": True,
                "message": "Parity check paused"
            }
        }

        # Call the method
        result = self.resource.pause_parity_check()

        # Verify the result
        assert result == self.client.execute_query.return_value["pauseParityCheck"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation PauseParityCheck {
            pauseParityCheck {
                success
                message
            }
        }
        """
        )

    def test_pause_parity_check_error(self):
        """Test pause_parity_check method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "pauseParityCheck": {
                "success": False,
                "message": "No parity check running"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to pause parity check: No parity check running"):
            self.resource.pause_parity_check()

        self.client.execute_query.assert_called_once()

    def test_resume_parity_check(self):
        """Test resume_parity_check method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "resumeParityCheck": {
                "success": True,
                "message": "Parity check resumed"
            }
        }

        # Call the method
        result = self.resource.resume_parity_check()

        # Verify the result
        assert result == self.client.execute_query.return_value["resumeParityCheck"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation ResumeParityCheck {
            resumeParityCheck {
                success
                message
            }
        }
        """
        )

    def test_resume_parity_check_error(self):
        """Test resume_parity_check method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "resumeParityCheck": {
                "success": False,
                "message": "No paused parity check"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to resume parity check: No paused parity check"):
            self.resource.resume_parity_check()

        self.client.execute_query.assert_called_once()

    def test_cancel_parity_check(self):
        """Test cancel_parity_check method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "cancelParityCheck": {
                "success": True,
                "message": "Parity check cancelled"
            }
        }

        # Call the method
        result = self.resource.cancel_parity_check()

        # Verify the result
        assert result == self.client.execute_query.return_value["cancelParityCheck"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation CancelParityCheck {
            cancelParityCheck {
                success
                message
            }
        }
        """
        )

    def test_cancel_parity_check_error(self):
        """Test cancel_parity_check method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "cancelParityCheck": {
                "success": False,
                "message": "No parity check running"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to cancel parity check: No parity check running"):
            self.resource.cancel_parity_check()

        self.client.execute_query.assert_called_once()

    def test_get_parity_history(self):
        """Test get_parity_history method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "parityHistory": [
                {
                    "duration": 3600,
                    "speed": 100,
                    "status": "COMPLETED",
                    "errors": 0,
                    "date": "2023-01-01T00:00:00Z",
                    "corrected": True
                }
            ]
        }

        # Call the method
        result = self.resource.get_parity_history()

        # Verify the result
        assert result == self.client.execute_query.return_value["parityHistory"]
        self.client.execute_query.assert_called_once_with(
            """
        query GetParityHistory {
            parityHistory {
                duration
                speed
                status
                errors
                date
                corrected
            }
        }
        """
        )

    def test_get_parity_history_error(self):
        """Test get_parity_history method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing parityHistory field"):
            self.resource.get_parity_history()

        self.client.execute_query.assert_called_once()


@pytest.mark.asyncio
class TestAsyncArrayResource:
    """Tests for the AsyncArrayResource class."""

    def setup_method(self):
        """Set up the test."""
        self.client = MagicMock()
        # Make execute_query a coroutine
        self.client.execute_query = AsyncMock()
        self.resource = AsyncArrayResource(self.client)

    async def test_init(self):
        """Test initialization."""
        assert self.resource.client == self.client

    async def test_start_array(self):
        """Test start_array method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "startArray": {
                "success": True,
                "message": "Array started"
            }
        }

        # Call the method
        result = await self.resource.start_array()

        # Verify the result
        assert result == self.client.execute_query.return_value["startArray"]
        self.client.execute_query.assert_called_once()

    async def test_start_array_error(self):
        """Test start_array method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "startArray": {
                "success": False,
                "message": "Array already started"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to start array: Array already started"):
            await self.resource.start_array()

        self.client.execute_query.assert_called_once()

    async def test_stop_array(self):
        """Test stop_array method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "stopArray": {
                "success": True,
                "message": "Array stopped"
            }
        }

        # Call the method
        result = await self.resource.stop_array()

        # Verify the result
        assert result == self.client.execute_query.return_value["stopArray"]
        self.client.execute_query.assert_called_once()

    async def test_stop_array_error(self):
        """Test stop_array method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "stopArray": {
                "success": False,
                "message": "Array already stopped"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to stop array: Array already stopped"):
            await self.resource.stop_array()

        self.client.execute_query.assert_called_once()

    async def test_get_array_status(self):
        """Test get_array_status method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "array": {
                "state": "STARTED",
                "capacity": {
                    "kilobytes": {
                        "free": 1000000,
                        "used": 2000000,
                        "total": 3000000
                    }
                },
                "boot": {
                    "id": "boot",
                    "device": "/dev/sda1",
                    "name": "boot",
                    "size": 100000,
                    "status": "NORMAL",
                    "type": "boot",
                    "fsType": "ext4"
                },
                "parities": [
                    {
                        "id": "parity1",
                        "size": 1000000,
                        "status": "NORMAL"
                    }
                ],
                "disks": [
                    {
                        "id": "disk1",
                        "size": 1000000,
                        "status": "NORMAL",
                        "fsType": "xfs"
                    }
                ],
                "caches": [
                    {
                        "id": "cache1",
                        "size": 500000,
                        "status": "NORMAL",
                        "fsType": "btrfs"
                    }
                ]
            }
        }

        # Call the method
        result = await self.resource.get_array_status()

        # Verify the result
        assert result == self.client.execute_query.return_value["array"]
        self.client.execute_query.assert_called_once()

    async def test_get_array_status_error(self):
        """Test get_array_status method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing array field"):
            await self.resource.get_array_status()

        self.client.execute_query.assert_called_once()

    async def test_add_disk_to_array(self):
        """Test add_disk_to_array method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "addDiskToArray": {
                "success": True,
                "message": "Disk added to array"
            }
        }

        # Call the method
        result = await self.resource.add_disk_to_array("disk1", "/dev/sdb")

        # Verify the result
        assert result == self.client.execute_query.return_value["addDiskToArray"]
        self.client.execute_query.assert_called_once()

    async def test_add_disk_to_array_error(self):
        """Test add_disk_to_array method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "addDiskToArray": {
                "success": False,
                "message": "Disk already in array"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to add disk to array: Disk already in array"):
            await self.resource.add_disk_to_array("disk1", "/dev/sdb")

        self.client.execute_query.assert_called_once()

    async def test_remove_disk_from_array(self):
        """Test remove_disk_from_array method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "removeDiskFromArray": {
                "success": True,
                "message": "Disk removed from array"
            }
        }

        # Call the method
        result = await self.resource.remove_disk_from_array("disk1")

        # Verify the result
        assert result == self.client.execute_query.return_value["removeDiskFromArray"]
        self.client.execute_query.assert_called_once()

    async def test_remove_disk_from_array_error(self):
        """Test remove_disk_from_array method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "removeDiskFromArray": {
                "success": False,
                "message": "Disk not in array"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to remove disk from array: Disk not in array"):
            await self.resource.remove_disk_from_array("disk1")

        self.client.execute_query.assert_called_once()

    async def test_start_parity_check(self):
        """Test start_parity_check method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "startParityCheck": {
                "success": True,
                "message": "Parity check started"
            }
        }

        # Call the method
        result = await self.resource.start_parity_check()

        # Verify the result
        assert result == self.client.execute_query.return_value["startParityCheck"]
        self.client.execute_query.assert_called_once()

    async def test_start_parity_check_no_correcting(self):
        """Test start_parity_check method with correcting=False."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "startParityCheck": {
                "success": True,
                "message": "Parity check started"
            }
        }

        # Call the method
        result = await self.resource.start_parity_check(correcting=False)

        # Verify the result
        assert result == self.client.execute_query.return_value["startParityCheck"]
        self.client.execute_query.assert_called_once()

    async def test_start_parity_check_error(self):
        """Test start_parity_check method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "startParityCheck": {
                "success": False,
                "message": "Parity check already running"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to start parity check: Parity check already running"):
            await self.resource.start_parity_check()

        self.client.execute_query.assert_called_once()

    async def test_pause_parity_check(self):
        """Test pause_parity_check method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "pauseParityCheck": {
                "success": True,
                "message": "Parity check paused"
            }
        }

        # Call the method
        result = await self.resource.pause_parity_check()

        # Verify the result
        assert result == self.client.execute_query.return_value["pauseParityCheck"]
        self.client.execute_query.assert_called_once()

    async def test_pause_parity_check_error(self):
        """Test pause_parity_check method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "pauseParityCheck": {
                "success": False,
                "message": "No parity check running"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to pause parity check: No parity check running"):
            await self.resource.pause_parity_check()

        self.client.execute_query.assert_called_once()

    async def test_resume_parity_check(self):
        """Test resume_parity_check method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "resumeParityCheck": {
                "success": True,
                "message": "Parity check resumed"
            }
        }

        # Call the method
        result = await self.resource.resume_parity_check()

        # Verify the result
        assert result == self.client.execute_query.return_value["resumeParityCheck"]
        self.client.execute_query.assert_called_once()

    async def test_resume_parity_check_error(self):
        """Test resume_parity_check method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "resumeParityCheck": {
                "success": False,
                "message": "No paused parity check"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to resume parity check: No paused parity check"):
            await self.resource.resume_parity_check()

        self.client.execute_query.assert_called_once()

    async def test_cancel_parity_check(self):
        """Test cancel_parity_check method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "cancelParityCheck": {
                "success": True,
                "message": "Parity check cancelled"
            }
        }

        # Call the method
        result = await self.resource.cancel_parity_check()

        # Verify the result
        assert result == self.client.execute_query.return_value["cancelParityCheck"]
        self.client.execute_query.assert_called_once()

    async def test_cancel_parity_check_error(self):
        """Test cancel_parity_check method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "cancelParityCheck": {
                "success": False,
                "message": "No parity check running"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to cancel parity check: No parity check running"):
            await self.resource.cancel_parity_check()

        self.client.execute_query.assert_called_once()

    async def test_get_parity_history(self):
        """Test get_parity_history method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "parityHistory": [
                {
                    "duration": 3600,
                    "speed": 100,
                    "status": "COMPLETED",
                    "errors": 0,
                    "date": "2023-01-01T00:00:00Z",
                    "corrected": True
                }
            ]
        }

        # Call the method
        result = await self.resource.get_parity_history()

        # Verify the result
        assert result == self.client.execute_query.return_value["parityHistory"]
        self.client.execute_query.assert_called_once()

    async def test_get_parity_history_error(self):
        """Test get_parity_history method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing parityHistory field"):
            await self.resource.get_parity_history()

        self.client.execute_query.assert_called_once()
