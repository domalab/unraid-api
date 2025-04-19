---
title: Array API
description: Array management with the Unraid API
---

# Array API

The Array API enables you to manage your Unraid disk array. This includes starting and stopping the array, checking its status, and running operations like parity checks.

## Available Methods

### get_array_status

Retrieves the current status of the Unraid array.

```python
def get_array_status() -> ArrayStatusModel
```

**Returns**:
An `ArrayStatusModel` object representing the current status of the array.

**Example**:

```python
# Synchronous client
from unraid_api import UnraidClient

client = UnraidClient("192.168.1.10", api_key="your-api-key")
array_status = client.array.get_array_status()

print(f"Array status: {array_status.status}")
print(f"Protection mode: {array_status.protection_mode}")
```

```python
# Asynchronous client
import asyncio
from unraid_api import AsyncUnraidClient

async def main():
    client = AsyncUnraidClient("192.168.1.10", api_key="your-api-key")
    array_status = await client.array.get_array_status()
    
    print(f"Array status: {array_status.status}")
    print(f"Protection mode: {array_status.protection_mode}")

asyncio.run(main())
```

### start_array

Starts the Unraid array.

```python
def start_array() -> bool
```

**Returns**:
`True` if the array was successfully started, `False` otherwise.

**Raises**:

- `APIError`: If the array cannot be started.

**Example**:

```python
# Start the array
result = client.array.start_array()
if result:
    print("Array started successfully")
```

### stop_array

Stops the Unraid array.

```python
def stop_array() -> bool
```

**Returns**:
`True` if the array was successfully stopped, `False` otherwise.

**Raises**:

- `APIError`: If the array cannot be stopped.

**Example**:

```python
# Stop the array
result = client.array.stop_array()
if result:
    print("Array stopped successfully")
```

### start_parity_check

Starts a parity check operation on the array.

```python
def start_parity_check(correcting: bool = False) -> bool
```

**Parameters**:

- `correcting` (bool, optional): Whether to perform a correcting parity check. Default is `False`.

**Returns**:
`True` if the parity check was successfully started, `False` otherwise.

**Raises**:

- `APIError`: If the parity check cannot be started.

**Example**:

```python
# Start a parity check
result = client.array.start_parity_check()
if result:
    print("Parity check started")

# Start a correcting parity check
result = client.array.start_parity_check(correcting=True)
if result:
    print("Correcting parity check started")
```

### stop_parity_check

Stops an ongoing parity check operation.

```python
def stop_parity_check() -> bool
```

**Returns**:
`True` if the parity check was successfully stopped, `False` otherwise.

**Raises**:

- `APIError`: If the parity check cannot be stopped.

**Example**:

```python
# Stop a parity check
result = client.array.stop_parity_check()
if result:
    print("Parity check stopped")
```

## Model Reference

### ArrayStatusModel

Represents the status of the Unraid array.

**Properties**:

| Name | Type | Description |
|------|------|-------------|
| `status` | str | The array status (e.g., "Started", "Stopped") |
| `protection_mode` | str | The protection mode (e.g., "Parity", "Dual Parity") |
| `size` | int | Total size of the array in bytes |
| `used` | int | Used space in bytes |
| `free` | int | Free space in bytes |
| `parity_status` | str | Status of the parity (e.g., "Valid", "Checking") |
| `parity_check_progress` | float | Parity check progress percentage (0-100) |
| `parity_sync_speed` | float | Parity sync speed in MB/s |
| `parity_estimated_finish` | datetime | Estimated finish time for parity operations |
| `disks` | List[DiskModel] | List of disks in the array |

### DiskModel

Represents a disk in the Unraid array.

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