"""Additional tests for the subscription module to improve coverage."""
import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK

from unraid_api.exceptions import AuthenticationError, ConnectionError
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

    # Mock websockets.connect
    mock_ws = AsyncMock()
    mock_ws.send = AsyncMock()
    mock_ws.recv = AsyncMock()
    mock_ws.recv.side_effect = [
        json.dumps({"type": "connection_ack"}),
        json.dumps({"type": "data", "payload": {"data": {"test": "value"}}}),
        json.dumps({"type": "complete"})
    ]

    with patch("websockets.connect", AsyncMock(return_value=mock_ws)):
        # Start the subscription
        subscription._running = True

        # Run the handler for a short time
        task = asyncio.create_task(subscription._subscription_handler())
        await asyncio.sleep(0.1)

        # Stop the subscription
        subscription._running = False
        await task

        # Verify the token was retrieved from the sync client
        sync_client.auth.get_access_token.assert_called_once()


@pytest.mark.asyncio
async def test_subscription_handler_connection_closed_ok(subscription):
    """Test _subscription_handler method with ConnectionClosedOK exception."""
    # Mock websockets.connect
    mock_ws = AsyncMock()
    mock_ws.send = AsyncMock()
    mock_ws.recv = AsyncMock()
    mock_ws.recv.side_effect = [
        json.dumps({"type": "connection_ack"}),
        json.dumps({"type": "start"}),
        ConnectionClosedOK(code=1000, reason="")
    ]

    with patch("websockets.connect", AsyncMock(return_value=mock_ws)):
        # Start the subscription
        subscription._running = True

        # Run the handler for a short time
        task = asyncio.create_task(subscription._subscription_handler())
        await asyncio.sleep(0.1)

        # Stop the subscription
        subscription._running = False
        await task

        # Verify the connection was established
        assert mock_ws.send.call_count == 2  # init message and subscription message


@pytest.mark.asyncio
async def test_subscription_handler_connection_closed_error(subscription):
    """Test _subscription_handler method with ConnectionClosedError exception."""
    # Mock websockets.connect
    mock_ws = AsyncMock()
    mock_ws.send = AsyncMock()
    mock_ws.recv = AsyncMock()
    mock_ws.recv.side_effect = [
        json.dumps({"type": "connection_ack"}),
        json.dumps({"type": "start"}),
        ConnectionClosedError(code=1006, reason="")
    ]

    with patch("websockets.connect", AsyncMock(return_value=mock_ws)):
        # Start the subscription
        subscription._running = True

        # Run the handler for a short time
        task = asyncio.create_task(subscription._subscription_handler())
        await asyncio.sleep(0.1)

        # Stop the subscription
        subscription._running = False
        await task

        # Verify the connection was established and messages were sent
        # We expect 2 calls: init message and subscription message
        assert mock_ws.send.call_count >= 2


@pytest.mark.asyncio
async def test_subscription_handler_authentication_error(subscription):
    """Test _subscription_handler method with AuthenticationError exception."""
    # Mock the client's get_access_token to raise AuthenticationError
    subscription.client.auth.get_access_token.side_effect = AuthenticationError("Test auth error")

    # Start the subscription
    subscription._running = True

    # Run the handler for a short time
    task = asyncio.create_task(subscription._subscription_handler())
    await asyncio.sleep(0.1)

    # Stop the subscription
    subscription._running = False
    await task

    # Verify the token was attempted to be retrieved
    subscription.client.auth.get_access_token.assert_called_once()


@pytest.mark.asyncio
async def test_subscription_handler_connection_error(subscription):
    """Test _subscription_handler method with ConnectionError exception."""
    # Reset the mock to clear any previous calls
    subscription.client.auth.get_access_token.reset_mock()

    # Mock websockets.connect to raise ConnectionError
    with patch("websockets.connect", AsyncMock(side_effect=ConnectionError("Test connection error"))):
        # Mock asyncio.sleep to avoid waiting
        with patch("asyncio.sleep", AsyncMock()):
            # Start the subscription
            subscription._running = True

            # Run the handler
            await subscription._subscription_handler()

            # Verify the token was retrieved
            assert subscription.client.auth.get_access_token.called


@pytest.mark.asyncio
async def test_subscription_handler_general_exception(subscription):
    """Test _subscription_handler method with general exception."""
    # Reset the mock to clear any previous calls
    subscription.client.auth.get_access_token.reset_mock()

    # Mock websockets.connect to raise a general exception
    with patch("websockets.connect", AsyncMock(side_effect=Exception("Test general error"))):
        # Mock asyncio.sleep to avoid waiting
        with patch("asyncio.sleep", AsyncMock()):
            # Start the subscription
            subscription._running = True

            # Run the handler
            await subscription._subscription_handler()

            # Verify the token was retrieved
            assert subscription.client.auth.get_access_token.called


@pytest.mark.asyncio
async def test_subscription_handler_invalid_ack(subscription):
    """Test _subscription_handler method with invalid acknowledgement."""
    # Mock websockets.connect
    mock_ws = AsyncMock()
    mock_ws.send = AsyncMock()
    mock_ws.recv = AsyncMock()
    mock_ws.recv.side_effect = [
        json.dumps({"type": "invalid_ack"})  # Invalid acknowledgement
    ]

    with patch("websockets.connect", AsyncMock(return_value=mock_ws)):
        # Mock asyncio.sleep to avoid waiting
        with patch("asyncio.sleep", AsyncMock()):
            # Start the subscription
            subscription._running = True

            # Set up a flag to stop the subscription after a short time
            async def stop_after_delay():
                await asyncio.sleep(0.1)
                subscription._running = False

            # Run both tasks
            stop_task = asyncio.create_task(stop_after_delay())
            handler_task = asyncio.create_task(subscription._subscription_handler())

            # Wait for both tasks to complete
            await asyncio.gather(stop_task, handler_task)

            # Verify the init message was sent
            assert mock_ws.send.called


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
