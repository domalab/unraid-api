import pytest
from unraid_api import Unraid, SSHExecutor

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
async def test_get_hostname(unraid_instance, mocker):
    mock_execute = mocker.patch.object(unraid_instance, 'execute')
    mock_execute.return_value = {'code': 0, 'stdout': ['test_hostname']}
    
    hostname = await unraid_instance.system.get_hostname()
    assert hostname == 'test_hostname'

@pytest.mark.asyncio
async def test_cpu_usage(unraid_instance, mocker):
    mock_execute = mocker.patch.object(unraid_instance, 'execute')
    mock_execute.return_value = {
        'code': 0, 
        'stdout': ['%Cpu0  :  5.0 us,  2.0 sy,  0.0 ni, 93.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st']
    }
    
    usage = await unraid_instance.system.cpu.usage()
    assert usage.core_count == 1
    assert usage.all.usr == 5.0
    assert usage.all.sys == 2.0
    assert usage.all.idle == 93.0

@pytest.mark.asyncio
async def test_diskfree(unraid_instance, mocker):
    mock_execute = mocker.patch.object(unraid_instance, 'execute')
    mock_execute.return_value = {
        'code': 0, 
        'stdout': [
            'Filesystem     1K-blocks      Used Available Use% Mounted on',
            '/dev/sda1      61255492  12345678  48909814  21% /'
        ]
    }
    
    diskfree = await unraid_instance.system.diskfree.diskfree()
    assert len(diskfree) == 1
    assert diskfree[0].fs == '/dev/sda1'
    assert diskfree[0].used == 12345678
    assert diskfree[0].available == 48909814