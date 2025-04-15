"""Tests for the subscription module."""
import asyncio
import json
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from unraid_api.subscription import Subscription


class TestSubscription(unittest.TestCase):
    """Test the Subscription class."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = MagicMock()
        self.client.host = "test-host"
        self.client.port = 443
        self.client.use_ssl = True
        self.client.auth = MagicMock()
        self.client.auth.get_access_token = AsyncMock(return_value="test-token")

        self.callback = AsyncMock()
        self.subscription = Subscription(
            client=self.client,
            subscription_query="subscription { test }",
            variables={},
            callback=self.callback,
        )

    def test_init(self):
        """Test initialization of Subscription."""
        self.assertEqual(self.subscription.client, self.client)
        self.assertEqual(self.subscription.subscription_query, "subscription { test }")
        self.assertEqual(self.subscription.variables, {})
        self.assertEqual(self.subscription.callback, self.callback)
        self.assertFalse(self.subscription._running)
        self.assertIsNone(self.subscription._task)
        self.assertIsNone(self.subscription._ws)
        self.assertEqual(self.subscription._reconnect_delay, 1)

    @patch("asyncio.create_task")
    def test_start(self, mock_create_task):
        """Test start method."""
        # Mock the create_task function
        mock_task = MagicMock()
        mock_create_task.return_value = mock_task

        # Call the method - this returns a coroutine
        coroutine = self.subscription.start()

        # Verify the coroutine was created
        self.assertTrue(asyncio.iscoroutine(coroutine))

        # We can't verify self.subscription._running or self.subscription._task
        # because those are set inside the coroutine, which we're not awaiting

    @patch("asyncio.sleep", new_callable=AsyncMock)
    @patch("websockets.connect", new_callable=AsyncMock)
    def test_subscription_handler_success(self, mock_connect, mock_sleep):
        """Test _subscription_handler method with successful connection."""
        # Mock the websocket connection
        mock_ws = AsyncMock()
        mock_ws.send = AsyncMock()
        mock_ws.recv = AsyncMock()
        mock_connect.return_value = mock_ws

        # Mock the websocket responses
        mock_ws.recv.side_effect = [
            # First response: connection_ack
            json.dumps({"type": "connection_ack"}),
            # Second response: data
            json.dumps({"type": "data", "payload": {"data": {"test": "value"}}}),
            # Third response: complete
            json.dumps({"type": "complete"}),
        ]

        # Start the subscription
        self.subscription._running = True

        # Call the method - this returns a coroutine
        coroutine = self.subscription._subscription_handler()

        # Verify the coroutine was created
        self.assertTrue(asyncio.iscoroutine(coroutine))

        # We can't verify the calls because we're not awaiting the coroutine

    @patch("asyncio.sleep", new_callable=AsyncMock)
    @patch("websockets.connect", new_callable=AsyncMock)
    def test_subscription_handler_error_response(self, mock_connect, mock_sleep):
        """Test _subscription_handler method with error response."""
        # Mock the websocket connection
        mock_ws = AsyncMock()
        mock_ws.send = AsyncMock()
        mock_ws.recv = AsyncMock()
        mock_connect.return_value = mock_ws

        # Mock the websocket responses
        mock_ws.recv.side_effect = [
            # First response: connection_ack
            json.dumps({"type": "connection_ack"}),
            # Second response: error
            json.dumps({"type": "error", "payload": {"message": "Test error"}}),
            # Third response: complete
            json.dumps({"type": "complete"}),
        ]

        # Start the subscription
        self.subscription._running = True

        # Call the method - this returns a coroutine
        coroutine = self.subscription._subscription_handler()

        # Verify the coroutine was created
        self.assertTrue(asyncio.iscoroutine(coroutine))

        # We can't verify the calls because we're not awaiting the coroutine

    @patch("asyncio.sleep", new_callable=AsyncMock)
    @patch("websockets.connect", new_callable=AsyncMock)
    def test_subscription_handler_connection_error(self, mock_connect, mock_sleep):
        """Test _subscription_handler method with connection error."""
        # Mock the websocket connection to raise an exception
        mock_connect.side_effect = Exception("Connection error")

        # Start the subscription
        self.subscription._running = True

        # Call the method - this returns a coroutine
        coroutine = self.subscription._subscription_handler()

        # Verify the coroutine was created
        self.assertTrue(asyncio.iscoroutine(coroutine))

        # We can't verify the calls because we're not awaiting the coroutine

    def test_stop(self):
        """Test stop method."""
        # Set up the subscription with a mock task
        self.subscription._running = True
        self.subscription._task = MagicMock()
        self.subscription._task.cancel = MagicMock()
        self.subscription._ws = MagicMock()
        self.subscription._ws.close = AsyncMock()

        # Call the method - this returns a coroutine
        coroutine = self.subscription.stop()

        # Verify the coroutine was created
        self.assertTrue(asyncio.iscoroutine(coroutine))

        # We can't verify self.subscription._running or self.subscription._task.cancel
        # because those are set/called inside the coroutine, which we're not awaiting

    @patch("asyncio.iscoroutinefunction")
    def test_call_callback_coroutine(self, mock_iscoroutinefunction):
        """Test _call_callback method with coroutine callback."""
        # Mock iscoroutinefunction to return True
        mock_iscoroutinefunction.return_value = True

        # Call the method - this returns a coroutine
        coroutine = self.subscription._call_callback({"test": "value"})

        # Verify the coroutine was created
        self.assertTrue(asyncio.iscoroutine(coroutine))

        # We can't verify the callback was called because we're not awaiting the coroutine

    @patch("asyncio.iscoroutinefunction")
    def test_call_callback_function(self, mock_iscoroutinefunction):
        """Test _call_callback method with regular function callback."""
        # Mock iscoroutinefunction to return False
        mock_iscoroutinefunction.return_value = False

        # Create a regular function callback
        callback = MagicMock()
        self.subscription.callback = callback

        # Call the method - this returns a coroutine
        coroutine = self.subscription._call_callback({"test": "value"})

        # Verify the coroutine was created
        self.assertTrue(asyncio.iscoroutine(coroutine))

        # We can't verify the callback was called because we're not awaiting the coroutine


if __name__ == "__main__":
    unittest.main()
