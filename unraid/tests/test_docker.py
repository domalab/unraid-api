import pytest
from unraid_api import Unraid, SSHExecutor
from unraid_api.docker import Container

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
async def test_list_containers(unraid_instance, mocker):
    mock_fetch = mocker.patch.object(unraid_instance.docker, 'fetch')
    mock_fetch.return_value = [
        {
            "Id": "123",
            "Names": ["/test_container"],
            "State": "running"
        }
    ]
    
    containers = await unraid_instance.docker.list()
    assert len(containers) == 1
    assert isinstance(containers[0], Container)
    assert containers[0].name == "test_container"
    assert containers[0].state == "running"

@pytest.mark.asyncio
async def test_container_stop(unraid_instance, mocker):
    mock_execute = mocker.patch.object(unraid_instance, 'execute')
    mock_execute.return_value = {'code': 0, 'stdout': []}
    
    container = Container(unraid_instance, {"Id": "123", "Names": ["/test_container"]})
    await container.stop()
    
    mock_execute.assert_called_once_with('docker stop "123"')