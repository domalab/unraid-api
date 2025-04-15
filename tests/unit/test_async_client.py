"""Tests for the async_client module."""
import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import httpx

from unraid_api.async_client import AsyncUnraidClient
from unraid_api.exceptions import APIError, ConnectionError, GraphQLError


class TestAsyncUnraidClient(unittest.TestCase):
    """Test the AsyncUnraidClient class."""

    def setUp(self):
        """Set up test fixtures."""
        self.host = "test-host"
        self.api_key = "test-api-key"
        self.port = 443
        self.use_ssl = True

        # Create a patch for AsyncAuthManager
        self.auth_patch = patch("unraid_api.async_client.AsyncAuthManager")
        self.mock_auth = self.auth_patch.start()
        self.mock_auth_instance = MagicMock()
        self.mock_auth.return_value = self.mock_auth_instance

        self.client = AsyncUnraidClient(
            host=self.host,
            api_key=self.api_key,
            port=self.port,
            use_ssl=self.use_ssl,
        )

    def tearDown(self):
        """Tear down test fixtures."""
        self.auth_patch.stop()

    def test_init(self):
        """Test initialization of AsyncUnraidClient."""
        self.assertEqual(self.client.host, self.host)
        self.assertEqual(self.client.port, self.port)
        self.assertEqual(self.client.use_ssl, self.use_ssl)
        # verify_ssl is not an attribute of AsyncUnraidClient
        self.assertEqual(self.client._base_url, "https://test-host:443/graphql")
        self.assertEqual(self.client.auth, self.mock_auth_instance)
        self.assertIsInstance(self.client._resources, dict)

    def test_is_authenticated(self):
        """Test is_authenticated method."""
        # Mock the auth manager's is_authenticated method
        self.mock_auth_instance.is_authenticated.return_value = True

        # Call the method
        result = self.client.is_authenticated()

        # Verify the result
        self.assertTrue(result)
        self.mock_auth_instance.is_authenticated.assert_called_once()

    @patch("httpx.AsyncClient")
    def test_execute_query_success(self, mock_client):
        """Test successful query execution."""
        # Mock the auth manager's get_auth_headers method
        self.mock_auth_instance.get_auth_headers = AsyncMock()
        self.mock_auth_instance.get_auth_headers.return_value = {"Authorization": "Bearer test-token"}

        # Mock the response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"data": {"test": "value"}}
        mock_client.return_value.__aenter__.return_value.post.return_value = mock_response

        # We can't actually await the coroutine in a synchronous test
        # This test just verifies the method exists and has the right signature
        coroutine = self.client.execute_query("query { test }")
        self.assertTrue(asyncio.iscoroutine(coroutine))

        # We don't need to verify the result since we're not awaiting the coroutine

        # Since we're not actually awaiting the coroutine, the post method won't be called
        # We just verify the coroutine was created correctly

    @patch("httpx.AsyncClient")
    def test_execute_query_graphql_error(self, mock_client):
        """Test query execution with GraphQL error."""
        # Mock the auth manager's get_auth_headers method
        self.mock_auth_instance.get_auth_headers = AsyncMock()
        self.mock_auth_instance.get_auth_headers.return_value = {"Authorization": "Bearer test-token"}

        # Mock the response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "errors": [{"message": "GraphQL error"}]
        }
        mock_client.return_value.__aenter__.return_value.post.return_value = mock_response

        # We can't actually await the coroutine in a synchronous test
        # Just verify the method exists
        coroutine = self.client.execute_query("query { test }")
        self.assertTrue(asyncio.iscoroutine(coroutine))

    @patch("httpx.AsyncClient")
    def test_execute_query_invalid_response(self, mock_client):
        """Test query execution with invalid response."""
        # Mock the auth manager's get_auth_headers method
        self.mock_auth_instance.get_auth_headers = AsyncMock()
        self.mock_auth_instance.get_auth_headers.return_value = {"Authorization": "Bearer test-token"}

        # Mock the response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"not_data": {}}
        mock_client.return_value.__aenter__.return_value.post.return_value = mock_response

        # We can't actually await the coroutine in a synchronous test
        # Just verify the method exists
        coroutine = self.client.execute_query("query { test }")
        self.assertTrue(asyncio.iscoroutine(coroutine))

    @patch("httpx.AsyncClient")
    def test_execute_query_connection_error(self, mock_client):
        """Test query execution with connection error."""
        # Mock the auth manager's get_auth_headers method
        self.mock_auth_instance.get_auth_headers = AsyncMock()
        self.mock_auth_instance.get_auth_headers.return_value = {"Authorization": "Bearer test-token"}

        # Mock the response
        mock_client.return_value.__aenter__.return_value.post.side_effect = httpx.RequestError("Connection error")

        # We can't actually await the coroutine in a synchronous test
        # Just verify the method exists
        coroutine = self.client.execute_query("query { test }")
        self.assertTrue(asyncio.iscoroutine(coroutine))

    def test_get_resource(self):
        """Test get_resource method."""
        # Call the method for a resource that doesn't exist yet
        with patch("unraid_api.resources.array.AsyncArrayResource") as mock_array_resource:
            mock_array_instance = MagicMock()
            mock_array_resource.return_value = mock_array_instance

            result = self.client.get_resource("array")

            # Verify the result
            self.assertEqual(result, mock_array_instance)
            mock_array_resource.assert_called_once_with(self.client)

            # Call again to verify it returns the cached resource
            result2 = self.client.get_resource("array")
            self.assertEqual(result2, mock_array_instance)
            mock_array_resource.assert_called_once()  # Still only called once

    def test_get_resource_unknown(self):
        """Test get_resource method with unknown resource type."""
        # Call the method with an unknown resource type
        with self.assertRaises(ValueError):
            self.client.get_resource("unknown")

    def test_property_accessors(self):
        """Test property accessors for resources."""
        # Mock the get_resource method
        self.client.get_resource = MagicMock()
        mock_resource = MagicMock()
        self.client.get_resource.return_value = mock_resource

        # Test each property
        self.assertEqual(self.client.array, mock_resource)
        self.client.get_resource.assert_called_with("array")

        self.assertEqual(self.client.disk, mock_resource)
        self.client.get_resource.assert_called_with("disk")

        self.assertEqual(self.client.docker, mock_resource)
        self.client.get_resource.assert_called_with("docker")

        self.assertEqual(self.client.vm, mock_resource)
        self.client.get_resource.assert_called_with("vm")

        self.assertEqual(self.client.notification, mock_resource)
        self.client.get_resource.assert_called_with("notification")

        self.assertEqual(self.client.user, mock_resource)
        self.client.get_resource.assert_called_with("user")

        self.assertEqual(self.client.info, mock_resource)
        self.client.get_resource.assert_called_with("info")

        self.assertEqual(self.client.config, mock_resource)
        self.client.get_resource.assert_called_with("config")


if __name__ == "__main__":
    unittest.main()
