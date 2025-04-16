"""Tests for the docker resource."""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from unraid_api.exceptions import APIError, OperationError
from unraid_api.resources.docker import AsyncDockerResource, DockerResource


class TestDockerResource:
    """Tests for the DockerResource class."""

    def setup_method(self):
        """Set up the test."""
        self.client = MagicMock()
        self.resource = DockerResource(self.client)

    def test_init(self):
        """Test initialization."""
        assert self.resource.client == self.client

    def test_get_containers(self):
        """Test get_containers method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "docker": {
                "containers": [
                    {
                        "id": "container1",
                        "names": ["container1"],
                        "image": "image1",
                        "state": "running",
                        "status": "Up 2 days"
                    }
                ]
            }
        }

        # Call the method
        result = self.resource.get_containers()

        # Verify the result
        assert result == self.client.execute_query.return_value["docker"]["containers"]
        self.client.execute_query.assert_called_once()

    def test_get_containers_error(self):
        """Test get_containers method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing docker.containers field"):
            self.resource.get_containers()

        self.client.execute_query.assert_called_once()

    def test_get_container(self):
        """Test get_container method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "dockerContainer": {
                "id": "container1",
                "name": "container1",
                "image": "image1",
                "imageId": "sha256:123456",
                "status": "Up 2 days",
                "state": "running"
            }
        }

        # Call the method
        result = self.resource.get_container("container1")

        # Verify the result
        assert result == self.client.execute_query.return_value["dockerContainer"]
        self.client.execute_query.assert_called_once_with(
            """
        query GetContainer($id: String!) {
            dockerContainer(id: $id) {
                id
                name
                image
                imageId
                status
                state
                created
                started
                finished
                exitCode
                autostart
                network
                repository
                command
                registry
                index
                nohc
                temp
                cpuPercent
                memUsage
                memLimit
                memPercent
                networkMode
                privileged
                restartPolicy
                logRotation
                ports {
                    IP
                    PrivatePort
                    PublicPort
                    Type
                }
                mounts {
                    name
                    source
                    destination
                    driver
                    mode
                    rw
                    propagation
                }
                icon
            }
        }
        """,
            {"id": "container1"}
        )

    def test_get_container_error(self):
        """Test get_container method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing dockerContainer field"):
            self.resource.get_container("container1")

        self.client.execute_query.assert_called_once()

    def test_start_container(self):
        """Test start_container method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "startContainer": {
                "success": True,
                "message": "Container started"
            }
        }

        # Call the method
        result = self.resource.start_container("container1")

        # Verify the result
        assert result == self.client.execute_query.return_value["startContainer"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation StartContainer($id: String!) {
            startContainer(id: $id) {
                success
                message
            }
        }
        """,
            {"id": "container1"}
        )

    def test_start_container_error(self):
        """Test start_container method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "startContainer": {
                "success": False,
                "message": "Container not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to start container: Container not found"):
            self.resource.start_container("container1")

        self.client.execute_query.assert_called_once()

    def test_stop_container(self):
        """Test stop_container method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "stopContainer": {
                "success": True,
                "message": "Container stopped"
            }
        }

        # Call the method
        result = self.resource.stop_container("container1")

        # Verify the result
        assert result == self.client.execute_query.return_value["stopContainer"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation StopContainer($id: String!) {
            stopContainer(id: $id) {
                success
                message
            }
        }
        """,
            {"id": "container1"}
        )

    def test_stop_container_error(self):
        """Test stop_container method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "stopContainer": {
                "success": False,
                "message": "Container not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to stop container: Container not found"):
            self.resource.stop_container("container1")

        self.client.execute_query.assert_called_once()

    def test_restart_container(self):
        """Test restart_container method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "restartContainer": {
                "success": True,
                "message": "Container restarted"
            }
        }

        # Call the method
        result = self.resource.restart_container("container1")

        # Verify the result
        assert result == self.client.execute_query.return_value["restartContainer"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation RestartContainer($id: String!) {
            restartContainer(id: $id) {
                success
                message
            }
        }
        """,
            {"id": "container1"}
        )

    def test_restart_container_error(self):
        """Test restart_container method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "restartContainer": {
                "success": False,
                "message": "Container not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to restart container: Container not found"):
            self.resource.restart_container("container1")

        self.client.execute_query.assert_called_once()

    def test_remove_container(self):
        """Test remove_container method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "removeContainer": {
                "success": True,
                "message": "Container removed"
            }
        }

        # Call the method
        result = self.resource.remove_container("container1")

        # Verify the result
        assert result == self.client.execute_query.return_value["removeContainer"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation RemoveContainer($id: String!) {
            removeContainer(id: $id) {
                success
                message
            }
        }
        """,
            {"id": "container1"}
        )

    def test_remove_container_error(self):
        """Test remove_container method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "removeContainer": {
                "success": False,
                "message": "Container not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to remove container: Container not found"):
            self.resource.remove_container("container1")

        self.client.execute_query.assert_called_once()

    def test_get_container_logs(self):
        """Test get_container_logs method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "containerLogs": "Log line 1\nLog line 2"
        }

        # Call the method
        result = self.resource.get_container_logs("container1")

        # Verify the result
        assert result == self.client.execute_query.return_value["containerLogs"]
        self.client.execute_query.assert_called_once_with(
            """
        query GetContainerLogs($id: String!, $tail: Int) {
            containerLogs(id: $id, tail: $tail)
        }
        """,
            {"id": "container1"}
        )

    def test_get_container_logs_with_tail(self):
        """Test get_container_logs method with tail parameter."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "containerLogs": "Log line 1\nLog line 2"
        }

        # Call the method
        result = self.resource.get_container_logs("container1", tail=10)

        # Verify the result
        assert result == self.client.execute_query.return_value["containerLogs"]
        self.client.execute_query.assert_called_once_with(
            """
        query GetContainerLogs($id: String!, $tail: Int) {
            containerLogs(id: $id, tail: $tail)
        }
        """,
            {"id": "container1", "tail": "10"}
        )

    def test_get_container_logs_error(self):
        """Test get_container_logs method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing containerLogs field"):
            self.resource.get_container_logs("container1")

        self.client.execute_query.assert_called_once()

    def test_get_images(self):
        """Test get_images method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "dockerImages": [
                {
                    "id": "image1",
                    "name": "image1",
                    "repository": "repo/image1",
                    "tag": "latest",
                    "created": "2023-01-01T00:00:00Z",
                    "size": 100000000,
                    "containers": 1
                }
            ]
        }

        # Call the method
        result = self.resource.get_images()

        # Verify the result
        assert result == self.client.execute_query.return_value["dockerImages"]
        self.client.execute_query.assert_called_once()

    def test_get_images_error(self):
        """Test get_images method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing dockerImages field"):
            self.resource.get_images()

        self.client.execute_query.assert_called_once()

    def test_pull_image(self):
        """Test pull_image method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "pullImage": {
                "success": True,
                "message": "Image pulled"
            }
        }

        # Call the method
        result = self.resource.pull_image("repo/image1")

        # Verify the result
        assert result == self.client.execute_query.return_value["pullImage"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation PullImage($repository: String!, $tag: String) {
            pullImage(repository: $repository, tag: $tag) {
                success
                message
            }
        }
        """,
            {"repository": "repo/image1", "tag": "latest"}
        )

    def test_pull_image_with_tag(self):
        """Test pull_image method with tag parameter."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "pullImage": {
                "success": True,
                "message": "Image pulled"
            }
        }

        # Call the method
        result = self.resource.pull_image("repo/image1", tag="1.0.0")

        # Verify the result
        assert result == self.client.execute_query.return_value["pullImage"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation PullImage($repository: String!, $tag: String) {
            pullImage(repository: $repository, tag: $tag) {
                success
                message
            }
        }
        """,
            {"repository": "repo/image1", "tag": "1.0.0"}
        )

    def test_pull_image_error(self):
        """Test pull_image method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "pullImage": {
                "success": False,
                "message": "Image not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to pull image: Image not found"):
            self.resource.pull_image("repo/image1")

        self.client.execute_query.assert_called_once()

    def test_remove_image(self):
        """Test remove_image method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "removeImage": {
                "success": True,
                "message": "Image removed"
            }
        }

        # Call the method
        result = self.resource.remove_image("image1")

        # Verify the result
        assert result == self.client.execute_query.return_value["removeImage"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation RemoveImage($id: String!) {
            removeImage(id: $id) {
                success
                message
            }
        }
        """,
            {"id": "image1"}
        )

    def test_remove_image_error(self):
        """Test remove_image method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "removeImage": {
                "success": False,
                "message": "Image not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to remove image: Image not found"):
            self.resource.remove_image("image1")

        self.client.execute_query.assert_called_once()

    def test_get_networks(self):
        """Test get_networks method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "dockerNetworks": [
                {
                    "id": "network1",
                    "name": "network1",
                    "driver": "bridge",
                    "scope": "local",
                    "subnet": "172.17.0.0/16",
                    "gateway": "172.17.0.1",
                    "containers": 1
                }
            ]
        }

        # Call the method
        result = self.resource.get_networks()

        # Verify the result
        assert result == self.client.execute_query.return_value["dockerNetworks"]
        self.client.execute_query.assert_called_once()

    def test_get_networks_error(self):
        """Test get_networks method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing dockerNetworks field"):
            self.resource.get_networks()

        self.client.execute_query.assert_called_once()


@pytest.mark.asyncio
class TestAsyncDockerResource:
    """Tests for the AsyncDockerResource class."""

    def setup_method(self):
        """Set up the test."""
        self.client = MagicMock()
        # Make execute_query a coroutine
        self.client.execute_query = AsyncMock()
        self.resource = AsyncDockerResource(self.client)

    async def test_init(self):
        """Test initialization."""
        assert self.resource.client == self.client

    async def test_get_containers(self):
        """Test get_containers method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "docker": {
                "containers": [
                    {
                        "id": "container1",
                        "names": ["container1"],
                        "image": "image1",
                        "state": "running",
                        "status": "Up 2 days"
                    }
                ]
            }
        }

        # Call the method
        result = await self.resource.get_containers()

        # Verify the result
        assert result == self.client.execute_query.return_value["docker"]["containers"]
        self.client.execute_query.assert_called_once()

    async def test_get_containers_error(self):
        """Test get_containers method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing docker.containers field"):
            await self.resource.get_containers()

        self.client.execute_query.assert_called_once()

    async def test_get_container(self):
        """Test get_container method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "dockerContainer": {
                "id": "container1",
                "name": "container1",
                "image": "image1",
                "imageId": "sha256:123456",
                "status": "Up 2 days",
                "state": "running"
            }
        }

        # Call the method
        result = await self.resource.get_container("container1")

        # Verify the result
        assert result == self.client.execute_query.return_value["dockerContainer"]
        self.client.execute_query.assert_called_once()

    async def test_get_container_error(self):
        """Test get_container method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing dockerContainer field"):
            await self.resource.get_container("container1")

        self.client.execute_query.assert_called_once()

    async def test_start_container(self):
        """Test start_container method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "startContainer": {
                "success": True,
                "message": "Container started"
            }
        }

        # Call the method
        result = await self.resource.start_container("container1")

        # Verify the result
        assert result == self.client.execute_query.return_value["startContainer"]
        self.client.execute_query.assert_called_once()

    async def test_start_container_error(self):
        """Test start_container method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "startContainer": {
                "success": False,
                "message": "Container already running"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to start container: Container already running"):
            await self.resource.start_container("container1")

        self.client.execute_query.assert_called_once()

    async def test_stop_container(self):
        """Test stop_container method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "stopContainer": {
                "success": True,
                "message": "Container stopped"
            }
        }

        # Call the method
        result = await self.resource.stop_container("container1")

        # Verify the result
        assert result == self.client.execute_query.return_value["stopContainer"]
        self.client.execute_query.assert_called_once()

    async def test_stop_container_error(self):
        """Test stop_container method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "stopContainer": {
                "success": False,
                "message": "Container not running"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to stop container: Container not running"):
            await self.resource.stop_container("container1")

        self.client.execute_query.assert_called_once()

    async def test_restart_container(self):
        """Test restart_container method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "restartContainer": {
                "success": True,
                "message": "Container restarted"
            }
        }

        # Call the method
        result = await self.resource.restart_container("container1")

        # Verify the result
        assert result == self.client.execute_query.return_value["restartContainer"]
        self.client.execute_query.assert_called_once()

    async def test_restart_container_error(self):
        """Test restart_container method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "restartContainer": {
                "success": False,
                "message": "Container not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to restart container: Container not found"):
            await self.resource.restart_container("container1")

        self.client.execute_query.assert_called_once()

    async def test_remove_container(self):
        """Test remove_container method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "removeContainer": {
                "success": True,
                "message": "Container removed"
            }
        }

        # Call the method
        result = await self.resource.remove_container("container1")

        # Verify the result
        assert result == self.client.execute_query.return_value["removeContainer"]
        self.client.execute_query.assert_called_once()

    async def test_remove_container_error(self):
        """Test remove_container method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "removeContainer": {
                "success": False,
                "message": "Container not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to remove container: Container not found"):
            await self.resource.remove_container("container1")

        self.client.execute_query.assert_called_once()

    async def test_get_container_logs(self):
        """Test get_container_logs method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "containerLogs": "Log line 1\nLog line 2"
        }

        # Call the method
        result = await self.resource.get_container_logs("container1")

        # Verify the result
        assert result == self.client.execute_query.return_value["containerLogs"]
        self.client.execute_query.assert_called_once()

    async def test_get_container_logs_with_tail(self):
        """Test get_container_logs method with tail parameter."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "containerLogs": "Log line 2"
        }

        # Call the method
        result = await self.resource.get_container_logs("container1", tail=1)

        # Verify the result
        assert result == self.client.execute_query.return_value["containerLogs"]
        self.client.execute_query.assert_called_once()

    async def test_get_container_logs_error(self):
        """Test get_container_logs method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing containerLogs field"):
            await self.resource.get_container_logs("container1")

        self.client.execute_query.assert_called_once()

    async def test_get_images(self):
        """Test get_images method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "dockerImages": [
                {
                    "id": "sha256:123456",
                    "name": "image1",
                    "tag": "latest",
                    "size": 100000000
                }
            ]
        }

        # Call the method
        result = await self.resource.get_images()

        # Verify the result
        assert result == self.client.execute_query.return_value["dockerImages"]
        self.client.execute_query.assert_called_once()

    async def test_get_images_error(self):
        """Test get_images method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing dockerImages field"):
            await self.resource.get_images()

        self.client.execute_query.assert_called_once()

    async def test_pull_image(self):
        """Test pull_image method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "pullImage": {
                "success": True,
                "message": "Image pulled"
            }
        }

        # Call the method
        result = await self.resource.pull_image("image1")

        # Verify the result
        assert result == self.client.execute_query.return_value["pullImage"]
        self.client.execute_query.assert_called_once()

    async def test_pull_image_with_tag(self):
        """Test pull_image method with tag parameter."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "pullImage": {
                "success": True,
                "message": "Image pulled"
            }
        }

        # Call the method
        result = await self.resource.pull_image("image1", tag="1.0")

        # Verify the result
        assert result == self.client.execute_query.return_value["pullImage"]
        self.client.execute_query.assert_called_once()

    async def test_pull_image_error(self):
        """Test pull_image method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "pullImage": {
                "success": False,
                "message": "Image not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to pull image: Image not found"):
            await self.resource.pull_image("image1")

        self.client.execute_query.assert_called_once()

    async def test_remove_image(self):
        """Test remove_image method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "removeImage": {
                "success": True,
                "message": "Image removed"
            }
        }

        # Call the method
        result = await self.resource.remove_image("image1")

        # Verify the result
        assert result == self.client.execute_query.return_value["removeImage"]
        self.client.execute_query.assert_called_once()

    async def test_remove_image_error(self):
        """Test remove_image method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "removeImage": {
                "success": False,
                "message": "Image not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to remove image: Image not found"):
            await self.resource.remove_image("image1")

        self.client.execute_query.assert_called_once()

    async def test_get_networks(self):
        """Test get_networks method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "dockerNetworks": [
                {
                    "id": "network1",
                    "name": "bridge",
                    "driver": "bridge",
                    "scope": "local"
                }
            ]
        }

        # Call the method
        result = await self.resource.get_networks()

        # Verify the result
        assert result == self.client.execute_query.return_value["dockerNetworks"]
        self.client.execute_query.assert_called_once()

    async def test_get_networks_error(self):
        """Test get_networks method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing dockerNetworks field"):
            await self.resource.get_networks()

        self.client.execute_query.assert_called_once()
