import pytest
from unraid_api import Unraid, SSHExecutor
from unraid_api.exceptions import ConnectionError, ExecutionError

@pytest.fixture
async def unraid_instance():
    unraid = Unraid(SSHExecutor, {
        'host': 'mock_host',
        'username': 'mock_user',
        'password': 'mock_password',
        'port': 22
    })
    yield unraid

@pytest.mark.asyncio
async def test_connect(unraid_instance, mocker):
    mock_connect = mocker.patch.object(unraid_instance.executor, 'connect')
    await unraid_instance.connect()
    mock_connect.assert_called_once()

@pytest.mark.asyncio
async def test_connect_error(unraid_instance, mocker):
    mock_connect = mocker.patch.object(unraid_instance.executor, 'connect')
    mock_connect.side_effect = Exception("Connection failed")
    
    with pytest.raises(ConnectionError):
        await unraid_instance.connect()

@pytest.mark.asyncio
async def test_execute(unraid_instance, mocker):
    mock_execute = mocker.patch.object(unraid_instance.executor, 'execute')
    mock_execute.return_value = {'code': 0, 'stdout': ['test output']}
    
    result = await unraid_instance.execute('test command')
    assert result['stdout'] == ['test output']

@pytest.mark.asyncio
async def test_execute_error(unraid_instance, mocker):
    mock_execute = mocker.patch.object(unraid_instance.executor, 'execute')
    mock_execute.side_effect = Exception("Execution failed")
    
    with pytest.raises(ExecutionError):
        await unraid_instance.execute('test command')