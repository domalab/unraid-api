"""Tests for the async client module to improve coverage."""
import json
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
import pytest_asyncio
import websockets

from unraid_api.client_async import AsyncUnraidClient
from unraid_api.exceptions import AuthenticationError, ConnectionError, GraphQLError, SubscriptionError


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
    
    # Mock the httpx.AsyncClient.post method
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": {"test": "value"}}
    mock_response.raise_for_status = MagicMock()
    
    mock_client = AsyncMock()
    mock_client.post.return_value = mock_response
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        # Call the method
        result = await client.execute_query("query { test }")
        
        # Verify the result
        assert result == {"test": "value"}
        
        # Verify the headers
        _, kwargs = mock_client.post.call_args
        assert kwargs["headers"]["x-api-key"] == "test-api-key"


@pytest.mark.asyncio
async def test_execute_query_with_auth_token(client):
    """Test execute_query method with auth token."""
    # Mock the auth manager's get_auth_headers method
    client._auth_manager.get_auth_headers = MagicMock(return_value={"Authorization": "Bearer test-token"})
    
    # Mock the httpx.AsyncClient.post method
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": {"test": "value"}}
    mock_response.raise_for_status = MagicMock()
    
    mock_client = AsyncMock()
    mock_client.post.return_value = mock_response
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        # Call the method
        result = await client.execute_query("query { test }")
        
        # Verify the result
        assert result == {"test": "value"}
        
        # Verify the headers
        _, kwargs = mock_client.post.call_args
        assert kwargs["headers"]["Authorization"] == "Bearer test-token"


@pytest.mark.asyncio
async def test_execute_query_auth_error(client):
    """Test execute_query method with authentication error."""
    # Mock the auth manager's get_auth_headers method to raise AuthenticationError
    client._auth_manager.get_auth_headers = MagicMock(side_effect=AuthenticationError("Not authenticated"))
    
    # Call the method and verify it raises an exception
    with pytest.raises(AuthenticationError, match="Not authenticated"):
        await client.execute_query("query { test }")


@pytest.mark.asyncio
async def test_execute_query_graphql_error(client):
    """Test execute_query method with GraphQL error."""
    # Mock the auth manager's get_auth_headers method
    client._auth_manager.get_auth_headers = MagicMock(return_value={"Authorization": "Bearer test-token"})
    
    # Mock the httpx.AsyncClient.post method
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": None,
        "errors": [{"message": "Test GraphQL error"}]
    }
    mock_response.raise_for_status = MagicMock()
    
    mock_client = AsyncMock()
    mock_client.post.return_value = mock_response
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        # Call the method and verify it raises an exception
        with pytest.raises(GraphQLError, match="Query failed: Test GraphQL error"):
            await client.execute_query("query { test }")


@pytest.mark.asyncio
async def test_execute_query_connection_error(client):
    """Test execute_query method with connection error."""
    # Mock the auth manager's get_auth_headers method
    client._auth_manager.get_auth_headers = MagicMock(return_value={"Authorization": "Bearer test-token"})
    
    # Mock the httpx.AsyncClient.post method to raise RequestError
    mock_client = AsyncMock()
    mock_client.post.side_effect = httpx.RequestError("Test connection error", request=MagicMock())
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        # Call the method and verify it raises an exception
        with pytest.raises(ConnectionError, match="Failed to connect to Unraid server: Test connection error"):
            await client.execute_query("query { test }")


@pytest.mark.asyncio
async def test_execute_query_http_error_401(client):
    """Test execute_query method with HTTP 401 error."""
    # Mock the auth manager's get_auth_headers method
    client._auth_manager.get_auth_headers = MagicMock(return_value={"Authorization": "Bearer test-token"})
    
    # Mock the httpx.AsyncClient.post method to raise HTTPStatusError with 401
    mock_response = MagicMock()
    mock_response.status_code = 401
    
    mock_client = AsyncMock()
    mock_client.post.side_effect = httpx.HTTPStatusError("401 Unauthorized", request=MagicMock(), response=mock_response)
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        # Call the method and verify it raises an exception
        with pytest.raises(AuthenticationError, match="Authentication failed, token may be expired"):
            await client.execute_query("query { test }")


@pytest.mark.asyncio
async def test_execute_query_http_error_other(client):
    """Test execute_query method with other HTTP error."""
    # Mock the auth manager's get_auth_headers method
    client._auth_manager.get_auth_headers = MagicMock(return_value={"Authorization": "Bearer test-token"})
    
    # Mock the httpx.AsyncClient.post method to raise HTTPStatusError with 500
    mock_response = MagicMock()
    mock_response.status_code = 500
    
    mock_client = AsyncMock()
    mock_client.post.side_effect = httpx.HTTPStatusError("500 Server Error", request=MagicMock(), response=mock_response)
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        # Call the method and verify it raises an exception
        with pytest.raises(ConnectionError, match="HTTP error: 500 Server Error"):
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


@pytest.mark.asyncio
async def test_subscribe_success(client):
    """Test subscribe method with successful subscription."""
    # Mock the auth manager's get_auth_headers method
    client._auth_manager.get_auth_headers = MagicMock(return_value={"Authorization": "Bearer test-token"})
    
    # Mock websockets.connect
    mock_websocket = AsyncMock()
    mock_websocket.recv = AsyncMock()
    mock_websocket.recv.side_effect = [
        json.dumps({"type": "connection_ack"}),
        json.dumps({"type": "data", "payload": {"data": {"test": "value1"}}}),
        json.dumps({"type": "data", "payload": {"data": {"test": "value2"}}}),
        json.dumps({"type": "complete"})
    ]
    
    # Mock the context manager
    mock_connect = AsyncMock()
    mock_connect.__aenter__.return_value = mock_websocket
    mock_connect.__aexit__.return_value = None
    
    with patch("websockets.connect", return_value=mock_connect):
        # Call the method
        results = []
        async for result in client.subscribe("subscription { test }"):
            results.append(result)
        
        # Verify the results
        assert results == [{"test": "value1"}, {"test": "value2"}]
        
        # Verify the websocket methods were called
        assert mock_websocket.send.call_count == 2  # init and subscription messages
        assert mock_websocket.recv.call_count == 4  # ack, data1, data2, complete


@pytest.mark.asyncio
async def test_subscribe_with_callback(client):
    """Test subscribe method with callback."""
    # Mock the auth manager's get_auth_headers method
    client._auth_manager.get_auth_headers = MagicMock(return_value={"Authorization": "Bearer test-token"})
    
    # Mock websockets.connect
    mock_websocket = AsyncMock()
    mock_websocket.recv = AsyncMock()
    mock_websocket.recv.side_effect = [
        json.dumps({"type": "connection_ack"}),
        json.dumps({"type": "data", "payload": {"data": {"test": "value"}}}),
        json.dumps({"type": "complete"})
    ]
    
    # Mock the context manager
    mock_connect = AsyncMock()
    mock_connect.__aenter__.return_value = mock_websocket
    mock_connect.__aexit__.return_value = None
    
    # Create a callback
    callback = MagicMock()
    
    with patch("websockets.connect", return_value=mock_connect):
        # Call the method
        # Since we're using a callback, we need to consume the generator
        async for _ in client.subscribe("subscription { test }", callback=callback):
            pass
        
        # Verify the callback was called
        callback.assert_called_once_with({"test": "value"})


@pytest.mark.asyncio
async def test_subscribe_connection_error(client):
    """Test subscribe method with connection error."""
    # Mock the auth manager's get_auth_headers method
    client._auth_manager.get_auth_headers = MagicMock(return_value={"Authorization": "Bearer test-token"})
    
    # Mock websockets.connect to raise ConnectionError
    with patch("websockets.connect", side_effect=ConnectionError("Test connection error")):
        # Call the method and verify it raises an exception
        with pytest.raises(ConnectionError, match="Failed to establish subscription connection: Test connection error"):
            async for _ in client.subscribe("subscription { test }"):
                pass


@pytest.mark.asyncio
async def test_subscribe_connection_closed(client):
    """Test subscribe method with connection closed."""
    # Mock the auth manager's get_auth_headers method
    client._auth_manager.get_auth_headers = MagicMock(return_value={"Authorization": "Bearer test-token"})
    
    # Mock websockets.connect
    mock_websocket = AsyncMock()
    mock_websocket.recv = AsyncMock()
    mock_websocket.recv.side_effect = [
        json.dumps({"type": "connection_ack"}),
        websockets.exceptions.ConnectionClosed(1000, "Test close")
    ]
    
    # Mock the context manager
    mock_connect = AsyncMock()
    mock_connect.__aenter__.return_value = mock_websocket
    mock_connect.__aexit__.return_value = None
    
    with patch("websockets.connect", return_value=mock_connect):
        # Call the method and verify it raises an exception
        with pytest.raises(ConnectionError, match="Subscription connection closed: 1000 \\(Test close\\)"):
            async for _ in client.subscribe("subscription { test }"):
                pass


@pytest.mark.asyncio
async def test_subscribe_ack_error(client):
    """Test subscribe method with acknowledgement error."""
    # Mock the auth manager's get_auth_headers method
    client._auth_manager.get_auth_headers = MagicMock(return_value={"Authorization": "Bearer test-token"})
    
    # Mock websockets.connect
    mock_websocket = AsyncMock()
    mock_websocket.recv = AsyncMock()
    mock_websocket.recv.side_effect = [
        json.dumps({"type": "connection_error", "payload": {"message": "Test ack error"}})
    ]
    
    # Mock the context manager
    mock_connect = AsyncMock()
    mock_connect.__aenter__.return_value = mock_websocket
    mock_connect.__aexit__.return_value = None
    
    with patch("websockets.connect", return_value=mock_connect):
        # Call the method and verify it raises an exception
        with pytest.raises(SubscriptionError, match="Failed to establish subscription connection:"):
            async for _ in client.subscribe("subscription { test }"):
                pass


@pytest.mark.asyncio
async def test_subscribe_error_message(client):
    """Test subscribe method with error message."""
    # Mock the auth manager's get_auth_headers method
    client._auth_manager.get_auth_headers = MagicMock(return_value={"Authorization": "Bearer test-token"})
    
    # Mock websockets.connect
    mock_websocket = AsyncMock()
    mock_websocket.recv = AsyncMock()
    mock_websocket.recv.side_effect = [
        json.dumps({"type": "connection_ack"}),
        json.dumps({"type": "error", "payload": {"message": "Test subscription error"}})
    ]
    
    # Mock the context manager
    mock_connect = AsyncMock()
    mock_connect.__aenter__.return_value = mock_websocket
    mock_connect.__aexit__.return_value = None
    
    with patch("websockets.connect", return_value=mock_connect):
        # Call the method and verify it raises an exception
        with pytest.raises(SubscriptionError, match="Subscription error: Test subscription error"):
            async for _ in client.subscribe("subscription { test }"):
                pass


@pytest.mark.asyncio
async def test_subscribe_data_with_errors(client):
    """Test subscribe method with errors in data payload."""
    # Mock the auth manager's get_auth_headers method
    client._auth_manager.get_auth_headers = MagicMock(return_value={"Authorization": "Bearer test-token"})
    
    # Mock websockets.connect
    mock_websocket = AsyncMock()
    mock_websocket.recv = AsyncMock()
    mock_websocket.recv.side_effect = [
        json.dumps({"type": "connection_ack"}),
        json.dumps({"type": "data", "payload": {"errors": [{"message": "Test data error"}]}})
    ]
    
    # Mock the context manager
    mock_connect = AsyncMock()
    mock_connect.__aenter__.return_value = mock_websocket
    mock_connect.__aexit__.return_value = None
    
    with patch("websockets.connect", return_value=mock_connect):
        # Call the method and verify it raises an exception
        with pytest.raises(SubscriptionError, match="Subscription error: Test data error"):
            async for _ in client.subscribe("subscription { test }"):
                pass


@pytest.mark.asyncio
async def test_subscribe_data_with_unknown_errors(client):
    """Test subscribe method with unknown errors in data payload."""
    # Mock the auth manager's get_auth_headers method
    client._auth_manager.get_auth_headers = MagicMock(return_value={"Authorization": "Bearer test-token"})
    
    # Mock websockets.connect
    mock_websocket = AsyncMock()
    mock_websocket.recv = AsyncMock()
    mock_websocket.recv.side_effect = [
        json.dumps({"type": "connection_ack"}),
        json.dumps({"type": "data", "payload": {"errors": "Not a list"}})
    ]
    
    # Mock the context manager
    mock_connect = AsyncMock()
    mock_connect.__aenter__.return_value = mock_websocket
    mock_connect.__aexit__.return_value = None
    
    with patch("websockets.connect", return_value=mock_connect):
        # Call the method and verify it raises an exception
        with pytest.raises(SubscriptionError, match="Subscription error: Unknown subscription error"):
            async for _ in client.subscribe("subscription { test }"):
                pass
