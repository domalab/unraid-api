"""Pytest configuration and shared fixtures."""
import os
import tempfile
import time
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from unraid_api.async_client import AsyncUnraidClient
from unraid_api.auth import AuthManager
from unraid_api.client import UnraidClient
from unraid_api.resources.array import ArrayResource
from unraid_api.resources.disk import DiskResource
from unraid_api.resources.docker import DockerResource
from unraid_api.resources.info import InfoResource
from unraid_api.resources.vm import VMResource
from unraid_api.subscription import Subscription


@pytest.fixture
def host():
    """Return a test host."""
    return "test-host"


@pytest.fixture
def port():
    """Return a test port."""
    return 443


@pytest.fixture
def use_ssl():
    """Return a test use_ssl value."""
    return True


@pytest.fixture
def api_key():
    """Return a test API key."""
    return "test-api-key"


@pytest.fixture
def temp_file():
    """Create a temporary file and clean it up after the test."""
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()

    # Create a mock token file
    with open(temp_file.name, 'w') as f:
        f.write('{}')

    yield temp_file

    # Clean up
    if os.path.exists(temp_file.name):
        os.unlink(temp_file.name)


@pytest.fixture
def auth_manager(host, port, use_ssl, temp_file):
    """Return a test AuthManager instance."""
    return AuthManager(
        host=host,
        port=port,
        use_ssl=use_ssl,
        token_persistence_path=temp_file.name,
        verify_ssl=True
    )


@pytest.fixture
def mock_auth():
    """Return a mock auth manager."""
    mock_auth = MagicMock()
    mock_auth_instance = MagicMock()
    mock_auth.return_value = mock_auth_instance
    return mock_auth, mock_auth_instance


@pytest.fixture
def client(host, api_key, port, use_ssl):
    """Return a test UnraidClient instance with mocked execute_query."""
    with patch.object(UnraidClient, '_discover_redirect_url'):
        client = UnraidClient(
            host=host,
            api_key=api_key,
            port=port,
            use_ssl=use_ssl,
            verify_ssl=False
        )
        # Create a mock for execute_query that returns the expected value
        mock_execute_query = MagicMock()
        mock_execute_query.return_value = {"test": "value"}
        client.execute_query = mock_execute_query

        # Mock the resource objects
        client.array = MagicMock()
        client.disk = MagicMock()
        client.docker = MagicMock()
        client.vm = MagicMock()
        client.notification = MagicMock()
        client.user = MagicMock()
        client.info = MagicMock()
        client.info.get_system_info.return_value = {"os": {"platform": "linux"}, "cpu": {}, "memory": {}, "system": {}}
        client.config = MagicMock()

        return client


@pytest.fixture
def async_client(host, api_key, port, use_ssl):
    """Return a test AsyncUnraidClient instance with mocked auth."""
    with patch.object(AsyncUnraidClient, '_discover_redirect_url', create=True):
        client = AsyncUnraidClient(
            host=host,
            api_key=api_key,
            port=port,
            use_ssl=use_ssl
        )

        # Mock the auth object
        client.auth = MagicMock()
        client.auth.is_authenticated.return_value = True
        client.auth.get_auth_headers = AsyncMock(return_value={"x-api-key": api_key})

        # Mock the execute_query method
        client.execute_query = AsyncMock(return_value={"test": "value"})

        # Mock the resource objects
        client._resources = {}
        client.get_resource = MagicMock()
        mock_resource = MagicMock()
        client.get_resource.return_value = mock_resource

        return client


@pytest.fixture
def array_resource(client):
    """Return a test ArrayResource instance."""
    return ArrayResource(client)


@pytest.fixture
def disk_resource(client):
    """Return a test DiskResource instance."""
    return DiskResource(client)


@pytest.fixture
def docker_resource(client):
    """Return a test DockerResource instance."""
    return DockerResource(client)


@pytest.fixture
def info_resource(client):
    """Return a test InfoResource instance."""
    return InfoResource(client)


@pytest.fixture
def vm_resource(client):
    """Return a test VMResource instance."""
    return VMResource(client)


@pytest.fixture
def subscription():
    """Return a test Subscription instance."""
    client = MagicMock()
    client.host = "test-host"
    client.port = 443
    client.use_ssl = True
    client.auth = MagicMock()
    client.auth.get_access_token = MagicMock()

    callback = MagicMock()

    return Subscription(
        client=client,
        subscription_query="subscription { test }",
        variables={},
        callback=callback
    )
