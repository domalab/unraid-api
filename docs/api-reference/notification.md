---
title: Notification API
description: Notification management with the Unraid API
---

# Notification API

The Notification API allows you to manage and interact with notifications on your Unraid server. This includes retrieving, creating, and archiving notifications.

## Available Methods

### get_notifications

Retrieves a list of all notifications on the Unraid server.

```python
def get_notifications(include_archived: bool = False) -> List[NotificationModel]
```

**Parameters**:

- `include_archived` (bool, optional): Whether to include archived notifications. Default is `False`.

**Returns**:
A list of `NotificationModel` objects representing each notification.

**Example**:

```python
# Synchronous client
from unraid_api import UnraidClient

client = UnraidClient("192.168.1.10", api_key="your-api-key")
notifications = client.notification.get_notifications()

for notification in notifications:
    print(f"Notification: {notification.title}, Importance: {notification.importance}")

# Include archived notifications
all_notifications = client.notification.get_notifications(include_archived=True)
```

```python
# Asynchronous client
import asyncio
from unraid_api import AsyncUnraidClient

async def main():
    client = AsyncUnraidClient("192.168.1.10", api_key="your-api-key")
    notifications = await client.notification.get_notifications()
    
    for notification in notifications:
        print(f"Notification: {notification.title}, Importance: {notification.importance}")

asyncio.run(main())
```

### get_notification

Retrieves a specific notification by ID.

```python
def get_notification(notification_id: str) -> NotificationModel
```

**Parameters**:

- `notification_id` (str): The ID of the notification to retrieve.

**Returns**:
A `NotificationModel` object representing the specified notification.

**Raises**:

- `APIError`: If the notification does not exist or cannot be accessed.

**Example**:

```python
# Get a specific notification
notification = client.notification.get_notification(notification_id="abc123")
print(f"Notification: {notification.title}")
print(f"Message: {notification.message}")
```

### create_notification

Creates a new notification on the Unraid server.

```python
def create_notification(
    title: str,
    message: str,
    importance: str = "normal",
    icon: str = None,
    action_url: str = None
) -> NotificationModel
```

**Parameters**:

- `title` (str): The title of the notification.
- `message` (str): The message content of the notification.
- `importance` (str, optional): The importance level ("low", "normal", "high", "alert"). Default is "normal".
- `icon` (str, optional): The icon to display with the notification. If `None`, a default icon is used.
- `action_url` (str, optional): A URL to open when the notification is clicked. If `None`, no action is taken.

**Returns**:
A `NotificationModel` object representing the newly created notification.

**Raises**:

- `APIError`: If the notification cannot be created.

**Example**:

```python
# Create a new notification
notification = client.notification.create_notification(
    title="Backup Completed",
    message="The scheduled backup has completed successfully.",
    importance="normal",
    icon="check-circle",
    action_url="/Main/BackupStatus"
)
print(f"Created notification with ID: {notification.id}")
```

### archive_notification

Archives a notification.

```python
def archive_notification(notification_id: str) -> bool
```

**Parameters**:

- `notification_id` (str): The ID of the notification to archive.

**Returns**:
`True` if the notification was successfully archived, `False` otherwise.

**Raises**:

- `APIError`: If the notification does not exist or cannot be archived.

**Example**:

```python
# Archive a notification
result = client.notification.archive_notification(notification_id="abc123")
if result:
    print("Notification archived successfully")
```

### delete_notification

Deletes a notification from the server.

```python
def delete_notification(notification_id: str) -> bool
```

**Parameters**:

- `notification_id` (str): The ID of the notification to delete.

**Returns**:
`True` if the notification was successfully deleted, `False` otherwise.

**Raises**:

- `APIError`: If the notification does not exist or cannot be deleted.

**Example**:

```python
# Delete a notification
result = client.notification.delete_notification(notification_id="abc123")
if result:
    print("Notification deleted successfully")
```

### get_notification_settings

Retrieves the notification settings for the Unraid server.

```python
def get_notification_settings() -> NotificationSettingsModel
```

**Returns**:
A `NotificationSettingsModel` object containing the notification settings.

**Example**:

```python
# Get notification settings
settings = client.notification.get_notification_settings()
print(f"Email notifications enabled: {settings.email.enabled}")
```

### update_notification_settings

Updates the notification settings for the Unraid server.

```python
def update_notification_settings(settings: NotificationSettingsModel) -> NotificationSettingsModel
```

**Parameters**:

- `settings` (NotificationSettingsModel): The notification settings to update.

**Returns**:
A `NotificationSettingsModel` object containing the updated notification settings.

**Raises**:

- `APIError`: If the settings cannot be updated.

**Example**:

```python
# Get current settings
settings = client.notification.get_notification_settings()

# Update email settings
settings.email.enabled = True
settings.email.recipient = "admin@example.com"

# Save updated settings
updated_settings = client.notification.update_notification_settings(settings)
```

## Model Reference

### NotificationModel

Represents a notification on the Unraid server.

**Properties**:

| Name | Type | Description |
|------|------|-------------|
| `id` | str | The notification ID |
| `title` | str | The notification title |
| `message` | str | The notification message |
| `importance` | str | Importance level ("low", "normal", "high", "alert") |
| `timestamp` | datetime | When the notification was created |
| `icon` | str | The notification icon |
| `action_url` | str | URL to open when the notification is clicked |
| `is_read` | bool | Whether the notification has been read |
| `is_archived` | bool | Whether the notification has been archived |
| `source` | str | The source of the notification |

### NotificationSettingsModel

Represents notification settings on the Unraid server.

**Properties**:

| Name | Type | Description |
|------|------|-------------|
| `email` | EmailSettingsModel | Email notification settings |
| `pushover` | PushoverSettingsModel | Pushover notification settings |
| `discord` | DiscordSettingsModel | Discord notification settings |
| `telegram` | TelegramSettingsModel | Telegram notification settings |
| `notification_levels` | Dict[str, str] | Notification levels for different events | 