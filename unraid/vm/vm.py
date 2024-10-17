from enum import Enum
from typing import Optional
from ..unraid import Unraid
from ..exceptions import ExecutionError

class VMState(Enum):
    """Enum representing possible states of a virtual machine."""
    RUNNING = 'running'
    STOPPED = 'shut off'
    PAUSED = 'paused'
    IDLE = 'idle'
    IN_SHUTDOWN = 'in shutdown'
    CRASHED = 'crashed'
    SUSPENDED = 'pmsuspended'

class VM:
    """
    Represents a virtual machine on the Unraid server.
    """

    def __init__(self, instance: Unraid, name: str, state: VMState, id: Optional[str] = None):
        self.instance = instance
        self.name = name
        self.state = state
        self.id = id

    async def start(self) -> None:
        """
        Start the virtual machine.

        Raises:
            ExecutionError: If the start command fails.
        """
        result = await self.instance.execute(f'virsh start "{self.name}"')
        if result['code'] != 0:
            raise ExecutionError(f'Got non-zero exit code while starting VM "{self.name}"')

    async def shutdown(self, mode: str = 'acpi') -> None:
        """
        Shutdown the virtual machine.

        Args:
            mode: The shutdown mode to use (default is 'acpi').

        Raises:
            ExecutionError: If the shutdown command fails.
        """
        result = await self.instance.execute(f'virsh shutdown "{self.name}" --mode {mode}')
        if result['code'] != 0:
            raise ExecutionError(f'Got non-zero exit code while shutting down VM "{self.name}" with mode "{mode}"')

    async def reset(self) -> None:
        """
        Reset the virtual machine.

        Raises:
            ExecutionError: If the reset command fails.
        """
        result = await self.instance.execute(f'virsh reset "{self.name}"')
        if result['code'] != 0:
            raise ExecutionError(f'Got non-zero exit code while resetting VM "{self.name}"')

    async def suspend(self) -> None:
        """
        Suspend the virtual machine.

        Raises:
            ExecutionError: If the suspend command fails.
        """
        result = await self.instance.execute(f'virsh suspend "{self.name}"')
        if result['code'] != 0:
            raise ExecutionError(f'Got non-zero exit code while suspending VM "{self.name}"')

    async def resume(self) -> None:
        """
        Resume the suspended virtual machine.

        Raises:
            ExecutionError: If the resume command fails.
        """
        result = await self.instance.execute(f'virsh resume "{self.name}"')
        if result['code'] != 0:
            raise ExecutionError(f'Got non-zero exit code while resuming VM "{self.name}"')

    async def get_info(self) -> dict:
        """
        Get detailed information about the virtual machine.

        Returns:
            A dictionary containing detailed information about the VM.

        Raises:
            ExecutionError: If the command to get VM info fails.
        """
        result = await self.instance.execute(f'virsh dominfo "{self.name}"')
        if result['code'] != 0:
            raise ExecutionError(f'Got non-zero exit code while getting info for VM "{self.name}"')

        info = {}
        for line in result['stdout']:
            try:
                key, value = line.split(':', 1)
                info[key.strip()] = value.strip()
            except ValueError:
                continue

        return info

    def to_dict(self) -> dict:
        """
        Convert the VM object to a dictionary.

        Returns:
            A dictionary representation of the VM.
        """
        return {
            'name': self.name,
            'state': self.state.value,
            'id': self.id
        }