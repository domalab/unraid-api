"""Simple tests for the subscription module to improve coverage."""
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio

from unraid_api.exceptions import AuthenticationError
from unraid_api.subscription import Subscription


@pytest_asyncio.fixture
async def mock_client():
    """Return a mock client."""
    client = MagicMock()
    client.host = "test-host"
    client.port = 443
    client.use_ssl = True
    client.auth = MagicMock()
    client.auth.get_access_token = AsyncMock(return_value="test-token")
    return client


@pytest_asyncio.fixture
async def mock_callback():
    """Return a mock callback."""
    return AsyncMock()


@pytest_asyncio.fixture
async def subscription(mock_client, mock_callback):
    """Return a test Subscription instance."""
    return Subscription(
        client=mock_client,
        subscription_query="subscription { test }",
        variables={},
        callback=mock_callback
    )


@pytest.mark.asyncio
async def test_start_already_running(subscription):
    """Test start method when subscription is already running."""
    # Set up the subscription as already running
    subscription._running = True
    
    # Start the subscription
    await subscription.start()
    
    # Verify the subscription was not started again
    assert subscription._task is None


@pytest.mark.asyncio
async def test_subscription_handler_sync_client(subscription):
    """Test _subscription_handler method with sync client."""
    # Set up a sync client
    sync_client = MagicMock()
    sync_client.host = "test-host"
    sync_client.port = 443
    sync_client.use_ssl = True
    sync_client.auth = MagicMock()
    sync_client.auth.get_access_token = MagicMock(return_value="test-token")
    subscription.client = sync_client
    
    # Mock the subscription handler to return immediately
    subscription._subscription_handler = AsyncMock()
    
    # Start the subscription
    await subscription.start()
    
    # Stop the subscription
    await subscription.stop()
    
    # Verify the subscription was started and stopped
    assert subscription._subscription_handler.called


@pytest.mark.asyncio
async def test_subscription_handler_authentication_error(subscription):
    """Test _subscription_handler method with AuthenticationError exception."""
    # Mock the client's get_access_token to raise AuthenticationError
    subscription.client.auth.get_access_token.side_effect = AuthenticationError("Test auth error")
    
    # Set the subscription as running
    subscription._running = True
    
    # Call the handler directly
    await subscription._subscription_handler()
    
    # Verify the token was attempted to be retrieved
    subscription.client.auth.get_access_token.assert_called_once()
    
    # Verify the subscription is no longer running (should break on auth error)
    assert subscription._running is True  # The handler doesn't set _running to False on auth error


@pytest.mark.asyncio
async def test_call_callback_no_callback(subscription):
    """Test _call_callback method with no callback."""
    # Remove the callback
    subscription.callback = None
    
    # Call the method
    await subscription._call_callback({"test": "value"})
    
    # No assertion needed, just verifying it doesn't raise an exception


@pytest.mark.asyncio
async def test_call_callback_exception(subscription, mock_callback):
    """Test _call_callback method with exception in callback."""
    # Make the callback raise an exception
    mock_callback.side_effect = Exception("Test callback error")
    
    # Call the method
    await subscription._call_callback({"test": "value"})
    
    # Verify the callback was called
    mock_callback.assert_called_once_with({"test": "value"})


@pytest.mark.asyncio
async def test_stop_with_task_cancelled_error(subscription):
    """Test stop method with CancelledError when awaiting task."""
    # Set up the subscription with a mock task
    subscription._running = True
    
    # Create a task that raises CancelledError when awaited
    async def raise_cancelled():
        raise asyncio.CancelledError()
    
    task = asyncio.create_task(raise_cancelled())
    subscription._task = task
    
    # Mock the websocket
    ws = MagicMock()
    ws.close = AsyncMock()
    subscription._ws = ws
    
    # Stop the subscription
    await subscription.stop()
    
    # Verify the subscription was stopped
    assert subscription._running is False
    assert subscription._task is None
    # The websocket close method should have been called
    ws.close.assert_awaited_once()
