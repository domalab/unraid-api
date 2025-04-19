---
title: Quick Start
description: Get started quickly with the Unraid API client
---

# Quick Start

This guide will help you get started with the Unraid API library by walking through common usage patterns.

## Prerequisites

Before you begin:

1. [Install the library](installation.md)
2. [Set up authentication](authentication.md) with your API key

## Basic Usage

### Synchronous Client

```python
from unraid_api import UnraidClient

# Connect to Unraid server with API key
client = UnraidClient("192.168.1.10", api_key="your-api-key")

# Get system info
system_info = client.get_system_info()
print(f"System version: {system_info.version}")
print(f"Uptime: {system_info.uptime}")
```

### Asynchronous Client

```python
import asyncio
from unraid_api import AsyncUnraidClient

async def main():
    client = AsyncUnraidClient("192.168.1.10", api_key="your-api-key")
    
    # Get system info
    system_info = await client.get_system_info()
    print(f"System version: {system_info.version}")
    print(f"Uptime: {system_info.uptime}")

# Run the async function
asyncio.run(main())
```

## Common Operations

### Working with Docker Containers

```python
# Get all Docker containers
containers = client.docker.get_containers()
for container in containers:
    print(f"Container: {container.name}, Status: {container.status}")

# Start a container
client.docker.start_container(container_id="container_name")

# Stop a container
client.docker.stop_container(container_id="container_name")

# Restart a container
client.docker.restart_container(container_id="container_name")
```

### Working with the Array

```python
# Get array status
array_status = client.array.get_array_status()
print(f"Array status: {array_status.status}")
print(f"Protection mode: {array_status.protection_mode}")

# Start the array
client.array.start_array()

# Stop the array
client.array.stop_array()

# Start a parity check
client.array.start_parity_check()
```

### Working with VMs

```python
# Get all VMs
vms = client.vm.get_vms()
for vm in vms:
    print(f"VM: {vm.name}, Status: {vm.status}")

# Start a VM
client.vm.start_vm(vm_id="vm_name")

# Stop a VM
client.vm.stop_vm(vm_id="vm_name")

# Restart a VM
client.vm.restart_vm(vm_id="vm_name")
```

### System Operations

```python
# Get notification settings
notifications = client.notification.get_notifications()
for notification in notifications:
    print(f"Notification: {notification.title}")

# Reboot the system
client.system.reboot()

# Shutdown the system
client.system.shutdown()
```

## Error Handling

```python
from unraid_api import UnraidClient
from unraid_api.exceptions import AuthenticationError, ConnectionError, APIError

try:
    client = UnraidClient("192.168.1.10", api_key="your-api-key")
    system_info = client.get_system_info()
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except ConnectionError as e:
    print(f"Connection error: {e}")
except APIError as e:
    print(f"API error: {e}")
```

## Next Steps

Now that you've learned the basics, explore the [API Reference](../api-reference/overview.md) for detailed information about all available endpoints and methods. 