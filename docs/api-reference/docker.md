---
title: Docker API
description: Docker container management with the Unraid API
---

# Docker API

The Docker API enables you to manage Docker containers on your Unraid server. This includes listing, starting, stopping, and restarting containers.

## Available Methods

### get_containers

Retrieves a list of all Docker containers on the Unraid server.

```python
def get_containers() -> List[ContainerModel]
```

**Returns**:
A list of `ContainerModel` objects representing each Docker container.

**Example**:

```python
# Synchronous client
from unraid_api import UnraidClient

client = UnraidClient("192.168.1.10", api_key="your-api-key")
containers = client.docker.get_containers()

for container in containers:
    print(f"Container: {container.name}, Status: {container.status}")
```

```python
# Asynchronous client
import asyncio
from unraid_api import AsyncUnraidClient

async def main():
    client = AsyncUnraidClient("192.168.1.10", api_key="your-api-key")
    containers = await client.docker.get_containers()
    
    for container in containers:
        print(f"Container: {container.name}, Status: {container.status}")

asyncio.run(main())
```

### get_container

Retrieves information about a specific Docker container.

```python
def get_container(container_id: str) -> ContainerModel
```

**Parameters**:

- `container_id` (str): The ID or name of the container to retrieve.

**Returns**:
A `ContainerModel` object representing the specified container.

**Raises**:

- `APIError`: If the container does not exist or cannot be accessed.

**Example**:

```python
# Get a specific container
container = client.docker.get_container(container_id="plex")
print(f"Container: {container.name}, Status: {container.status}")
```

### start_container

Starts a Docker container.

```python
def start_container(container_id: str) -> bool
```

**Parameters**:

- `container_id` (str): The ID or name of the container to start.

**Returns**:
`True` if the container was successfully started, `False` otherwise.

**Raises**:

- `APIError`: If the container does not exist or cannot be started.

**Example**:

```python
# Start a container
result = client.docker.start_container(container_id="plex")
if result:
    print("Container started successfully")
```

### stop_container

Stops a Docker container.

```python
def stop_container(container_id: str) -> bool
```

**Parameters**:

- `container_id` (str): The ID or name of the container to stop.

**Returns**:
`True` if the container was successfully stopped, `False` otherwise.

**Raises**:

- `APIError`: If the container does not exist or cannot be stopped.

**Example**:

```python
# Stop a container
result = client.docker.stop_container(container_id="plex")
if result:
    print("Container stopped successfully")
```

### restart_container

Restarts a Docker container.

```python
def restart_container(container_id: str) -> bool
```

**Parameters**:

- `container_id` (str): The ID or name of the container to restart.

**Returns**:
`True` if the container was successfully restarted, `False` otherwise.

**Raises**:

- `APIError`: If the container does not exist or cannot be restarted.

**Example**:

```python
# Restart a container
result = client.docker.restart_container(container_id="plex")
if result:
    print("Container restarted successfully")
```

## Model Reference

### ContainerModel

Represents a Docker container.

**Properties**:

| Name | Type | Description |
|------|------|-------------|
| `id` | str | The container ID |
| `name` | str | The container name |
| `image` | str | The container image |
| `status` | str | The container status (e.g., "running", "stopped") |
| `created` | datetime | When the container was created |
| `ports` | List[PortMapping] | List of port mappings |
| `volumes` | List[VolumeMapping] | List of volume mappings |
| `env` | Dict[str, str] | Environment variables |
| `command` | str | The command used to run the container |
| `cpu_usage` | float | Current CPU usage percentage |
| `memory_usage` | int | Current memory usage in bytes |
| `memory_limit` | int | Memory limit in bytes |
| `network_rx` | int | Network receive in bytes |
| `network_tx` | int | Network transmit in bytes |

### PortMapping

Represents a port mapping for a Docker container.

**Properties**:

| Name | Type | Description |
|------|------|-------------|
| `container_port` | int | The port inside the container |
| `host_port` | int | The port on the host |
| `protocol` | str | The protocol (e.g., "tcp", "udp") |

### VolumeMapping

Represents a volume mapping for a Docker container.

**Properties**:

| Name | Type | Description |
|------|------|-------------|
| `container_path` | str | The path inside the container |
| `host_path` | str | The path on the host |
| `mode` | str | The access mode (e.g., "rw", "ro") |

## Real-time Subscriptions

The Docker API supports subscribing to container status changes in real-time.

### subscribe_to_containers

Subscribes to real-time updates for all Docker containers.

```python
def subscribe_to_containers() -> AsyncGenerator[ContainerModel, None]
```

**Returns**:
An asynchronous generator that yields `ContainerModel` objects when container statuses change.

**Example**:

```python
import asyncio
from unraid_api import AsyncUnraidClient

async def main():
    client = AsyncUnraidClient("192.168.1.10", api_key="your-api-key")
    
    # Subscribe to container updates
    async for container in client.docker.subscribe_to_containers():
        print(f"Container update: {container.name} is now {container.status}")
        
        # Process other container properties
        print(f"CPU Usage: {container.cpu_usage}%")
        print(f"Memory Usage: {container.memory_usage / 1024 / 1024} MB")

asyncio.run(main())
```

This subscription will continue until the connection is closed or an error occurs. 