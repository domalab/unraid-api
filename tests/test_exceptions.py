"""Tests for the exceptions module."""
import pytest

from unraid_api.exceptions import (
    APIError,
    AuthenticationError,
    ConnectionError,
    GraphQLError,
    OperationError,
    SubscriptionError,
    TokenExpiredError,
    UnraidAPIError,
)


def test_unraid_api_error():
    """Test UnraidAPIError exception."""
    error = UnraidAPIError("Test error")
    assert str(error) == "Test error"
    assert isinstance(error, Exception)


def test_api_error():
    """Test APIError exception."""
    error = APIError("Test error")
    assert str(error) == "Test error"
    assert isinstance(error, UnraidAPIError)


def test_authentication_error():
    """Test AuthenticationError exception."""
    error = AuthenticationError("Test error")
    assert str(error) == "Test error"
    assert isinstance(error, UnraidAPIError)


def test_connection_error():
    """Test ConnectionError exception."""
    error = ConnectionError("Test error")
    assert str(error) == "Test error"
    assert isinstance(error, UnraidAPIError)


def test_graphql_error():
    """Test GraphQLError exception."""
    error = GraphQLError("Test error", [{"message": "Error 1"}, {"message": "Error 2"}])
    assert str(error) == "Test error"
    assert error.errors == [{"message": "Error 1"}, {"message": "Error 2"}]
    assert isinstance(error, UnraidAPIError)


def test_operation_error():
    """Test OperationError exception."""
    error = OperationError("Test error")
    assert str(error) == "Test error"
    assert isinstance(error, UnraidAPIError)


def test_subscription_error():
    """Test SubscriptionError exception."""
    error = SubscriptionError("Test error")
    assert str(error) == "Test error"
    assert isinstance(error, UnraidAPIError)


def test_token_expired_error():
    """Test TokenExpiredError exception."""
    error = TokenExpiredError("Test error")
    assert str(error) == "Test error"
    assert isinstance(error, AuthenticationError)
