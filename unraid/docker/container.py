from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from ..unraid import Unraid
from ..exceptions import ExecutionError

class Port(BaseModel):
    IP: str
    PrivatePort: int
    PublicPort: int
    Type: str

class Mount(BaseModel):
    Type: str
    Source: str
    Destination: str
    Mode: str
    RW: bool
    Propagation: str

class RawContainer(BaseModel):
    Id: str
    Names: List[str]
    Image: str
    ImageID: str
    Command: str
    Created: int
    Ports: List[Port]
    Labels: dict[str, str]
    State: str
    Status: str
    HostConfig: dict
    NetworkSettings: dict
    Mounts: List[Mount]

class ContainerImage(BaseModel):
    encoded: str
    checksum: str

class Container:
    """
    Represents a Docker container on the Unraid server.
    """

    def __init__(self, instance: Unraid, data: RawContainer):
        self.instance = instance
        self.data = data
        self.id = data.Id
        self._image: Optional[ContainerImage] = None

    @property
    def name(self) -> str:
        """The name of the container."""
        return self.data.Names[0].replace('/', '')

    @property
    def state(self) -> str:
        """The current state of the container."""
        return self.data.State

    @property
    def created(self) -> datetime:
        """The creation time of the container."""
        return datetime.fromtimestamp(self.data.Created)

    async def get_image(self, ignore_cache: bool = False) -> ContainerImage:
        """
        Get the image data for the container.

        Args:
            ignore_cache: If True, fetch the image data even if it's already cached.

        Returns:
            A ContainerImage object containing the encoded image data and its checksum.

        Raises:
            ExecutionError: If unable to read the image data.
        """
        if self._image is not None and not ignore_cache:
            return self._image

        image_path = f"/var/lib/docker/unraid/images/{self.name}-icon.png"
        question_icon = "/usr/local/emhttp/plugins/dynamix.docker.manager/images/question.png"

        result = await self.instance.execute(
            f"[ -f {image_path} ] && (base64 {image_path} && base64 -w 0 {image_path} | sha512sum) || "
            f"(base64 {question_icon} && base64 -w 0 {question_icon} | sha512sum)"
        )

        if result['code'] != 0:
            raise ExecutionError(f"Unable to read image for container {self.id} / {self.name}")

        checksum = result['stdout'][-1].split(' ')[0]
        image = ''.join(result['stdout'][:-1])

        self._image = ContainerImage(encoded=image, checksum=checksum)
        return self._image

    async def stop(self) -> None:
        """
        Stop the container.

        Raises:
            ExecutionError: If the stop command fails.
        """
        result = await self.instance.execute(f'docker stop "{self.id}"')
        if result['code'] != 0:
            raise ExecutionError(f'Got non-zero exit code while stopping container "{self.id}"')

    async def start(self) -> None:
        """
        Start the container.

        Raises:
            ExecutionError: If the start command fails.
        """
        result = await self.instance.execute(f'docker start "{self.id}"')
        if result['code'] != 0:
            raise ExecutionError(f'Got non-zero exit code while starting container "{self.id}"')

    async def restart(self) -> None:
        """
        Restart the container.

        Raises:
            ExecutionError: If the restart command fails.
        """
        result = await self.instance.execute(f'docker restart "{self.id}"')
        if result['code'] != 0:
            raise ExecutionError(f'Got non-zero exit code while restarting container "{self.id}"')

    def to_dict(self) -> dict:
        """
        Convert the container object to a dictionary.

        Returns:
            A dictionary representation of the container.
        """
        return {
            'id': self.id,
            'name': self.name,
            'state': self.state,
            'created': self.created.isoformat(),
            'image': self.data.Image,
            'ports': [port.dict() for port in self.data.Ports],
            'mounts': [mount.dict() for mount in self.data.Mounts],
        }