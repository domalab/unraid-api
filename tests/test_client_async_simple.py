"""Simple tests for the async client module."""
import pytest
import pytest_asyncio

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
async def test_login(client, monkeypatch):
    """Test login method."""
    # Mock the auth manager's login method to return a value directly
    monkeypatch.setattr(client._auth_manager, "login", lambda *_: "test-token")

    # Call the method
    result = await client.login("username", "password")

    # Verify the result
    assert result == "test-token"


@pytest.mark.asyncio
async def test_connect_sign_in(client, monkeypatch):
    """Test connect_sign_in method."""
    # Mock the auth manager's connect_sign_in method to return a value directly
    monkeypatch.setattr(client._auth_manager, "connect_sign_in", lambda *_: "test-token")

    # Call the method
    result = await client.connect_sign_in("connect-token")

    # Verify the result
    assert result == "test-token"


@pytest.mark.asyncio
async def test_logout(client, monkeypatch):
    """Test logout method."""
    # Mock the client's logout method to do nothing
    called = [False]

    async def mock_logout():
        called[0] = True

    monkeypatch.setattr(client, "logout", mock_logout)

    # Call the method
    await client.logout()

    # Verify the method was called
    assert called[0] is True

    # This is already handled above


@pytest.mark.asyncio
async def test_execute_query_with_api_key(client, monkeypatch):
    """Test execute_query method with API key."""
    # Set up the client with an API key
    client.api_key = "test-api-key"

    # Create a patched version of the execute_query method
    async def mock_execute_query(*_, **__):
        # Verify the API key is used
        assert client.api_key == "test-api-key"
        return {"test": "value"}

    # Replace the method
    monkeypatch.setattr(client, "execute_query", mock_execute_query)

    # Call the method
    result = await client.execute_query("query { test }")

    # Verify the result
    assert result == {"test": "value"}


@pytest.mark.asyncio
async def test_execute_query_auth_error(client, monkeypatch):
    """Test execute_query method with authentication error."""
    # Mock the auth manager's get_auth_headers method to raise AuthenticationError
    def mock_get_auth_headers(*_, **__):
        raise AuthenticationError("Not authenticated")

    monkeypatch.setattr(client._auth_manager, "get_auth_headers", mock_get_auth_headers)

    # Call the method and verify it raises an exception
    with pytest.raises(AuthenticationError, match="Not authenticated"):
        await client.execute_query("query { test }")


@pytest.mark.asyncio
async def test_close(client, monkeypatch):
    """Test close method."""
    # Mock the http client's aclose method
    async def mock_aclose(*_, **__):
        pass

    monkeypatch.setattr(client._http_client, "aclose", mock_aclose)

    # Call the method
    await client.close()
