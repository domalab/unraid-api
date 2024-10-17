from typing import List
import json
import asyncio
from ..unraid import Unraid
from .container import Container, RawContainer
from ..exceptions import ExecutionError, ParseError

class DockerModule:
    """
    Module for managing Docker containers on an Unraid server.

    This module provides methods for listing, starting, stopping, and monitoring Docker containers.
    """

    def __init__(self, instance: Unraid):
        """
        Initialize the Docker module.

        Args:
            instance: The Unraid instance to use for executing commands.
        """
        self.instance = instance

    async def fetch(self, path: str) -> dict:
        """
        Fetch data from the Docker API.

        Args:
            path: The API path to fetch.

        Returns:
            The JSON-decoded response from the Docker API.

        Raises:
            ExecutionError: If the command execution fails.
            ParseError: If the response cannot be parsed as JSON.
        """
        result = await self.instance.execute(f"curl --unix-socket /var/run/docker.sock {path}")
        if result['code'] != 0:
            raise ExecutionError("Got non-zero exit code while fetching Docker data")
        try:
            return json.loads(result['stdout'][0])
        except json.JSONDecodeError:
            raise ParseError("Failed to parse Docker API response as JSON")

    async def list(self) -> List[Container]:
        """
        List all Docker containers on the Unraid server.

        Returns:
            A list of Container objects representing the Docker containers on the server.

        Raises:
            ExecutionError: If the command to list containers fails.
            ParseError: If the container data cannot be parsed.
        """
        data = await self.fetch('http://localhost/v1.41/containers/json?all=1')
        try:
            return [Container(self.instance, RawContainer(**container)) for container in data]
        except Exception as e:
            raise ParseError(f"Failed to parse container data: {str(e)}")

    async def watch_containers(self, listener):
        """
        Watch for Docker container events on the Unraid server.

        Args:
            listener: An async function that will be called with each container event.

        Returns:
            A Future object that can be used to cancel the watch operation.

        Raises:
            ExecutionError: If the command to watch container events fails.
        """
        command = "docker events --filter 'type=container' --format '{{json .}}'"
        event, future = await self.instance.execute_stream(command)
        
        async def reader():
            while True:
                await event.wait()
                try:
                    container_event = json.loads(await self.instance.read_stream_output())
                    await listener(container_event)
                except json.JSONDecodeError:
                    # Log the error or handle it as appropriate
                    pass
                event.clear()

        asyncio.create_task(reader())
        return future