---
title: Disk API
description: Disk management with the Unraid API
---

# Disk API

The Disk API allows you to manage and monitor disks within your Unraid server. This includes getting information about disks, mounting, unmounting, and monitoring disk health.

## Available Methods

### get_disks

Retrieves a list of all disks on the Unraid server.

```python
def get_disks() -> List[DiskModel]
```

**Returns**:
A list of `DiskModel` objects representing each disk.

**Example**:

```python
# Synchronous client
from unraid_api import UnraidClient

client = UnraidClient("192.168.1.10", api_key="your-api-key")
disks = client.disk.get_disks()

for disk in disks:
    print(f"Disk: {disk.name}, Size: {disk.size / 1024 / 1024 / 1024:.2f} GB")
```

```python
# Asynchronous client
import asyncio
from unraid_api import AsyncUnraidClient

async def main():
    client = AsyncUnraidClient("192.168.1.10", api_key="your-api-key")
    disks = await client.disk.get_disks()
    
    for disk in disks:
        print(f"Disk: {disk.name}, Size: {disk.size / 1024 / 1024 / 1024:.2f} GB")

asyncio.run(main())
```

### get_disk

Retrieves information about a specific disk.

```python
def get_disk(disk_id: str) -> DiskModel
```

**Parameters**:

- `disk_id` (str): The ID or name of the disk to retrieve.

**Returns**:
A `DiskModel` object representing the specified disk.

**Raises**:

- `APIError`: If the disk does not exist or cannot be accessed.

**Example**:

```python
# Get a specific disk
disk = client.disk.get_disk(disk_id="disk1")
print(f"Disk: {disk.name}, Status: {disk.status}")
```

### mount_disk

Mounts a disk.

```python
def mount_disk(disk_id: str) -> bool
```

**Parameters**:

- `disk_id` (str): The ID or name of the disk to mount.

**Returns**:
`True` if the disk was successfully mounted, `False` otherwise.

**Raises**:

- `APIError`: If the disk does not exist or cannot be mounted.

**Example**:

```python
# Mount a disk
result = client.disk.mount_disk(disk_id="disk1")
if result:
    print("Disk mounted successfully")
```

### unmount_disk

Unmounts a disk.

```python
def unmount_disk(disk_id: str) -> bool
```

**Parameters**:

- `disk_id` (str): The ID or name of the disk to unmount.

**Returns**:
`True` if the disk was successfully unmounted, `False` otherwise.

**Raises**:

- `APIError`: If the disk does not exist or cannot be unmounted.

**Example**:

```python
# Unmount a disk
result = client.disk.unmount_disk(disk_id="disk1")
if result:
    print("Disk unmounted successfully")
```

### check_disk_health

Checks the health status of a disk.

```python
def check_disk_health(disk_id: str) -> DiskHealthModel
```

**Parameters**:

- `disk_id` (str): The ID or name of the disk to check.

**Returns**:
A `DiskHealthModel` object representing the health status of the disk.

**Raises**:

- `APIError`: If the disk does not exist or its health cannot be checked.

**Example**:

```python
# Check disk health
health = client.disk.check_disk_health(disk_id="disk1")
print(f"Health status: {health.status}")
print(f"SMART attributes: {health.smart_attributes}")
```

## Model Reference

### DiskModel

Represents a disk in the Unraid server.

**Properties**:

| Name | Type | Description |
|------|------|-------------|
| `id` | str | The disk ID |
| `name` | str | The disk name |
| `device` | str | The device path |
| `serial` | str | The disk serial number |
| `model` | str | The disk model |
| `size` | int | Size in bytes |
| `used` | int | Used space in bytes |
| `free` | int | Free space in bytes |
| `status` | str | Status (e.g., "Normal", "SMART errors") |
| `temperature` | float | Current temperature in Celsius |
| `type` | str | Type (e.g., "data", "parity", "cache") |
| `mounted` | bool | Whether the disk is mounted |
| `file_system` | str | The file system type |

### DiskHealthModel

Represents the health status of a disk.

**Properties**:

| Name | Type | Description |
|------|------|-------------|
| `id` | str | The disk ID |
| `status` | str | Overall health status (e.g., "Good", "Warning", "Bad") |
| `smart_status` | str | SMART status (e.g., "PASSED", "FAILED") |
| `temperature` | float | Current temperature in Celsius |
| `power_on_hours` | int | Hours the disk has been powered on |
| `smart_attributes` | Dict[str, Any] | SMART attributes and values |
| `recent_errors` | List[str] | Recent error messages | 