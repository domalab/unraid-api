"""Tests for the SubscriptionManager class."""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio

from unraid_api.subscription import SubscriptionManager


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
async def subscription_manager(mock_client):
    """Return a test SubscriptionManager instance."""
    return SubscriptionManager(mock_client)


@pytest.mark.asyncio
async def test_subscribe(subscription_manager):
    """Test subscribe method."""
    # Mock the Subscription class
    with patch("unraid_api.subscription.Subscription") as mock_subscription_class:
        mock_subscription = MagicMock()
        mock_subscription.start = AsyncMock()
        mock_subscription_class.return_value = mock_subscription

        # Call the method
        await subscription_manager.subscribe(
            name="test",
            subscription_query="subscription { test }",
            variables={"var": "value"},
            callback=lambda x: x
        )

        # Verify the subscription was created and started
        mock_subscription_class.assert_called_once()
        call_args = mock_subscription_class.call_args
        assert call_args[0][0] == subscription_manager.client
        assert call_args[0][1] == "subscription { test }"
        assert call_args[0][2] == {"var": "value"}
        # We can't directly compare the lambda functions
        mock_subscription.start.assert_awaited_once()
        assert subscription_manager.subscriptions["test"] == mock_subscription


@pytest.mark.asyncio
async def test_subscribe_duplicate(subscription_manager):
    """Test subscribe method with duplicate name."""
    # Add a subscription with the same name
    subscription_manager.subscriptions["test"] = MagicMock()

    # Call the method and verify it raises an exception
    with pytest.raises(ValueError, match="Subscription 'test' already exists"):
        await subscription_manager.subscribe(
            name="test",
            subscription_query="subscription { test }"
        )


@pytest.mark.asyncio
async def test_unsubscribe(subscription_manager):
    """Test unsubscribe method."""
    # Add a subscription
    mock_subscription = MagicMock()
    mock_subscription.stop = AsyncMock()
    subscription_manager.subscriptions["test"] = mock_subscription

    # Call the method
    await subscription_manager.unsubscribe("test")

    # Verify the subscription was stopped and removed
    mock_subscription.stop.assert_awaited_once()
    assert "test" not in subscription_manager.subscriptions


@pytest.mark.asyncio
async def test_unsubscribe_not_found(subscription_manager):
    """Test unsubscribe method with non-existent subscription."""
    # Call the method and verify it raises an exception
    with pytest.raises(ValueError, match="Subscription 'test' does not exist"):
        await subscription_manager.unsubscribe("test")


@pytest.mark.asyncio
async def test_stop_all(subscription_manager):
    """Test stop_all method."""
    # Add some subscriptions
    mock_subscription1 = MagicMock()
    mock_subscription1.stop = AsyncMock()
    mock_subscription2 = MagicMock()
    mock_subscription2.stop = AsyncMock()
    subscription_manager.subscriptions["test1"] = mock_subscription1
    subscription_manager.subscriptions["test2"] = mock_subscription2

    # Call the method
    await subscription_manager.stop_all()

    # Verify all subscriptions were stopped and removed
    mock_subscription1.stop.assert_awaited_once()
    mock_subscription2.stop.assert_awaited_once()
    assert len(subscription_manager.subscriptions) == 0


def test_get_subscription(subscription_manager):
    """Test get_subscription method."""
    # Add a subscription
    mock_subscription = MagicMock()
    subscription_manager.subscriptions["test"] = mock_subscription

    # Call the method
    result = subscription_manager.get_subscription("test")

    # Verify the result
    assert result == mock_subscription


def test_get_subscription_not_found(subscription_manager):
    """Test get_subscription method with non-existent subscription."""
    # Call the method and verify it raises an exception
    with pytest.raises(ValueError, match="Subscription 'test' does not exist"):
        subscription_manager.get_subscription("test")
