---
title: API Reference Overview
description: Overview of the Unraid API resources
---

# API Reference Overview

The Unraid API library provides a comprehensive set of resources that allow you to interact with all aspects of your Unraid server. This section provides detailed documentation for each resource.

## Available Resources

| Resource | Description |
|----------|-------------|
| [Array](array.md) | Manage the Unraid array - start, stop, and check status |
| [Disk](disk.md) | Control and monitor disks within the array |
| [Docker](docker.md) | Manage Docker containers |
| [VM](vm.md) | Control virtual machines |
| [System](system.md) | System-wide operations and information |
| [User](user.md) | User management functions |
| [Notification](notification.md) | Handle Unraid notifications |

## Client Structure

The client object provides access to various resources through properties. For example:

```python
from unraid_api import UnraidClient

client = UnraidClient("192.168.1.10", api_key="your-api-key")

# Access resources through properties
client.array    # Array resource
client.disk     # Disk resource
client.docker   # Docker resource
client.vm       # VM resource
client.system   # System resource
client.user     # User resource
client.notification  # Notification resource
```

## Common Patterns

Most resources follow a common pattern for method naming:

- `get_*`: Methods that retrieve information
- `create_*`: Methods that create new resources
- `update_*`: Methods that modify existing resources
- `delete_*`: Methods that remove resources
- `start_*`, `stop_*`, `restart_*`: Methods that control the state of resources

## Models

The library uses Pydantic models to provide strongly typed responses. Each API call returns a structured model with appropriate type hints, making it easier to work with the data and benefit from IDE autocompletion.

For example:

```python
# Get system info
system_info = client.get_system_info()

# Access properties of the returned model
print(system_info.version)  # The Unraid version
print(system_info.uptime)   # Server uptime
```

## Error Handling

API calls may raise various exceptions. See the [Error Handling](../advanced/error-handling.md) section for details on available exceptions and how to handle them effectively. 