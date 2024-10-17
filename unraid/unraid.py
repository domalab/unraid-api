import asyncio
from typing import Type, TypeVar
from .executors import Executor, ExecutorConfig
from . import docker, vm, system, userscripts, notifications, config
from .exceptions import ConnectionError, ExecutionError
from .util.command_queue import CommandQueue

T = TypeVar('T', bound=Executor)

class Unraid:
    """
    Main class for interacting with an Unraid server.

    This class provides access to various modules for managing different aspects of an Unraid server,
    including Docker containers, virtual machines, system information, user scripts, and notifications.

    Attributes:
        executor: The executor used for running commands on the Unraid server.
        docker: Module for managing Docker containers.
        vm: Module for managing virtual machines.
        system: Module for retrieving system information.
        userscripts: Module for managing user scripts.
        notifications: Module for managing notifications.
        unraid: Module for accessing Unraid-specific configurations.
        command_queue: Queue for managing concurrent command execution.
    """

    def __init__(self, executor_class: Type[T], executor_config: ExecutorConfig):
        """
        Initialize the Unraid instance.

        Args:
            executor_class: The class of the executor to use (e.g., SSHExecutor).
            executor_config: Configuration for the executor.
        """
        self.executor: T = executor_class(executor_config)
        self.docker = docker.DockerModule(self)
        self.vm = vm.VMModule(self)
        self.system = system.SystemModule(self)
        self.userscripts = userscripts.UserScriptsModule(self)
        self.notifications = notifications.NotificationModule(self)
        self.unraid = config.UnraidModule(self)
        self.command_queue = CommandQueue()

    async def connect(self):
        """
        Establish a connection to the Unraid server.

        Raises:
            ConnectionError: If the connection fails.
        """
        try:
            await self.executor.connect()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Unraid server: {str(e)}")

    async def disconnect(self):
        """
        Disconnect from the Unraid server.
        """
        await self.executor.disconnect()

    async def execute(self, command: str) -> dict:
        """
        Execute a command on the Unraid server.

        Args:
            command: The command to execute.

        Returns:
            A dictionary containing the command output and exit code.

        Raises:
            ExecutionError: If the command execution fails.
        """
        try:
            return await self.command_queue.do_task(self.executor.execute, command)
        except Exception as e:
            raise ExecutionError(f"Command execution failed: {str(e)}")

    async def execute_stream(self, command: str) -> tuple[asyncio.Event, asyncio.Future]:
        """
        Execute a command on the Unraid server with streaming output.

        Args:
            command: The command to execute.

        Returns:
            A tuple containing an Event for new output and a Future for the command completion.

        Raises:
            ExecutionError: If the streaming command execution fails.
        """
        try:
            return await self.command_queue.do_task(self.executor.execute_stream, command)
        except Exception as e:
            raise ExecutionError(f"Streaming command execution failed: {str(e)}")