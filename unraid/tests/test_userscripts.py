import pytest
from unraid_api import Unraid, SSHExecutor
from unraid_api.userscripts import UserScript

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
async def test_has_user_scripts_installed(unraid_instance, mocker):
    mock_execute = mocker.patch.object(unraid_instance, 'execute')
    mock_execute.return_value = {'code': 0, 'stdout': []}
    
    result = await unraid_instance.userscripts.has_user_scripts_installed()
    assert result == True

@pytest.mark.asyncio
async def test_get_user_scripts(unraid_instance, mocker):
    mock_execute = mocker.patch.object(unraid_instance, 'execute')
    mock_execute.return_value = {
        'code': 0, 
        'stdout': ['[{"name": "Test Script", "dirName": "test_script", "running": false, "script": "#!/bin/bash\\necho Hello"}]']
    }
    
    scripts = await unraid_instance.userscripts.get_user_scripts()
    assert len(scripts) == 1
    assert isinstance(scripts[0], UserScript)
    assert scripts[0].name == "Test Script"
    assert scripts[0].dir_name == "test_script"

@pytest.mark.asyncio
async def test_create_user_script(unraid_instance, mocker):
    mock_execute = mocker.patch.object(unraid_instance, 'execute')
    mock_execute.return_value = {'code': 0, 'stdout': []}
    
    script = await unraid_instance.userscripts.create_user_script("New Script", "#!/bin/bash\necho Hello", "Test Description")
    assert isinstance(script, UserScript)
    assert script.name == "New Script"
    assert script.description == "Test Description"