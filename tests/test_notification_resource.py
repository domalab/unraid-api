"""Tests for the notification resource."""
import pytest
from unittest.mock import MagicMock, AsyncMock, patch

from unraid_api.resources.notification import NotificationResource, AsyncNotificationResource
from unraid_api.exceptions import APIError, OperationError


class TestNotificationResource:
    """Tests for the NotificationResource class."""

    def setup_method(self):
        """Set up the test."""
        self.client = MagicMock()
        self.resource = NotificationResource(self.client)

    def test_init(self):
        """Test initialization."""
        assert self.resource.client == self.client

    def test_get_notifications(self):
        """Test get_notifications method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "notifications": {
                "overview": {
                    "unread": {
                        "info": 1,
                        "warning": 2,
                        "alert": 0,
                        "total": 3
                    }
                }
            }
        }

        # Call the method
        result = self.resource.get_notifications()

        # Verify the result
        assert result == self.client.execute_query.return_value["notifications"]
        self.client.execute_query.assert_called_once_with(
            """
        query GetNotifications {
            notifications {
                overview {
                    unread {
                        info
                        warning
                        alert
                        total
                    }
                }
            }
        }
        """
        )

    def test_get_notifications_error(self):
        """Test get_notifications method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing notifications field"):
            self.resource.get_notifications()

        self.client.execute_query.assert_called_once()

    def test_get_notification(self):
        """Test get_notification method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "notification": {
                "id": "notification1",
                "type": "info",
                "importance": "normal",
                "subject": "Test Subject",
                "description": "Test Description",
                "timestamp": "2023-01-01T00:00:00Z",
                "read": False
            }
        }

        # Call the method
        result = self.resource.get_notification("notification1")

        # Verify the result
        assert result == self.client.execute_query.return_value["notification"]
        self.client.execute_query.assert_called_once_with(
            """
        query GetNotification($id: String!) {
            notification(id: $id) {
                id
                type
                importance
                subject
                description
                timestamp
                read
            }
        }
        """,
            {"id": "notification1"}
        )

    def test_get_notification_error(self):
        """Test get_notification method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing notification field"):
            self.resource.get_notification("notification1")

        self.client.execute_query.assert_called_once()

    def test_mark_notification_read(self):
        """Test mark_notification_read method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "markNotificationRead": {
                "success": True,
                "message": "Notification marked as read"
            }
        }

        # Call the method
        result = self.resource.mark_notification_read("notification1")

        # Verify the result
        assert result == self.client.execute_query.return_value["markNotificationRead"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation MarkNotificationRead($id: String!) {
            markNotificationRead(id: $id) {
                success
                message
            }
        }
        """,
            {"id": "notification1"}
        )

    def test_mark_notification_read_error(self):
        """Test mark_notification_read method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "markNotificationRead": {
                "success": False,
                "message": "Notification not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to mark notification as read: Notification not found"):
            self.resource.mark_notification_read("notification1")

        self.client.execute_query.assert_called_once()

    def test_mark_all_notifications_read(self):
        """Test mark_all_notifications_read method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "markAllNotificationsRead": {
                "success": True,
                "message": "All notifications marked as read"
            }
        }

        # Call the method
        result = self.resource.mark_all_notifications_read()

        # Verify the result
        assert result == self.client.execute_query.return_value["markAllNotificationsRead"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation MarkAllNotificationsRead {
            markAllNotificationsRead {
                success
                message
            }
        }
        """
        )

    def test_mark_all_notifications_read_error(self):
        """Test mark_all_notifications_read method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "markAllNotificationsRead": {
                "success": False,
                "message": "No notifications to mark as read"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to mark all notifications as read: No notifications to mark as read"):
            self.resource.mark_all_notifications_read()

        self.client.execute_query.assert_called_once()

    def test_dismiss_notification(self):
        """Test dismiss_notification method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "dismissNotification": {
                "success": True,
                "message": "Notification dismissed"
            }
        }

        # Call the method
        result = self.resource.dismiss_notification("notification1")

        # Verify the result
        assert result == self.client.execute_query.return_value["dismissNotification"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation DismissNotification($id: String!) {
            dismissNotification(id: $id) {
                success
                message
            }
        }
        """,
            {"id": "notification1"}
        )

    def test_dismiss_notification_error(self):
        """Test dismiss_notification method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "dismissNotification": {
                "success": False,
                "message": "Notification not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to dismiss notification: Notification not found"):
            self.resource.dismiss_notification("notification1")

        self.client.execute_query.assert_called_once()

    def test_dismiss_all_notifications(self):
        """Test dismiss_all_notifications method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "dismissAllNotifications": {
                "success": True,
                "message": "All notifications dismissed"
            }
        }

        # Call the method
        result = self.resource.dismiss_all_notifications()

        # Verify the result
        assert result == self.client.execute_query.return_value["dismissAllNotifications"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation DismissAllNotifications {
            dismissAllNotifications {
                success
                message
            }
        }
        """
        )

    def test_dismiss_all_notifications_error(self):
        """Test dismiss_all_notifications method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "dismissAllNotifications": {
                "success": False,
                "message": "No notifications to dismiss"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to dismiss all notifications: No notifications to dismiss"):
            self.resource.dismiss_all_notifications()

        self.client.execute_query.assert_called_once()

    def test_subscribe_to_notifications(self):
        """Test subscribe_to_notifications method."""
        # Mock the callback function
        callback = MagicMock()

        # Call the method
        self.resource.subscribe_to_notifications(callback)

        # Verify the client's subscribe method was called
        self.client.subscribe.assert_called_once_with(
            """
        subscription OnNotification {
            notification {
                id
                type
                importance
                subject
                description
                timestamp
                read
            }
        }
        """,
            callback
        )


@pytest.mark.asyncio
class TestAsyncNotificationResource:
    """Tests for the AsyncNotificationResource class."""

    def setup_method(self):
        """Set up the test."""
        self.client = MagicMock()
        # Make execute_query a coroutine
        self.client.execute_query = AsyncMock()
        self.client.subscribe = AsyncMock()
        self.resource = AsyncNotificationResource(self.client)

    async def test_init(self):
        """Test initialization."""
        assert self.resource.client == self.client

    async def test_get_notifications(self):
        """Test get_notifications method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "notifications": [
                {
                    "id": "notification1",
                    "type": "info",
                    "importance": "normal",
                    "subject": "Test Subject",
                    "description": "Test Description",
                    "timestamp": "2023-01-01T00:00:00Z",
                    "read": False
                }
            ]
        }

        # Call the method
        result = await self.resource.get_notifications()

        # Verify the result
        assert result == self.client.execute_query.return_value["notifications"]
        self.client.execute_query.assert_called_once()

    async def test_get_notifications_error(self):
        """Test get_notifications method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing notifications field"):
            await self.resource.get_notifications()

        self.client.execute_query.assert_called_once()

    async def test_get_notification(self):
        """Test get_notification method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "notification": {
                "id": "notification1",
                "type": "info",
                "importance": "normal",
                "subject": "Test Subject",
                "description": "Test Description",
                "timestamp": "2023-01-01T00:00:00Z",
                "read": False
            }
        }

        # Call the method
        result = await self.resource.get_notification("notification1")

        # Verify the result
        assert result == self.client.execute_query.return_value["notification"]
        self.client.execute_query.assert_called_once()

    async def test_get_notification_error(self):
        """Test get_notification method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing notification field"):
            await self.resource.get_notification("notification1")

        self.client.execute_query.assert_called_once()

    async def test_mark_notification_read(self):
        """Test mark_notification_read method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "markNotificationRead": {
                "success": True,
                "message": "Notification marked as read"
            }
        }

        # Call the method
        result = await self.resource.mark_notification_read("notification1")

        # Verify the result
        assert result == self.client.execute_query.return_value["markNotificationRead"]
        self.client.execute_query.assert_called_once()

    async def test_mark_notification_read_error(self):
        """Test mark_notification_read method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "markNotificationRead": {
                "success": False,
                "message": "Notification not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to mark notification as read: Notification not found"):
            await self.resource.mark_notification_read("notification1")

        self.client.execute_query.assert_called_once()

    async def test_mark_all_notifications_read(self):
        """Test mark_all_notifications_read method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "markAllNotificationsRead": {
                "success": True,
                "message": "All notifications marked as read"
            }
        }

        # Call the method
        result = await self.resource.mark_all_notifications_read()

        # Verify the result
        assert result == self.client.execute_query.return_value["markAllNotificationsRead"]
        self.client.execute_query.assert_called_once()

    async def test_mark_all_notifications_read_error(self):
        """Test mark_all_notifications_read method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "markAllNotificationsRead": {
                "success": False,
                "message": "No notifications to mark as read"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to mark all notifications as read: No notifications to mark as read"):
            await self.resource.mark_all_notifications_read()

        self.client.execute_query.assert_called_once()

    async def test_dismiss_notification(self):
        """Test dismiss_notification method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "dismissNotification": {
                "success": True,
                "message": "Notification dismissed"
            }
        }

        # Call the method
        result = await self.resource.dismiss_notification("notification1")

        # Verify the result
        assert result == self.client.execute_query.return_value["dismissNotification"]
        self.client.execute_query.assert_called_once()

    async def test_dismiss_notification_error(self):
        """Test dismiss_notification method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "dismissNotification": {
                "success": False,
                "message": "Notification not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to dismiss notification: Notification not found"):
            await self.resource.dismiss_notification("notification1")

        self.client.execute_query.assert_called_once()

    async def test_dismiss_all_notifications(self):
        """Test dismiss_all_notifications method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "dismissAllNotifications": {
                "success": True,
                "message": "All notifications dismissed"
            }
        }

        # Call the method
        result = await self.resource.dismiss_all_notifications()

        # Verify the result
        assert result == self.client.execute_query.return_value["dismissAllNotifications"]
        self.client.execute_query.assert_called_once()

    async def test_dismiss_all_notifications_error(self):
        """Test dismiss_all_notifications method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "dismissAllNotifications": {
                "success": False,
                "message": "No notifications to dismiss"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to dismiss all notifications: No notifications to dismiss"):
            await self.resource.dismiss_all_notifications()

        self.client.execute_query.assert_called_once()

    async def test_subscribe_to_notifications(self):
        """Test subscribe_to_notifications method."""
        # Mock the callback function
        callback = AsyncMock()

        # Call the method
        await self.resource.subscribe_to_notifications(callback)

        # Verify the client's subscribe method was called
        self.client.subscribe.assert_called_once_with(
            """
        subscription OnNotification {
            notification {
                id
                type
                importance
                subject
                description
                timestamp
                read
            }
        }
        """,
            callback
        )
