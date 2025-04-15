"""Tests for the exceptions module."""
import unittest

from unraid_api.exceptions import (APIError, AuthenticationError,
                                   ConnectionError, GraphQLError,
                                   OperationError, SubscriptionError,
                                   TokenExpiredError, UnraidAPIError)


class TestExceptions(unittest.TestCase):
    """Test the exceptions module."""

    def test_unraid_api_error(self):
        """Test UnraidAPIError exception."""
        error = UnraidAPIError("Test error")
        self.assertEqual(str(error), "Test error")
        self.assertIsInstance(error, Exception)

    def test_api_error(self):
        """Test APIError exception."""
        error = APIError("Test error")
        self.assertEqual(str(error), "Test error")
        self.assertIsInstance(error, UnraidAPIError)

    def test_authentication_error(self):
        """Test AuthenticationError exception."""
        error = AuthenticationError("Test error")
        self.assertEqual(str(error), "Test error")
        self.assertIsInstance(error, UnraidAPIError)

    def test_connection_error(self):
        """Test ConnectionError exception."""
        error = ConnectionError("Test error")
        self.assertEqual(str(error), "Test error")
        self.assertIsInstance(error, UnraidAPIError)

    def test_graphql_error(self):
        """Test GraphQLError exception."""
        error = GraphQLError("Test error", [{"message": "Error 1"}, {"message": "Error 2"}])
        self.assertEqual(str(error), "Test error")
        self.assertEqual(error.errors, [{"message": "Error 1"}, {"message": "Error 2"}])
        self.assertIsInstance(error, UnraidAPIError)

    def test_operation_error(self):
        """Test OperationError exception."""
        error = OperationError("Test error")
        self.assertEqual(str(error), "Test error")
        self.assertIsInstance(error, UnraidAPIError)

    def test_subscription_error(self):
        """Test SubscriptionError exception."""
        error = SubscriptionError("Test error")
        self.assertEqual(str(error), "Test error")
        self.assertIsInstance(error, UnraidAPIError)

    def test_token_expired_error(self):
        """Test TokenExpiredError exception."""
        error = TokenExpiredError("Test error")
        self.assertEqual(str(error), "Test error")
        self.assertIsInstance(error, AuthenticationError)


if __name__ == "__main__":
    unittest.main()
