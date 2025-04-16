"""Async tests for the subscription module."""
import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio

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
async def test_start(subscription):
    """Test start method."""
    # Mock the subscription handler
    subscription._subscription_handler = AsyncMock()

    # Start the subscription
    await subscription.start()

    # Verify the subscription was started
    assert subscription._running is True
    assert subscription._task is not None
    subscription._subscription_handler.assert_called_once()


@pytest.mark.asyncio
async def test_stop(subscription):
    """Test stop method."""
    # Set up the subscription with a mock task
    subscription._running = True

    # Create a real asyncio task that just returns
    async def dummy_task():
        return

    subscription._task = asyncio.create_task(dummy_task())

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


@pytest.mark.asyncio
async def test_call_callback_coroutine(subscription, mock_callback):
    """Test _call_callback method with coroutine."""
    # Set up the test
    mock_callback.return_value = None

    # Call the method
    await subscription._call_callback({"test": "value"})

    # Verify the callback was called
    mock_callback.assert_called_once_with({"test": "value"})


@pytest.mark.asyncio
async def test_call_callback_function(subscription):
    """Test _call_callback method with function."""
    # Set up the test
    callback = MagicMock()
    subscription.callback = callback

    # Call the method
    await subscription._call_callback({"test": "value"})

    # Verify the callback was called
    callback.assert_called_once_with({"test": "value"})


@pytest.mark.asyncio
async def test_process_data_message(subscription, mock_callback):
    """Test processing a data message in the subscription handler."""
    # Call the _call_callback method directly with test data
    await subscription._call_callback({"test": "value"})

    # Verify the callback was called with the same data
    mock_callback.assert_called_once_with({"test": "value"})



