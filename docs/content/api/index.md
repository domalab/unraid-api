---
layout: default
title: API Reference
nav_order: 3
has_children: true
permalink: /content/api
---

# API Reference

This section provides detailed documentation for the Unraid API library. It covers all the available resources and methods, along with examples of how to use them.

## Resources

The Unraid API library is organized into resources, each representing a different aspect of the Unraid server:

- [GraphQL API Reference](graphql-api) - Complete reference for the Unraid GraphQL API
- [System Information](system-info) - Get information about the Unraid server
- [Array Management](array) - Manage the Unraid array
- [Disk Operations](disk) - Work with disks
- [Docker Containers](docker) - Manage Docker containers
- [Virtual Machines](vm) - Manage virtual machines
- [User Management](user) - Manage users
- [Notifications](notification) - Manage notifications
- [Configuration](config) - Manage configuration

## Client Classes

The library provides two client classes:

- `UnraidClient` - Synchronous client for the Unraid GraphQL API
- `AsyncUnraidClient` - Asynchronous client for the Unraid GraphQL API

Both clients provide the same functionality, but the asynchronous client is designed for use in asynchronous applications.

## Client Options

When creating a client, you can specify the following options:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `host` | str | - | The hostname or IP address of the Unraid server |
| `api_key` | str | - | The API key for authentication |
| `port` | int | 443 | The port to connect to |
| `use_ssl` | bool | True | Whether to use SSL |
| `timeout` | float | 30.0 | Timeout for HTTP requests in seconds |
| `verify_ssl` | bool | False | Whether to verify SSL certificates |

## Example

```python
from unraid_api import UnraidClient

# Create a client
client = UnraidClient(
    host="192.168.1.10",
    api_key="your-api-key",
    port=443,
    use_ssl=True,
    timeout=30.0,
    verify_ssl=False,
)

# Use the client to interact with the Unraid server
system_info = client.info.get_system_info()
print(f"Unraid version: {system_info.get('os', {}).get('release')}")
```

## Next Steps

Explore the documentation for each resource to learn more about the available methods and how to use them.
