from abc import ABC, abstractmethod
from typing import TypedDict, Optional
import asyncio

class ExecutorConfig(TypedDict):
    host: str
    username: str
    password: Optional[str]
    port: int = 22

class ExecuteResult(TypedDict):
    stdout: list[str]
    stderr: list[str]
    code: int
    signal: Optional[str]

class Executor(ABC):
    """
    Abstract base class for executors that run commands on an Unraid server.
    """

    def __init__(self, config: ExecutorConfig):
        self.config = config

    @abstractmethod
    async def connect(self) -> None:
        """Establish a connection to the Unraid server."""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from the Unraid server."""
        pass

    @abstractmethod
    async def execute(self, command: str) -> ExecuteResult:
        """
        Execute a command on the Unraid server.

        Args:
            command: The command to execute.

        Returns:
            An ExecuteResult containing the command output and exit code.
        """
        pass

    @abstractmethod
    async def execute_stream(self, command: str) -> tuple[asyncio.Event, asyncio.Future]:
        """
        Execute a command on the Unraid server with streaming output.

        Args:
            command: The command to execute.

        Returns:
            A tuple containing an Event for new output and a Future for the command completion.
        """
        pass