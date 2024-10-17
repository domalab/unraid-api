import pytest
from unraid_api import Unraid, SSHExecutor
from unraid_api.vm import VM, VMState

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
async def test_list_vms(unraid_instance, mocker):
    mock_execute = mocker.patch.object(unraid_instance, 'execute')
    mock_execute.return_value = {
        'code': 0, 
        'stdout': [
            ' Id    Name                           State',
            '----------------------------------------------------',
            ' 1     test_vm                        running',
            ' -     inactive_vm                    shut off'
        ]
    }
    
    vms = await unraid_instance.vm.list()
    assert len(vms) == 2
    assert isinstance(vms[0], VM)
    assert vms[0].name == "test_vm"
    assert vms[0].state == VMState.RUNNING
    assert vms[1].name == "inactive_vm"
    assert vms[1].state == VMState.STOPPED

@pytest.mark.asyncio
async def test_vm_start(unraid_instance, mocker):
    mock_execute = mocker.patch.object(unraid_instance, 'execute')
    mock_execute.return_value = {'code': 0, 'stdout': []}
    
    vm = VM(unraid_instance, "test_vm", VMState.STOPPED)
    await vm.start()
    
    mock_execute.assert_called_once_with('virsh start "test_vm"')

@pytest.mark.asyncio
async def test_vm_shutdown(unraid_instance, mocker):
    mock_execute = mocker.patch.object(unraid_instance, 'execute')
    mock_execute.return_value = {'code': 0, 'stdout': []}
    
    vm = VM(unraid_instance, "test_vm", VMState.RUNNING)
    await vm.shutdown()
    
    mock_execute.assert_called_once_with('virsh shutdown "test_vm" --mode acpi')