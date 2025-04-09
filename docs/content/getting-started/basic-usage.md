---
layout: default
title: Basic Usage
parent: Getting Started
nav_order: 3
---

# Basic Usage

This guide covers the basic usage of the Unraid API library, including connecting to your Unraid server and performing common operations.

## Connecting to Your Unraid Server

### Synchronous Client

The synchronous client is the simplest way to connect to your Unraid server:

```python
from unraid_api import UnraidClient

# Connect to Unraid server with API key
client = UnraidClient(
    host="192.168.1.10",
    api_key="your-api-key",
    port=443,  # Default: 443
    use_ssl=True,  # Default: True
    timeout=30.0,  # Default: 30.0
    verify_ssl=False,  # Default: False
)

# Test the connection
system_info = client.info.get_system_info()
print(f"Connected to Unraid version: {system_info.get('os', {}).get('release')}")
```

### Asynchronous Client

For applications that need to perform multiple operations concurrently, the asynchronous client is recommended:

```python
import asyncio
from unraid_api import AsyncUnraidClient

async def main():
    # Connect to Unraid server with API key
    client = AsyncUnraidClient(
        host="192.168.1.10",
        api_key="your-api-key",
        port=443,  # Default: 443
        use_ssl=True,  # Default: True
        timeout=30.0,  # Default: 30.0
        verify_ssl=False,  # Default: False
    )

    # Test the connection
    system_info = await client.info.get_system_info()
    print(f"Connected to Unraid version: {system_info.get('os', {}).get('release')}")

# Run the async function
asyncio.run(main())
```

## Getting System Information

The `info` resource provides access to system information:

```python
# Get system information
system_info = client.info.get_system_info()

# Access specific information
os_info = system_info.get("os", {})
cpu_info = system_info.get("cpu", {})
memory_info = system_info.get("memory", {})
system_details = system_info.get("system", {})

# Print system information
print(f"OS: {os_info.get('distro')} {os_info.get('release')}")
print(f"Kernel: {os_info.get('kernel')}")
print(f"Uptime: {os_info.get('uptime')}")
print(f"CPU: {cpu_info.get('brand')} ({cpu_info.get('cores')} cores, {cpu_info.get('threads')} threads)")
print(f"Memory: {memory_info.get('total') / (1024**3):.2f} GB total, {memory_info.get('used') / (1024**3):.2f} GB used")
print(f"System: {system_details.get('manufacturer')} {system_details.get('model')}")
```

## Managing the Array

The `array` resource provides methods for managing the Unraid array:

```python
# Get array status
array_status = client.array.get_array_status()
print(f"Array state: {array_status.get('state')}")

# Start the array
client.array.start_array()

# Stop the array
client.array.stop_array()

# Start a parity check
client.array.start_parity_check()

# Stop a parity check
client.array.stop_parity_check()
```

## Working with Disks

The `disk` resource provides methods for working with disks:

```python
# Get all disks
disks = client.disk.get_disks()
for disk in disks:
    print(f"Disk: {disk.get('name')} ({disk.get('size') / (1024**3):.2f} GB)")

# Get a specific disk
disk = client.disk.get_disk("sda")
print(f"Disk: {disk.get('name')} ({disk.get('size') / (1024**3):.2f} GB)")

# Get SMART status for a disk
smart_status = client.disk.get_disk_smart("sda")
print(f"SMART status: {smart_status.get('status')}")
```

## Managing Docker Containers

The `docker` resource provides methods for managing Docker containers:

```python
# Get all Docker containers
containers = client.docker.get_containers()
for container in containers:
    print(f"Container: {container.get('names')[0]} ({container.get('state')})")

# Start a container
client.docker.start_container("container_id")

# Stop a container
client.docker.stop_container("container_id")

# Restart a container
client.docker.restart_container("container_id")
```

## Managing Virtual Machines

The `vm` resource provides methods for managing virtual machines:

```python
# Get all VMs
vms = client.vm.get_vms()
for vm in vms.get("domain", []):
    print(f"VM: {vm.get('name')} ({vm.get('state')})")

# Start a VM
client.vm.start_vm("vm_uuid")

# Stop a VM
client.vm.stop_vm("vm_uuid")

# Restart a VM
client.vm.restart_vm("vm_uuid")
```

## Next Steps

Now that you understand the basic usage of the Unraid API library, you can:

1. [Learn how to handle errors](error-handling)
2. [Explore the API reference]({{ site.baseurl }}/content/api/overview)
3. [Use the command-line interface]({{ site.baseurl }}/content/cli/overview)
4. [Integrate with Home Assistant]({{ site.baseurl }}/content/home-assistant/overview)
