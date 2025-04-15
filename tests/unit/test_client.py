"""Tests for the client module."""
import unittest
from unittest.mock import MagicMock, patch

import httpx

from unraid_api.client import UnraidClient
from unraid_api.exceptions import (APIError, AuthenticationError,
                                   ConnectionError, GraphQLError)


class TestUnraidClient(unittest.TestCase):
    """Test the UnraidClient class."""

    def setUp(self):
        """Set up test fixtures."""
        self.host = "test-host"
        self.api_key = "test-api-key"
        self.port = 443
        self.use_ssl = True
        self.client = UnraidClient(
            host=self.host,
            api_key=self.api_key,
            port=self.port,
            use_ssl=self.use_ssl,
        )

    def test_init(self):
        """Test initialization of UnraidClient."""
        self.assertEqual(self.client.host, self.host)
        self.assertEqual(self.client.port, self.port)
        self.assertEqual(self.client.use_ssl, self.use_ssl)
        self.assertEqual(self.client.verify_ssl, False)
        self.assertEqual(self.client.api_key, self.api_key)
        self.assertEqual(self.client._base_url, "https://test-host:443/graphql")
        self.assertEqual(self.client._followed_url, None)
        self.assertEqual(self.client._headers["Content-Type"], "application/json")
        self.assertEqual(self.client._headers["x-api-key"], self.api_key)

    def test_set_api_key(self):
        """Test setting API key."""
        self.client.set_api_key("new-api-key")
        self.assertEqual(self.client.api_key, "new-api-key")
        self.assertEqual(self.client._headers["x-api-key"], "new-api-key")

    @patch("httpx.Client")
    def test_execute_query_success(self, mock_client):
        """Test successful query execution."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"data": {"test": "value"}}
        mock_client.return_value.__enter__.return_value.post.return_value = mock_response

        # Call the method
        result = self.client.execute_query("query { test }")

        # Verify the result
        self.assertEqual(result, {"test": "value"})

        # Verify the call to httpx.Client.post
        mock_client.return_value.__enter__.return_value.post.assert_called_once()
        args, kwargs = mock_client.return_value.__enter__.return_value.post.call_args
        self.assertEqual(args[0], "https://test-host:443/graphql")
        self.assertEqual(kwargs["json"]["query"], "query { test }")
        self.assertEqual(kwargs["json"]["variables"], {})
        self.assertEqual(kwargs["headers"], self.client._headers)

    @patch("httpx.Client")
    def test_execute_query_with_variables(self, mock_client):
        """Test query execution with variables."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"data": {"test": "value"}}
        mock_client.return_value.__enter__.return_value.post.return_value = mock_response

        # Call the method
        result = self.client.execute_query(
            "query($var: String!) { test(var: $var) }", {"var": "test-value"}
        )

        # Verify the result
        self.assertEqual(result, {"test": "value"})

        # Verify the call to httpx.Client.post
        mock_client.return_value.__enter__.return_value.post.assert_called_once()
        args, kwargs = mock_client.return_value.__enter__.return_value.post.call_args
        self.assertEqual(args[0], "https://test-host:443/graphql")
        self.assertEqual(kwargs["json"]["query"], "query($var: String!) { test(var: $var) }")
        self.assertEqual(kwargs["json"]["variables"], {"var": "test-value"})

    @patch("httpx.Client")
    def test_execute_query_graphql_error(self, mock_client):
        """Test query execution with GraphQL error."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "errors": [{"message": "GraphQL error"}]
        }
        mock_client.return_value.__enter__.return_value.post.return_value = mock_response

        # Call the method and verify it raises an exception
        with self.assertRaises(GraphQLError):
            self.client.execute_query("query { test }")

    @patch("httpx.Client")
    def test_execute_query_invalid_response(self, mock_client):
        """Test query execution with invalid response."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"not_data": {}}
        mock_client.return_value.__enter__.return_value.post.return_value = mock_response

        # Call the method and verify it raises an exception
        with self.assertRaises(APIError):
            self.client.execute_query("query { test }")

    @patch("httpx.Client")
    def test_execute_query_connection_error(self, mock_client):
        """Test query execution with connection error."""
        # Mock the response
        mock_client.return_value.__enter__.return_value.post.side_effect = httpx.RequestError("Connection error")

        # Call the method and verify it raises an exception
        with self.assertRaises(ConnectionError):
            self.client.execute_query("query { test }")

    @patch("httpx.Client")
    def test_execute_query_http_error(self, mock_client):
        """Test query execution with HTTP error."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_client.return_value.__enter__.return_value.post.side_effect = httpx.HTTPStatusError(
            "HTTP error", request=MagicMock(), response=mock_response
        )

        # Call the method and verify it raises an exception
        with self.assertRaises(AuthenticationError):
            self.client.execute_query("query { test }")

    @patch("httpx.Client")
    def test_execute_query_other_http_error(self, mock_client):
        """Test query execution with other HTTP error."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_client.return_value.__enter__.return_value.post.side_effect = httpx.HTTPStatusError(
            "HTTP error", request=MagicMock(), response=mock_response
        )

        # Call the method and verify it raises an exception
        with self.assertRaises(APIError):
            self.client.execute_query("query { test }")

    @patch("httpx.Client")
    def test_execute_query_unexpected_error(self, mock_client):
        """Test query execution with unexpected error."""
        # Mock the response
        mock_client.return_value.__enter__.return_value.post.side_effect = Exception("Unexpected error")

        # Call the method and verify it raises an exception
        with self.assertRaises(APIError):
            self.client.execute_query("query { test }")

    @patch.object(UnraidClient, "execute_query")
    def test_get_system_info(self, mock_execute_query):
        """Test get_system_info method."""
        # Mock the response with the expected structure
        mock_execute_query.return_value = {"info": {"os": {"platform": "linux"}, "cpu": {}, "memory": {}, "system": {}}}

        # Call the method
        result = self.client.get_system_info()

        # Verify the result
        self.assertEqual(result, {"os": {"platform": "linux"}, "cpu": {}, "memory": {}, "system": {}})

        # Verify the call to execute_query
        mock_execute_query.assert_called_once()


if __name__ == "__main__":
    unittest.main()
