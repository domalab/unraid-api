from typing import List
from datetime import datetime
from pydantic import BaseModel
from ..unraid import Unraid
from ..exceptions import ExecutionError, ParseError

class RichNotification(BaseModel):
    file_name: str
    created: datetime
    event: str
    subject: str
    description: str
    importance: str
    is_archived: bool

class NotificationCount(BaseModel):
    unread: int
    archived: int

class NotificationModule:
    """
    Module for managing notifications on an Unraid server.
    """

    def __init__(self, instance: Unraid):
        """
        Initialize the Notification module.

        Args:
            instance: The Unraid instance to use for executing commands.
        """
        self.instance = instance

    async def get_notifications(self) -> List[RichNotification]:
        """
        Get all notifications from the Unraid server.

        Returns:
            A list of RichNotification objects representing all notifications.

        Raises:
            ExecutionError: If the command to list notifications fails.
            ParseError: If the notification data cannot be parsed.
        """
        unread = await self._list_notifications('unread')
        archived = await self._list_notifications('archive')
        
        notifications = await self._load_notifications(unread, False)
        notifications.extend(await self._load_notifications(archived, True))
        
        return sorted(notifications, key=lambda n: n.created)

    async def get_notification_count(self) -> NotificationCount:
        """
        Get the count of unread and archived notifications.

        Returns:
            A NotificationCount object with the counts of unread and archived notifications.

        Raises:
            ExecutionError: If the command to list notifications fails.
        """
        unread = await self._list_notifications('unread')
        archived = await self._list_notifications('archive')
        
        return NotificationCount(unread=len(unread), archived=len(archived))

    async def delete_notification(self, notification_name: str, is_archived: bool):
        """
        Delete a specific notification.

        Args:
            notification_name: The name of the notification file to delete.
            is_archived: Whether the notification is in the archived folder.

        Raises:
            ExecutionError: If the delete command fails.
        """
        folder = 'archive' if is_archived else 'unread'
        result = await self.instance.execute(f"rm /tmp/notifications/{folder}/{notification_name}")
        if result['code'] != 0:
            raise ExecutionError("Failed to delete notification")

    async def toggle_notification_archive_state(self, notification_name: str, is_archived: bool):
        """
        Toggle the archive state of a notification.

        Args:
            notification_name: The name of the notification file to toggle.
            is_archived: The current archive state of the notification.

        Raises:
            ExecutionError: If the move command fails.
        """
        src_folder = 'archive' if is_archived else 'unread'
        dst_folder = 'unread' if is_archived else 'archive'
        result = await self.instance.execute(
            f"mv /tmp/notifications/{src_folder}/{notification_name} "
            f"/tmp/notifications/{dst_folder}/{notification_name}"
        )
        if result['code'] != 0:
            raise ExecutionError("Failed to toggle notification archive state")

    async def _list_notifications(self, folder: str) -> List[str]:
        """
        List notification files in a specific folder.

        Args:
            folder: The folder to list notifications from ('unread' or 'archive').

        Returns:
            A list of notification file names.

        Raises:
            ExecutionError: If the list command fails.
        """
        result = await self.instance.execute(f"ls -1 /tmp/notifications/{folder}/")
        if result['code'] != 0:
            raise ExecutionError(f"Failed to list notifications in {folder} folder")
        return result['stdout']

    async def _load_notifications(self, sources: List[str], is_archived: bool) -> List[RichNotification]:
        """
        Load notification data for a list of notification files.

        Args:
            sources: A list of notification file names to load.
            is_archived: Whether these notifications are from the archive folder.

        Returns:
            A list of RichNotification objects.

        Raises:
            ExecutionError: If loading a notification fails.
            ParseError: If parsing a notification fails.
        """
        notifications = []
        for source in sources:
            try:
                notification = await self._load_notification(source, is_archived)
                if notification:
                    notifications.append(notification)
            except (ExecutionError, ParseError) as e:
                # Log the error or handle it as appropriate
                print(f"Error loading notification {source}: {str(e)}")
        return notifications

    async def _load_notification(self, source: str, is_archived: bool) -> RichNotification:
        """
        Load data for a single notification file.

        Args:
            source: The name of the notification file to load.
            is_archived: Whether this notification is from the archive folder.

        Returns:
            A RichNotification object.

        Raises:
            ExecutionError: If the read command fails.
            ParseError: If parsing the notification data fails.
        """
        folder = 'archive' if is_archived else 'unread'
        result = await self.instance.execute(f"cat /tmp/notifications/{folder}/{source}")
        if result['code'] != 0:
            raise ExecutionError(f"Failed to read notification {source}")
        return self._parse_notification(result['stdout'], source, is_archived)

    def _parse_notification(self, content: List[str], file_name: str, is_archived: bool) -> RichNotification:
        """
        Parse notification data into a RichNotification object.

        Args:
            content: The content of the notification file.
            file_name: The name of the notification file.
            is_archived: Whether this notification is archived.

        Returns:
            A RichNotification object.

        Raises:
            ParseError: If parsing the notification data fails.
        """
        try:
            timestamp = int(content[0].split('=', 1)[1]) * 1000
            event = content[1].split('=', 1)[1]
            subject = content[2].split('=', 1)[1]
            description = content[3].split('=', 1)[1]
            importance = content[4].split('=', 1)[1]

            return RichNotification(
                file_name=file_name,
                created=datetime.fromtimestamp(timestamp / 1000),
                event=event,
                subject=subject,
                description=description,
                importance=importance,
                is_archived=is_archived
            )
        except (IndexError, ValueError) as e:
            raise ParseError(f"Failed to parse notification {file_name}: {str(e)}")