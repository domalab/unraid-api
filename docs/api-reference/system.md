---
title: System API
description: System management with the Unraid API
---

# System API

The System API provides access to system-wide operations and information about your Unraid server. This includes getting system information, rebooting, and shutting down the server.

## Available Methods

### get_system_info

Retrieves information about the Unraid system.

```python
def get_system_info() -> SystemInfoModel
```

**Returns**:
A `SystemInfoModel` object containing information about the Unraid system.

**Example**:

```python
# Synchronous client
from unraid_api import UnraidClient

client = UnraidClient("192.168.1.10", api_key="your-api-key")
system_info = client.system.get_system_info()

print(f"Version: {system_info.version}")
print(f"Uptime: {system_info.uptime}")
print(f"Model: {system_info.model}")
```

```python
# Asynchronous client
import asyncio
from unraid_api import AsyncUnraidClient

async def main():
    client = AsyncUnraidClient("192.168.1.10", api_key="your-api-key")
    system_info = await client.system.get_system_info()
    
    print(f"Version: {system_info.version}")
    print(f"Uptime: {system_info.uptime}")
    print(f"Model: {system_info.model}")

asyncio.run(main())
```

### reboot

Reboots the Unraid server.

```python
def reboot() -> bool
```

**Returns**:
`True` if the reboot command was successfully executed, `False` otherwise.

**Raises**:

- `APIError`: If the server cannot be rebooted.

**Example**:

```python
# Reboot the server
result = client.system.reboot()
if result:
    print("Server is rebooting")
```

### shutdown

Shuts down the Unraid server.

```python
def shutdown() -> bool
```

**Returns**:
`True` if the shutdown command was successfully executed, `False` otherwise.

**Raises**:

- `APIError`: If the server cannot be shut down.

**Example**:

```python
# Shutdown the server
result = client.system.shutdown()
if result:
    print("Server is shutting down")
```

### get_cpu_stats

Retrieves CPU usage statistics.

```python
def get_cpu_stats() -> CPUStatsModel
```

**Returns**:
A `CPUStatsModel` object containing CPU usage statistics.

**Example**:

```python
# Get CPU stats
cpu_stats = client.system.get_cpu_stats()
print(f"CPU Usage: {cpu_stats.usage_percent}%")
print(f"CPU Temperature: {cpu_stats.temperature}°C")
```

### get_memory_stats

Retrieves memory usage statistics.

```python
def get_memory_stats() -> MemoryStatsModel
```

**Returns**:
A `MemoryStatsModel` object containing memory usage statistics.

**Example**:

```python
# Get memory stats
memory_stats = client.system.get_memory_stats()
print(f"Total Memory: {memory_stats.total / 1024 / 1024:.2f} MB")
print(f"Used Memory: {memory_stats.used / 1024 / 1024:.2f} MB")
print(f"Free Memory: {memory_stats.free / 1024 / 1024:.2f} MB")
```

### get_network_stats

Retrieves network usage statistics.

```python
def get_network_stats() -> NetworkStatsModel
```

**Returns**:
A `NetworkStatsModel` object containing network usage statistics.

**Example**:

```python
# Get network stats
network_stats = client.system.get_network_stats()
for interface in network_stats.interfaces:
    print(f"Interface: {interface.name}")
    print(f"  RX: {interface.rx_bytes / 1024 / 1024:.2f} MB")
    print(f"  TX: {interface.tx_bytes / 1024 / 1024:.2f} MB")
```

## Model Reference

### SystemInfoModel

Represents information about the Unraid system.

**Properties**:

| Name | Type | Description |
|------|------|-------------|
| `version` | str | Unraid version |
| `uptime` | int | System uptime in seconds |
| `model` | str | Server model |
| `hostname` | str | Server hostname |
| `kernel_version` | str | Linux kernel version |
| `cpu_model` | str | CPU model |
| `cpu_cores` | int | Number of CPU cores |
| `total_memory` | int | Total memory in bytes |
| `board_manufacturer` | str | Motherboard manufacturer |
| `board_model` | str | Motherboard model |
| `machineid` | str | Machine ID |

### CPUStatsModel

Represents CPU usage statistics.

**Properties**:

| Name | Type | Description |
|------|------|-------------|
| `usage_percent` | float | CPU usage percentage |
| `temperature` | float | CPU temperature in Celsius |
| `core_stats` | List[CoreStatsModel] | Per-core statistics |
| `load_average` | List[float] | Load average (1, 5, 15 minutes) |

### CoreStatsModel

Represents statistics for a single CPU core.

**Properties**:

| Name | Type | Description |
|------|------|-------------|
| `core_id` | int | Core ID |
| `usage_percent` | float | Core usage percentage |
| `frequency` | float | Core frequency in MHz |
| `temperature` | float | Core temperature in Celsius |

### MemoryStatsModel

Represents memory usage statistics.

**Properties**:

| Name | Type | Description |
|------|------|-------------|
| `total` | int | Total memory in bytes |
| `used` | int | Used memory in bytes |
| `free` | int | Free memory in bytes |
| `shared` | int | Shared memory in bytes |
| `buffers` | int | Buffer memory in bytes |
| `cached` | int | Cached memory in bytes |
| `swap_total` | int | Total swap in bytes |
| `swap_used` | int | Used swap in bytes |
| `swap_free` | int | Free swap in bytes |

### NetworkStatsModel

Represents network usage statistics.

**Properties**:

| Name | Type | Description |
|------|------|-------------|
| `interfaces` | List[NetworkInterfaceModel] | Network interface statistics |

### NetworkInterfaceModel

Represents statistics for a single network interface.

**Properties**:

| Name | Type | Description |
|------|------|-------------|
| `name` | str | Interface name |
| `status` | str | Interface status |
| `mac_address` | str | MAC address |
| `ip_address` | str | IP address |
| `speed` | int | Link speed in Mbps |
| `rx_bytes` | int | Received bytes |
| `tx_bytes` | int | Transmitted bytes |
| `rx_packets` | int | Received packets |
| `tx_packets` | int | Transmitted packets |
| `rx_errors` | int | Receive errors |
| `tx_errors` | int | Transmit errors | 