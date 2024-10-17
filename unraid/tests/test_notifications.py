import pytest
from unraid_api import Unraid, SSHExecutor
from unraid_api.notifications import RichNotification

@pytest.fixture
async def unraid_instance():
    unraid = Unraid(SSHExecutor, {
        'host': 'mock_host',
        'username': 'mock_user',
        'password': 'mock_password',
        'port': 22
    })
    await unraid.connect()
    yield unraid
    await unraid.disconnect()

@pytest.mark.asyncio
async def test_get_notifications(unraid_instance, mocker):
    mock_execute = mocker.patch.object(unraid_instance, 'execute')
    mock_execute.side_effect = [
        {'code': 0, 'stdout': ['notification1']},
        {'code': 0, 'stdout': ['notification2']},
        {'code': 0, 'stdout': ['TIMESTAMP=1622505600', 'EVENT=Test', 'SUBJECT=Test Subject', 'DESCRIPTION=Test Description', 'IMPORTANCE=normal']},
        {'code': 0, 'stdout': ['TIMESTAMP=1622505601', 'EVENT=Test2', 'SUBJECT=Test Subject 2', 'DESCRIPTION=Test Description 2', 'IMPORTANCE=high']}
    ]
    
    notifications = await unraid_instance.notifications.get_notifications()
    assert len(notifications) == 2
    assert isinstance(notifications[0], RichNotification)
    assert notifications[0].event == 'Test'
    assert notifications[1].event == 'Test2'

@pytest.mark.asyncio
async def test_get_notification_count(unraid_instance, mocker):
    mock_execute = mocker.patch.object(unraid_instance, 'execute')
    mock_execute.side_effect = [
        {'code': 0, 'stdout': ['notification1', 'notification2']},
        {'code': 0, 'stdout': ['archived_notification']}
    ]
    
    count = await unraid_instance.notifications.get_notification_count()
    assert count.unread == 2
    assert count.archived == 1