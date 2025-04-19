---
title: VM API
description: Virtual Machine management with the Unraid API
---

# VM API

The VM API allows you to manage virtual machines on your Unraid server. This includes starting, stopping, and monitoring VMs.

## Available Methods

### get_vms

Retrieves a list of all virtual machines on the Unraid server.

```python
def get_vms() -> List[VMModel]
```

**Returns**:
A list of `VMModel` objects representing each virtual machine.

**Example**:

```python
# Synchronous client
from unraid_api import UnraidClient

client = UnraidClient("192.168.1.10", api_key="your-api-key")
vms = client.vm.get_vms()

for vm in vms:
    print(f"VM: {vm.name}, Status: {vm.status}")
```

```python
# Asynchronous client
import asyncio
from unraid_api import AsyncUnraidClient

async def main():
    client = AsyncUnraidClient("192.168.1.10", api_key="your-api-key")
    vms = await client.vm.get_vms()
    
    for vm in vms:
        print(f"VM: {vm.name}, Status: {vm.status}")

asyncio.run(main())
```

### get_vm

Retrieves information about a specific virtual machine.

```python
def get_vm(vm_id: str) -> VMModel
```

**Parameters**:

- `vm_id` (str): The ID or name of the VM to retrieve.

**Returns**:
A `VMModel` object representing the specified VM.

**Raises**:

- `APIError`: If the VM does not exist or cannot be accessed.

**Example**:

```python
# Get a specific VM
vm = client.vm.get_vm(vm_id="windows10")
print(f"VM: {vm.name}, Status: {vm.status}")
```

### start_vm

Starts a virtual machine.

```python
def start_vm(vm_id: str) -> bool
```

**Parameters**:

- `vm_id` (str): The ID or name of the VM to start.

**Returns**:
`True` if the VM was successfully started, `False` otherwise.

**Raises**:

- `APIError`: If the VM does not exist or cannot be started.

**Example**:

```python
# Start a VM
result = client.vm.start_vm(vm_id="windows10")
if result:
    print("VM started successfully")
```

### stop_vm

Stops a virtual machine.

```python
def stop_vm(vm_id: str, force: bool = False) -> bool
```

**Parameters**:

- `vm_id` (str): The ID or name of the VM to stop.
- `force` (bool, optional): Whether to force stop the VM. Default is `False`.

**Returns**:
`True` if the VM was successfully stopped, `False` otherwise.

**Raises**:

- `APIError`: If the VM does not exist or cannot be stopped.

**Example**:

```python
# Stop a VM gracefully
result = client.vm.stop_vm(vm_id="windows10")
if result:
    print("VM stopped successfully")

# Force stop a VM
result = client.vm.stop_vm(vm_id="windows10", force=True)
if result:
    print("VM force stopped")
```

### restart_vm

Restarts a virtual machine.

```python
def restart_vm(vm_id: str) -> bool
```

**Parameters**:

- `vm_id` (str): The ID or name of the VM to restart.

**Returns**:
`True` if the VM was successfully restarted, `False` otherwise.

**Raises**:

- `APIError`: If the VM does not exist or cannot be restarted.

**Example**:

```python
# Restart a VM
result = client.vm.restart_vm(vm_id="windows10")
if result:
    print("VM restarted successfully")
```

### pause_vm

Pauses a running virtual machine.

```python
def pause_vm(vm_id: str) -> bool
```

**Parameters**:

- `vm_id` (str): The ID or name of the VM to pause.

**Returns**:
`True` if the VM was successfully paused, `False` otherwise.

**Raises**:

- `APIError`: If the VM does not exist or cannot be paused.

**Example**:

```python
# Pause a VM
result = client.vm.pause_vm(vm_id="windows10")
if result:
    print("VM paused successfully")
```

### resume_vm

Resumes a paused virtual machine.

```python
def resume_vm(vm_id: str) -> bool
```

**Parameters**:

- `vm_id` (str): The ID or name of the VM to resume.

**Returns**:
`True` if the VM was successfully resumed, `False` otherwise.

**Raises**:

- `APIError`: If the VM does not exist or cannot be resumed.

**Example**:

```python
# Resume a VM
result = client.vm.resume_vm(vm_id="windows10")
if result:
    print("VM resumed successfully")
```

## Model Reference

### VMModel

Represents a virtual machine on the Unraid server.

**Properties**:

| Name | Type | Description |
|------|------|-------------|
| `id` | str | The VM ID |
| `name` | str | The VM name |
| `status` | str | Status (e.g., "running", "stopped", "paused") |
| `cpu_count` | int | Number of vCPUs |
| `memory` | int | Memory allocation in bytes |
| `primary_gpu` | str | Primary GPU assigned |
| `vnc_port` | int | VNC port for remote access |
| `description` | str | VM description |
| `autostart` | bool | Whether the VM is set to autostart |
| `template` | str | VM template |
| `disks` | List[VMDiskModel] | VM disk devices |
| `network_interfaces` | List[VMNetworkModel] | VM network interfaces |
| `usb_devices` | List[VMUSBModel] | Attached USB devices | 