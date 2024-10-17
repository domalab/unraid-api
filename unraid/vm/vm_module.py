from typing import List
from ..unraid import Unraid
from .vm import VM, VMState
from ..exceptions import ExecutionError, ParseError

class VMModule:
    """
    Module for managing virtual machines on an Unraid server.
    """

    def __init__(self, instance: Unraid):
        """
        Initialize the VM module.

        Args:
            instance: The Unraid instance to use for executing commands.
        """
        self.instance = instance

    async def list(self) -> List[VM]:
        """
        List all virtual machines on the Unraid server.

        Returns:
            A list of VM objects representing the virtual machines on the server.

        Raises:
            ExecutionError: If the command to list VMs fails.
            ParseError: If the VM data cannot be parsed.
        """
        result = await self.instance.execute('virsh list --all')
        if result['code'] != 0:
            raise ExecutionError('Got non-zero exit code while listing VMs')

        vms = result['stdout'][2:]  # Skip header lines
        parsed_vms = []

        for line in vms:
            try:
                parts = line.split()
                if len(parts) >= 3:
                    id = parts[0] if parts[0] != '-' else None
                    name = parts[1]
                    state = ' '.join(parts[2:])
                    parsed_vms.append(VM(self.instance, name, VMState(state), id))
            except ValueError as e:
                raise ParseError(f"Failed to parse VM data: {str(e)}")

        return parsed_vms

    async def get(self, name: str) -> VM:
        """
        Get a specific virtual machine by name.

        Args:
            name: The name of the virtual machine.

        Returns:
            A VM object representing the requested virtual machine.

        Raises:
            ExecutionError: If the command to get VM info fails.
            ParseError: If the VM data cannot be parsed.
            ValueError: If the VM is not found.
        """
        result = await self.instance.execute(f'virsh dominfo {name}')
        if result['code'] != 0:
            raise ExecutionError(f'Got non-zero exit code while getting info for VM "{name}"')

        vm_info = {}
        for line in result['stdout']:
            try:
                key, value = line.split(':', 1)
                vm_info[key.strip()] = value.strip()
            except ValueError:
                continue

        if 'Name' not in vm_info or 'State' not in vm_info:
            raise ParseError(f"Failed to parse VM data for {name}")

        return VM(self.instance, vm_info['Name'], VMState(vm_info['State']), vm_info.get('Id'))

    async def create(self, config: dict) -> VM:
        """
        Create a new virtual machine.

        Args:
            config: A dictionary containing the VM configuration.

        Returns:
            A VM object representing the newly created virtual machine.

        Raises:
            ExecutionError: If the command to create the VM fails.
        """
        # This is a placeholder. The actual implementation would depend on how Unraid creates VMs.
        # You might need to generate an XML configuration file and use 'virsh define' to create the VM.
        raise NotImplementedError("VM creation is not implemented yet")

    async def delete(self, name: str) -> None:
        """
        Delete a virtual machine.

        Args:
            name: The name of the virtual machine to delete.

        Raises:
            ExecutionError: If the command to delete the VM fails.
        """
        result = await self.instance.execute(f'virsh undefine {name}')
        if result['code'] != 0:
            raise ExecutionError(f'Got non-zero exit code while deleting VM "{name}"')