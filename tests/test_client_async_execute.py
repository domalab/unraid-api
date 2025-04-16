"""Fixed tests for the execute_query method in the async client module."""
from unittest.mock import MagicMock, patch

import httpx
import pytest
import pytest_asyncio

from tests.helpers import create_awaitable_mock
from unraid_api.client_async import AsyncUnraidClient
from unraid_api.exceptions import (AuthenticationError, ConnectionError,
                                   GraphQLError)


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
async def test_execute_query_with_api_key(client):
    """Test execute_query method with API key."""
    # Set up the client with an API key
    client.api_key = "test-api-key"

    # Create a mock response
    mock_response = MagicMock()
    mock_response.json = create_awaitable_mock({"data": {"test": "value"}})
    mock_response.raise_for_status = MagicMock()

    # Create a mock client
    mock_client = MagicMock()
    mock_client.__aenter__ = create_awaitable_mock(mock_client)
    mock_client.__aexit__ = create_awaitable_mock(None)
    mock_client.post = create_awaitable_mock(mock_response)

    # Patch httpx.AsyncClient to return our mock
    with patch("httpx.AsyncClient", return_value=mock_client):
        # Call the method
        result = await client.execute_query("query { test }")

        # Verify the result
        assert result == {"test": "value"}

        # Verify the API key was included in the headers
        _, kwargs = mock_client.post.call_args
        assert "x-api-key" in kwargs["headers"]
        assert kwargs["headers"]["x-api-key"] == "test-api-key"


@pytest.mark.asyncio
async def test_execute_query_with_auth_token(client):
    """Test execute_query method with auth token."""
    # Mock the auth manager's get_auth_headers method
    client._auth_manager.get_auth_headers = MagicMock(return_value={"Authorization": "Bearer test-token"})

    # Create a mock response
    mock_response = MagicMock()
    mock_response.json = create_awaitable_mock({"data": {"test": "value"}})
    mock_response.raise_for_status = MagicMock()

    # Create a mock client
    mock_client = MagicMock()
    mock_client.__aenter__ = create_awaitable_mock(mock_client)
    mock_client.__aexit__ = create_awaitable_mock(None)
    mock_client.post = create_awaitable_mock(mock_response)

    # Patch httpx.AsyncClient to return our mock
    with patch("httpx.AsyncClient", return_value=mock_client):
        # Call the method
        result = await client.execute_query("query { test }")

        # Verify the result
        assert result == {"test": "value"}

        # Verify the auth token was included in the headers
        _, kwargs = mock_client.post.call_args
        assert "Authorization" in kwargs["headers"]
        assert kwargs["headers"]["Authorization"] == "Bearer test-token"


@pytest.mark.asyncio
async def test_execute_query_graphql_error(client):
    """Test execute_query method with GraphQL error."""
    # Mock the auth manager's get_auth_headers method
    client._auth_manager.get_auth_headers = MagicMock(return_value={"Authorization": "Bearer test-token"})

    # Create a mock response with GraphQL errors
    mock_response = MagicMock()
    mock_response.json = create_awaitable_mock({
        "data": None,
        "errors": [{"message": "Test GraphQL error"}]
    })
    mock_response.raise_for_status = MagicMock()

    # Create a mock client
    mock_client = MagicMock()
    mock_client.__aenter__ = create_awaitable_mock(mock_client)
    mock_client.__aexit__ = create_awaitable_mock(None)
    mock_client.post = create_awaitable_mock(mock_response)

    # Patch httpx.AsyncClient to return our mock
    with patch("httpx.AsyncClient", return_value=mock_client):
        # Call the method and verify it raises an exception
        with pytest.raises(GraphQLError, match="Query failed: Test GraphQL error"):
            await client.execute_query("query { test }")


@pytest.mark.asyncio
async def test_execute_query_connection_error(client):
    """Test execute_query method with connection error."""
    # Mock the auth manager's get_auth_headers method
    client._auth_manager.get_auth_headers = MagicMock(return_value={"Authorization": "Bearer test-token"})

    # Create a mock client that raises a RequestError
    mock_client = MagicMock()
    mock_client.__aenter__ = create_awaitable_mock(mock_client)
    mock_client.__aexit__ = create_awaitable_mock(None)
    mock_client.post = create_awaitable_mock()
    mock_client.post.side_effect = httpx.RequestError("Test connection error", request=MagicMock())

    # Patch httpx.AsyncClient to return our mock
    with patch("httpx.AsyncClient", return_value=mock_client):
        # Call the method and verify it raises an exception
        with pytest.raises(ConnectionError, match="Failed to connect to Unraid server: Test connection error"):
            await client.execute_query("query { test }")


@pytest.mark.asyncio
async def test_execute_query_http_error_401(client):
    """Test execute_query method with HTTP 401 error."""
    # Mock the auth manager's get_auth_headers method
    client._auth_manager.get_auth_headers = MagicMock(return_value={"Authorization": "Bearer test-token"})

    # Create a mock response that raises an HTTPStatusError with 401
    mock_response = MagicMock()
    mock_response.status_code = 401

    # Create a mock client
    mock_client = MagicMock()
    mock_client.__aenter__ = create_awaitable_mock(mock_client)
    mock_client.__aexit__ = create_awaitable_mock(None)

    # Make the post method raise an HTTPStatusError
    http_error = httpx.HTTPStatusError("401 Unauthorized", request=MagicMock(), response=mock_response)
    mock_client.post = create_awaitable_mock()
    mock_client.post.side_effect = http_error

    # Patch httpx.AsyncClient to return our mock
    with patch("httpx.AsyncClient", return_value=mock_client):
        # Call the method and verify it raises an exception
        with pytest.raises(AuthenticationError, match="Authentication failed, token may be expired"):
            await client.execute_query("query { test }")


@pytest.mark.asyncio
async def test_execute_query_http_error_other(client):
    """Test execute_query method with other HTTP error."""
    # Mock the auth manager's get_auth_headers method
    client._auth_manager.get_auth_headers = MagicMock(return_value={"Authorization": "Bearer test-token"})

    # Create a mock response that raises an HTTPStatusError with 500
    mock_response = MagicMock()
    mock_response.status_code = 500

    # Create a mock client
    mock_client = MagicMock()
    mock_client.__aenter__ = create_awaitable_mock(mock_client)
    mock_client.__aexit__ = create_awaitable_mock(None)

    # Make the post method raise an HTTPStatusError
    http_error = httpx.HTTPStatusError("500 Server Error", request=MagicMock(), response=mock_response)
    mock_client.post = create_awaitable_mock()
    mock_client.post.side_effect = http_error

    # Patch httpx.AsyncClient to return our mock
    with patch("httpx.AsyncClient", return_value=mock_client):
        # Call the method and verify it raises an exception
        with pytest.raises(ConnectionError, match="HTTP error: 500 Server Error"):
            await client.execute_query("query { test }")
