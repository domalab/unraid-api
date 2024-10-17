import pytest
from unraid_api import Unraid, SSHExecutor
from unraid_api.exceptions import ExecutionError

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
async def test_get_case_model(unraid_instance, mocker):
    mock_execute = mocker.patch.object(unraid_instance, 'execute')
    mock_execute.return_value = {'code': 0, 'stdout': ['Test Case Model']}
    
    result = await unraid_instance.unraid.get_case_model()
    assert result == 'Test Case Model'

@pytest.mark.asyncio
async def test_set_case_model(unraid_instance, mocker):
    mock_execute = mocker.patch.object(unraid_instance, 'execute')
    mock_execute.return_value = {'code': 0, 'stdout': []}
    
    await unraid_instance.unraid.set_case_model('New Case Model')
    mock_execute.assert_called_once()

@pytest.mark.asyncio
async def test_get_ident_config(unraid_instance, mocker):
    mock_execute = mocker.patch.object(unraid_instance, 'execute')
    mock_execute.return_value = {
        'code': 0, 
        'stdout': ['NAME="UnraidServer"', 'TIMEZONE="UTC"']
    }
    
    result = await unraid_instance.unraid.get_ident_config()
    assert result.name == 'UnraidServer'
    assert result.timezone == 'UTC'