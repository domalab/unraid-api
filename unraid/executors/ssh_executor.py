import asyncio
import asyncssh
from typing import Optional
from .executor import Executor, ExecutorConfig, ExecuteResult
from ..exceptions import ConnectionError, ExecutionError

class SSHExecutor(Executor):
    """
    Executor that uses SSH to run commands on an Unraid server.
    """

    def __init__(self, config: ExecutorConfig):
        super().__init__(config)
        self.connection: Optional[asyncssh.SSHClientConnection] = None

    async def connect(self) -> None:
        """
        Establish an SSH connection to the Unraid server.

        Raises:
            ConnectionError: If the connection fails.
        """
        try:
            self.connection = await asyncssh.connect(
                self.config['host'],
                username=self.config['username'],
                password=self.config['password'],
                port=self.config['port'],
                known_hosts=None  # Note: In production, use proper known_hosts handling
            )
        except Exception as e:
            raise ConnectionError(f"Failed to establish SSH connection: {str(e)}")

    async def disconnect(self) -> None:
        """Disconnect the SSH connection from the Unraid server."""
        if self.connection:
            self.connection.close()
            await self.connection.wait_closed()

    async def execute(self, command: str) -> ExecuteResult:
        """
        Execute a command on the Unraid server via SSH.

        Args:
            command: The command to execute.

        Returns:
            An ExecuteResult containing the command output and exit code.

        Raises:
            ExecutionError: If the command execution fails.
        """
        if not self.connection:
            raise ConnectionError("Not connected to Unraid server")
        
        try:
            process = await self.connection.run(command)
            return {
                'stdout': process.stdout.splitlines(),
                'stderr': process.stderr.splitlines(),
                'code': process.exit_status,
                'signal': process.exit_signal
            }
        except Exception as e:
            raise ExecutionError(f"Command execution failed: {str(e)}")

    async def execute_stream(self, command: str) -> tuple[asyncio.Event, asyncio.Future]:
        """
        Execute a command on the Unraid server via SSH with streaming output.

        Args:
            command: The command to execute.

        Returns:
            A tuple containing an Event for new output and a Future for the command completion.

        Raises:
            ExecutionError: If the streaming command execution fails.
        """
        if not self.connection:
            raise ConnectionError("Not connected to Unraid server")

        try:
            process = await self.connection.create_process(command)
            event = asyncio.Event()
            future = asyncio.create_task(process.wait())

            async def reader():
                while True:
                    line = await process.stdout.readline()
                    if not line:
                        break
                    event.set()
                    event.clear()

            asyncio.create_task(reader())
            return event, future
        except Exception as e:
            raise ExecutionError(f"Streaming command execution failed: {str(e)}")