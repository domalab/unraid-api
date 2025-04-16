"""Tests for the VM resource."""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from unraid_api.exceptions import APIError, OperationError
from unraid_api.resources.vm import AsyncVMResource, VMResource


class TestVMResource:
    """Tests for the VMResource class."""

    def setup_method(self):
        """Set up the test."""
        self.client = MagicMock()
        self.resource = VMResource(self.client)

    def test_init(self):
        """Test initialization."""
        assert self.resource.client == self.client

    def test_get_vms(self):
        """Test get_vms method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "vms": {
                "domain": [
                    {
                        "uuid": "vm1",
                        "name": "vm1",
                        "state": "running"
                    }
                ]
            }
        }

        # Call the method
        result = self.resource.get_vms()

        # Verify the result
        assert result == self.client.execute_query.return_value["vms"]
        self.client.execute_query.assert_called_once_with(
            """
        query GetVMs {
            vms {
                domain {
                    uuid
                    name
                    state
                }
            }
        }
        """
        )

    def test_get_vms_error(self):
        """Test get_vms method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing vms field"):
            self.resource.get_vms()

        self.client.execute_query.assert_called_once()

    def test_get_vm(self):
        """Test get_vm method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "vm": {
                "id": "vm1",
                "name": "vm1",
                "coreCount": 4,
                "thread": 8,
                "memorySize": 4096,
                "status": "running",
                "icon": "icon.png",
                "description": "Test VM",
                "primaryGPU": "none",
                "autostart": True,
                "template": False,
                "disks": [
                    {
                        "name": "disk1",
                        "size": 50,
                        "driver": "virtio",
                        "interface": "virtio"
                    }
                ],
                "nics": [
                    {
                        "name": "nic1",
                        "mac": "00:11:22:33:44:55",
                        "bridge": "br0"
                    }
                ],
                "usbDevices": [],
                "usb": {
                    "enabled": False
                },
                "sound": {
                    "enabled": True
                }
            }
        }

        # Call the method
        result = self.resource.get_vm("vm1")

        # Verify the result
        assert result == self.client.execute_query.return_value["vm"]
        self.client.execute_query.assert_called_once_with(
            """
        query GetVM($id: String!) {
            vm(id: $id) {
                id
                name
                coreCount
                thread
                memorySize
                status
                icon
                description
                primaryGPU
                autostart
                template
                disks {
                    name
                    size
                    driver
                    interface
                }
                nics {
                    name
                    mac
                    bridge
                }
                usbDevices {
                    name
                    id
                }
                usb {
                    enabled
                }
                sound {
                    enabled
                }
            }
        }
        """,
            {"id": "vm1"}
        )

    def test_get_vm_error(self):
        """Test get_vm method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing vm field"):
            self.resource.get_vm("vm1")

        self.client.execute_query.assert_called_once()

    def test_start_vm(self):
        """Test start_vm method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "startVM": {
                "success": True,
                "message": "VM started"
            }
        }

        # Call the method
        result = self.resource.start_vm("vm1")

        # Verify the result
        assert result == self.client.execute_query.return_value["startVM"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation StartVM($id: String!) {
            startVM(id: $id) {
                success
                message
            }
        }
        """,
            {"id": "vm1"}
        )

    def test_start_vm_error(self):
        """Test start_vm method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "startVM": {
                "success": False,
                "message": "VM not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to start VM: VM not found"):
            self.resource.start_vm("vm1")

        self.client.execute_query.assert_called_once()

    def test_stop_vm(self):
        """Test stop_vm method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "stopVM": {
                "success": True,
                "message": "VM stopped"
            }
        }

        # Call the method
        result = self.resource.stop_vm("vm1")

        # Verify the result
        assert result == self.client.execute_query.return_value["stopVM"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation StopVM($id: String!) {
            stopVM(id: $id) {
                success
                message
            }
        }
        """,
            {"id": "vm1"}
        )

    def test_stop_vm_error(self):
        """Test stop_vm method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "stopVM": {
                "success": False,
                "message": "VM not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to stop VM: VM not found"):
            self.resource.stop_vm("vm1")

        self.client.execute_query.assert_called_once()

    def test_force_stop_vm(self):
        """Test force_stop_vm method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "forceStopVM": {
                "success": True,
                "message": "VM force stopped"
            }
        }

        # Call the method
        result = self.resource.force_stop_vm("vm1")

        # Verify the result
        assert result == self.client.execute_query.return_value["forceStopVM"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation ForceStopVM($id: String!) {
            forceStopVM(id: $id) {
                success
                message
            }
        }
        """,
            {"id": "vm1"}
        )

    def test_force_stop_vm_error(self):
        """Test force_stop_vm method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "forceStopVM": {
                "success": False,
                "message": "VM not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to force stop VM: VM not found"):
            self.resource.force_stop_vm("vm1")

        self.client.execute_query.assert_called_once()

    def test_restart_vm(self):
        """Test restart_vm method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "restartVM": {
                "success": True,
                "message": "VM restarted"
            }
        }

        # Call the method
        result = self.resource.restart_vm("vm1")

        # Verify the result
        assert result == self.client.execute_query.return_value["restartVM"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation RestartVM($id: String!) {
            restartVM(id: $id) {
                success
                message
            }
        }
        """,
            {"id": "vm1"}
        )

    def test_restart_vm_error(self):
        """Test restart_vm method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "restartVM": {
                "success": False,
                "message": "VM not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to restart VM: VM not found"):
            self.resource.restart_vm("vm1")

        self.client.execute_query.assert_called_once()

    def test_pause_vm(self):
        """Test pause_vm method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "pauseVM": {
                "success": True,
                "message": "VM paused"
            }
        }

        # Call the method
        result = self.resource.pause_vm("vm1")

        # Verify the result
        assert result == self.client.execute_query.return_value["pauseVM"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation PauseVM($id: String!) {
            pauseVM(id: $id) {
                success
                message
            }
        }
        """,
            {"id": "vm1"}
        )

    def test_pause_vm_error(self):
        """Test pause_vm method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "pauseVM": {
                "success": False,
                "message": "VM not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to pause VM: VM not found"):
            self.resource.pause_vm("vm1")

        self.client.execute_query.assert_called_once()

    def test_resume_vm(self):
        """Test resume_vm method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "resumeVM": {
                "success": True,
                "message": "VM resumed"
            }
        }

        # Call the method
        result = self.resource.resume_vm("vm1")

        # Verify the result
        assert result == self.client.execute_query.return_value["resumeVM"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation ResumeVM($id: String!) {
            resumeVM(id: $id) {
                success
                message
            }
        }
        """,
            {"id": "vm1"}
        )

    def test_resume_vm_error(self):
        """Test resume_vm method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "resumeVM": {
                "success": False,
                "message": "VM not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to resume VM: VM not found"):
            self.resource.resume_vm("vm1")

        self.client.execute_query.assert_called_once()

    def test_get_vm_templates(self):
        """Test get_vm_templates method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "vmTemplates": [
                {
                    "id": "template1",
                    "name": "template1",
                    "icon": "icon.png",
                    "description": "Test template"
                }
            ]
        }

        # Call the method
        result = self.resource.get_vm_templates()

        # Verify the result
        assert result == self.client.execute_query.return_value["vmTemplates"]
        self.client.execute_query.assert_called_once_with(
            """
        query GetVMTemplates {
            vmTemplates {
                id
                name
                icon
                description
            }
        }
        """
        )

    def test_get_vm_templates_error(self):
        """Test get_vm_templates method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing vmTemplates field"):
            self.resource.get_vm_templates()

        self.client.execute_query.assert_called_once()

    def test_create_vm_from_template(self):
        """Test create_vm_from_template method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "createVMFromTemplate": {
                "success": True,
                "message": "VM created"
            }
        }

        # Call the method
        result = self.resource.create_vm_from_template("template1", "new-vm")

        # Verify the result
        assert result == self.client.execute_query.return_value["createVMFromTemplate"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation CreateVMFromTemplate($templateId: String!, $name: String!) {
            createVMFromTemplate(templateId: $templateId, name: $name) {
                success
                message
            }
        }
        """,
            {"templateId": "template1", "name": "new-vm"}
        )

    def test_create_vm_from_template_error(self):
        """Test create_vm_from_template method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "createVMFromTemplate": {
                "success": False,
                "message": "Template not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to create VM from template: Template not found"):
            self.resource.create_vm_from_template("template1", "new-vm")

        self.client.execute_query.assert_called_once()

    def test_delete_vm(self):
        """Test delete_vm method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "deleteVM": {
                "success": True,
                "message": "VM deleted"
            }
        }

        # Call the method
        result = self.resource.delete_vm("vm1")

        # Verify the result
        assert result == self.client.execute_query.return_value["deleteVM"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation DeleteVM($id: String!) {
            deleteVM(id: $id) {
                success
                message
            }
        }
        """,
            {"id": "vm1"}
        )

    def test_delete_vm_error(self):
        """Test delete_vm method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "deleteVM": {
                "success": False,
                "message": "VM not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to delete VM: VM not found"):
            self.resource.delete_vm("vm1")

        self.client.execute_query.assert_called_once()


@pytest.mark.asyncio
class TestAsyncVMResource:
    """Tests for the AsyncVMResource class."""

    def setup_method(self):
        """Set up the test."""
        self.client = MagicMock()
        # Make execute_query a coroutine
        self.client.execute_query = AsyncMock()
        self.resource = AsyncVMResource(self.client)

    async def test_init(self):
        """Test initialization."""
        assert self.resource.client == self.client

    async def test_get_vms(self):
        """Test get_vms method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "vms": {
                "domain": [
                    {
                        "uuid": "vm1",
                        "name": "vm1",
                        "state": "running"
                    }
                ]
            }
        }

        # Call the method
        result = await self.resource.get_vms()

        # Verify the result
        assert result == self.client.execute_query.return_value["vms"]
        self.client.execute_query.assert_called_once()

    async def test_get_vms_error(self):
        """Test get_vms method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing vms field"):
            await self.resource.get_vms()

        self.client.execute_query.assert_called_once()

    async def test_get_vm(self):
        """Test get_vm method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "vm": {
                "id": "vm1",
                "name": "vm1",
                "coreCount": 4,
                "thread": 8,
                "memorySize": 4096,
                "status": "running",
                "icon": "icon.png",
                "description": "Test VM",
                "primaryGPU": "none",
                "autostart": True,
                "template": False,
                "disks": [
                    {
                        "name": "disk1",
                        "size": 50,
                        "driver": "virtio",
                        "interface": "virtio"
                    }
                ],
                "nics": [
                    {
                        "name": "nic1",
                        "mac": "00:11:22:33:44:55",
                        "bridge": "br0"
                    }
                ],
                "usbDevices": [],
                "usb": {
                    "enabled": False
                },
                "sound": {
                    "enabled": True
                }
            }
        }

        # Call the method
        result = await self.resource.get_vm("vm1")

        # Verify the result
        assert result == self.client.execute_query.return_value["vm"]
        self.client.execute_query.assert_called_once()

    async def test_get_vm_error(self):
        """Test get_vm method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing vm field"):
            await self.resource.get_vm("vm1")

        self.client.execute_query.assert_called_once()

    async def test_start_vm(self):
        """Test start_vm method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "startVM": {
                "success": True,
                "message": "VM started"
            }
        }

        # Call the method
        result = await self.resource.start_vm("vm1")

        # Verify the result
        assert result == self.client.execute_query.return_value["startVM"]
        self.client.execute_query.assert_called_once()

    async def test_start_vm_error(self):
        """Test start_vm method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "startVM": {
                "success": False,
                "message": "VM not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to start VM: VM not found"):
            await self.resource.start_vm("vm1")

        self.client.execute_query.assert_called_once()

    async def test_stop_vm(self):
        """Test stop_vm method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "stopVM": {
                "success": True,
                "message": "VM stopped"
            }
        }

        # Call the method
        result = await self.resource.stop_vm("vm1")

        # Verify the result
        assert result == self.client.execute_query.return_value["stopVM"]
        self.client.execute_query.assert_called_once()

    async def test_stop_vm_error(self):
        """Test stop_vm method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "stopVM": {
                "success": False,
                "message": "VM not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to stop VM: VM not found"):
            await self.resource.stop_vm("vm1")

        self.client.execute_query.assert_called_once()

    async def test_force_stop_vm(self):
        """Test force_stop_vm method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "forceStopVM": {
                "success": True,
                "message": "VM force stopped"
            }
        }

        # Call the method
        result = await self.resource.force_stop_vm("vm1")

        # Verify the result
        assert result == self.client.execute_query.return_value["forceStopVM"]
        self.client.execute_query.assert_called_once()

    async def test_force_stop_vm_error(self):
        """Test force_stop_vm method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "forceStopVM": {
                "success": False,
                "message": "VM not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to force stop VM: VM not found"):
            await self.resource.force_stop_vm("vm1")

        self.client.execute_query.assert_called_once()

    async def test_restart_vm(self):
        """Test restart_vm method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "restartVM": {
                "success": True,
                "message": "VM restarted"
            }
        }

        # Call the method
        result = await self.resource.restart_vm("vm1")

        # Verify the result
        assert result == self.client.execute_query.return_value["restartVM"]
        self.client.execute_query.assert_called_once()

    async def test_restart_vm_error(self):
        """Test restart_vm method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "restartVM": {
                "success": False,
                "message": "VM not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to restart VM: VM not found"):
            await self.resource.restart_vm("vm1")

        self.client.execute_query.assert_called_once()

    async def test_pause_vm(self):
        """Test pause_vm method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "pauseVM": {
                "success": True,
                "message": "VM paused"
            }
        }

        # Call the method
        result = await self.resource.pause_vm("vm1")

        # Verify the result
        assert result == self.client.execute_query.return_value["pauseVM"]
        self.client.execute_query.assert_called_once()

    async def test_pause_vm_error(self):
        """Test pause_vm method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "pauseVM": {
                "success": False,
                "message": "VM not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to pause VM: VM not found"):
            await self.resource.pause_vm("vm1")

        self.client.execute_query.assert_called_once()

    async def test_resume_vm(self):
        """Test resume_vm method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "resumeVM": {
                "success": True,
                "message": "VM resumed"
            }
        }

        # Call the method
        result = await self.resource.resume_vm("vm1")

        # Verify the result
        assert result == self.client.execute_query.return_value["resumeVM"]
        self.client.execute_query.assert_called_once()

    async def test_resume_vm_error(self):
        """Test resume_vm method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "resumeVM": {
                "success": False,
                "message": "VM not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to resume VM: VM not found"):
            await self.resource.resume_vm("vm1")

        self.client.execute_query.assert_called_once()

    async def test_get_vm_templates(self):
        """Test get_vm_templates method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "vmTemplates": [
                {
                    "id": "template1",
                    "name": "template1",
                    "icon": "icon.png",
                    "description": "Test template"
                }
            ]
        }

        # Call the method
        result = await self.resource.get_vm_templates()

        # Verify the result
        assert result == self.client.execute_query.return_value["vmTemplates"]
        self.client.execute_query.assert_called_once()

    async def test_get_vm_templates_error(self):
        """Test get_vm_templates method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing vmTemplates field"):
            await self.resource.get_vm_templates()

        self.client.execute_query.assert_called_once()

    async def test_create_vm_from_template(self):
        """Test create_vm_from_template method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "createVMFromTemplate": {
                "success": True,
                "message": "VM created"
            }
        }

        # Call the method
        result = await self.resource.create_vm_from_template("template1", "new-vm")

        # Verify the result
        assert result == self.client.execute_query.return_value["createVMFromTemplate"]
        self.client.execute_query.assert_called_once()

    async def test_create_vm_from_template_error(self):
        """Test create_vm_from_template method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "createVMFromTemplate": {
                "success": False,
                "message": "Template not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to create VM from template: Template not found"):
            await self.resource.create_vm_from_template("template1", "new-vm")

        self.client.execute_query.assert_called_once()

    async def test_delete_vm(self):
        """Test delete_vm method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "deleteVM": {
                "success": True,
                "message": "VM deleted"
            }
        }

        # Call the method
        result = await self.resource.delete_vm("vm1")

        # Verify the result
        assert result == self.client.execute_query.return_value["deleteVM"]
        self.client.execute_query.assert_called_once()

    async def test_delete_vm_error(self):
        """Test delete_vm method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "deleteVM": {
                "success": False,
                "message": "VM not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to delete VM: VM not found"):
            await self.resource.delete_vm("vm1")

        self.client.execute_query.assert_called_once()
        self.client.execute_query.assert_called_once()
