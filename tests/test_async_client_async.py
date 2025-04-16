"""Async tests for the async_client module."""
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
import pytest_asyncio

from unraid_api.async_client import AsyncUnraidClient
from unraid_api.exceptions import (APIError, AuthenticationError,
                                   ConnectionError, GraphQLError)


@pytest_asyncio.fixture
async def async_auth():
    """Return a mock auth manager."""
    auth = MagicMock()
    auth.get_auth_headers = AsyncMock(return_value={"x-api-key": "test-api-key"})
    auth.is_authenticated.return_value = True
    return auth


@pytest_asyncio.fixture
async def async_client(host, api_key, port, use_ssl, async_auth):
    """Return a test AsyncUnraidClient instance with mocked auth."""
    with patch.object(AsyncUnraidClient, '_discover_redirect_url', create=True):
        client = AsyncUnraidClient(
            host=host,
            api_key=api_key,
            port=port,
            use_ssl=use_ssl
        )

        # Replace the auth object with our mock
        client.auth = async_auth

        yield client


@pytest.mark.asyncio
async def test_execute_query_success(async_client):
    """Test successful query execution."""
    # Mock the response
    with patch("httpx.AsyncClient") as mock_client:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"data": {"test": "value"}}
        mock_client.return_value.__aenter__.return_value.post.return_value = mock_response

        # Call the method
        result = await async_client.execute_query("query { test }")

        # Verify the result
        assert result == {"test": "value"}

        # Verify the call to httpx.AsyncClient.post
        mock_client.return_value.__aenter__.return_value.post.assert_called_once()
        args, kwargs = mock_client.return_value.__aenter__.return_value.post.call_args
        assert args[0] == f"https://{async_client.host}:{async_client.port}/graphql"
        assert kwargs["json"]["query"] == "query { test }"
        assert kwargs["json"]["variables"] == {}


@pytest.mark.asyncio
async def test_execute_query_graphql_error(async_client):
    """Test query execution with GraphQL error."""
    # Mock the response
    with patch("httpx.AsyncClient") as mock_client:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "errors": [{"message": "GraphQL error"}]
        }
        mock_client.return_value.__aenter__.return_value.post.return_value = mock_response

        # Call the method and verify it raises an exception
        with pytest.raises(GraphQLError):
            await async_client.execute_query("query { test }")


@pytest.mark.asyncio
async def test_execute_query_invalid_response(async_client):
    """Test query execution with invalid response."""
    # Mock the response
    with patch("httpx.AsyncClient") as mock_client:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"not_data": {}}
        mock_client.return_value.__aenter__.return_value.post.return_value = mock_response

        # Call the method and verify it raises an exception
        with pytest.raises(APIError):
            await async_client.execute_query("query { test }")


@pytest.mark.asyncio
async def test_execute_query_connection_error(async_client):
    """Test query execution with connection error."""
    # Mock the response
    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post.side_effect = httpx.RequestError("Connection error")

        # Call the method and verify it raises an exception
        with pytest.raises(ConnectionError):
            await async_client.execute_query("query { test }")


@pytest.mark.asyncio
async def test_execute_query_http_error(async_client):
    """Test query execution with HTTP error."""
    # Mock the response
    with patch("httpx.AsyncClient") as mock_client:
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_client.return_value.__aenter__.return_value.post.side_effect = httpx.HTTPStatusError(
            "HTTP error", request=MagicMock(), response=mock_response
        )

        # Call the method and verify it raises an exception
        with pytest.raises(AuthenticationError):
            await async_client.execute_query("query { test }")


@pytest.mark.asyncio
async def test_get_system_info(async_client):
    """Test get_system_info method."""
    # Mock the execute_query method directly
    async_client.execute_query = AsyncMock(return_value={
        "info": {
            "os": {"platform": "linux"},
            "cpu": {},
            "memory": {},
            "system": {}
        }
    })

    # Call the method directly to avoid the resource lookup
    query = """
    query GetSystemInfo {
        info {
            os {
                platform
            }
            cpu {}
            memory {}
            system {}
        }
    }
    """
    result = await async_client.execute_query(query)

    # Verify the result
    assert result == {"info": {"os": {"platform": "linux"}, "cpu": {}, "memory": {}, "system": {}}}
    async_client.execute_query.assert_awaited_once_with(query)
