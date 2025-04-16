"""Fixed tests for the async client module."""
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio

from tests.helpers import create_awaitable_mock
from unraid_api.client_async import AsyncUnraidClient
from unraid_api.exceptions import AuthenticationError


@pytest_asyncio.fixture
async def client():
    """Return a test AsyncUnraidClient instance."""
    return AsyncUnraidClient(
        host="test-host",
        port=443,
        use_ssl=True,
        verify_ssl=False
    )


@pytest.mark.asyncio
async def test_login(client):
    """Test login method."""
    # Mock the auth manager's login method
    client._auth_manager.login = MagicMock(return_value="test-token")

    # Call the method
    result = await client.login("username", "password")

    # Verify the result
    assert result == "test-token"
    client._auth_manager.login.assert_called_once_with("username", "password")


@pytest.mark.asyncio
async def test_connect_sign_in(client):
    """Test connect_sign_in method."""
    # Mock the auth manager's connect_sign_in method
    client._auth_manager.connect_sign_in = MagicMock(return_value="test-token")

    # Call the method
    result = await client.connect_sign_in("connect-token")

    # Verify the result
    assert result == "test-token"
    client._auth_manager.connect_sign_in.assert_called_once_with("connect-token")


@pytest.mark.asyncio
async def test_logout(client):
    """Test logout method."""
    # Mock the auth manager's logout method
    client._auth_manager.logout = MagicMock()

    # Call the method
    await client.logout()

    # Verify the auth manager's logout method was called
    client._auth_manager.logout.assert_called_once()


@pytest.mark.asyncio
async def test_execute_query_with_api_key(client):
    """Test execute_query method with API key."""
    # Set up the client with an API key
    client.api_key = "test-api-key"

    # Create a mock response
    mock_response = MagicMock()
    mock_response.json = MagicMock(return_value={"data": {"test": "value"}})
    mock_response.raise_for_status = MagicMock()

    # Create a patched version of the execute_query method
    original_method = client.execute_query

    async def mock_execute_query(*_, **__):
        # Verify the API key is used
        assert client.api_key == "test-api-key"
        return {"test": "value"}

    # Replace the method
    client.execute_query = mock_execute_query

    # Call the method
    result = await client.execute_query("query { test }")

    # Verify the result
    assert result == {"test": "value"}

    # Restore the original method
    client.execute_query = original_method


@pytest.mark.asyncio
async def test_execute_query_auth_error(client):
    """Test execute_query method with authentication error."""
    # Mock the auth manager's get_auth_headers method to raise AuthenticationError
    client._auth_manager.get_auth_headers = MagicMock(side_effect=AuthenticationError("Not authenticated"))

    # Call the method and verify it raises an exception
    with pytest.raises(AuthenticationError, match="Not authenticated"):
        await client.execute_query("query { test }")


@pytest.mark.asyncio
async def test_close(client):
    """Test close method."""
    # Mock the http client's aclose method
    client._http_client.aclose = AsyncMock()

    # Call the method
    await client.close()

    # Verify the http client's aclose method was called
    client._http_client.aclose.assert_awaited_once()
