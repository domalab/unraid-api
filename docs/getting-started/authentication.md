---
title: Authentication
description: How to authenticate with the Unraid API
---

# Authentication

The `unraid-api` library uses API key authentication to securely connect to your Unraid server. This page will guide you through the authentication process.

## Prerequisites

Before you can authenticate:

1. You must have [installed the library](installation.md)
2. You must have [enabled the GraphQL API and created an API key](installation.md#creating-an-api-key) on your Unraid server

## Basic Authentication

The simplest way to authenticate is to provide your server's IP address and API key when creating a client:

```python
from unraid_api import UnraidClient

# Create a client with API key authentication
client = UnraidClient(
    server="192.168.1.10",  # Replace with your Unraid server IP or hostname
    api_key="your-api-key"  # Replace with your generated API key
)

# Test connection
system_info = client.get_system_info()
print(f"Connected to Unraid server version: {system_info.version}")
```

## Handling Connection Redirects

Unraid servers often redirect to myunraid.net domains. The client automatically handles these redirects, but you can customize this behavior:

```python
from unraid_api import UnraidClient

# Create a client with custom redirect handling
client = UnraidClient(
    server="192.168.1.10",
    api_key="your-api-key",
    follow_redirects=True,  # Default is True
    max_redirects=5         # Default is 5
)
```

## Async Authentication

For asynchronous applications, use the `AsyncUnraidClient` class:

```python
import asyncio
from unraid_api import AsyncUnraidClient

async def main():
    # Create an async client
    client = AsyncUnraidClient(
        server="192.168.1.10",
        api_key="your-api-key"
    )
    
    # Test connection
    system_info = await client.get_system_info()
    print(f"Connected to Unraid server version: {system_info.version}")

# Run the async function
asyncio.run(main())
```

## Advanced Configuration

### Timeout Configuration

You can configure the connection and request timeouts:

```python
from unraid_api import UnraidClient

client = UnraidClient(
    server="192.168.1.10",
    api_key="your-api-key",
    timeout=30  # Timeout in seconds (default is 10)
)
```

### SSL/TLS Configuration

If your Unraid server uses HTTPS, you can configure SSL verification:

```python
from unraid_api import UnraidClient

client = UnraidClient(
    server="192.168.1.10",
    api_key="your-api-key",
    ssl_verify=True  # Verify SSL certificates (default is True)
)
```

To connect to a server with a self-signed certificate, you can disable verification (not recommended for production):

```python
client = UnraidClient(
    server="192.168.1.10",
    api_key="your-api-key",
    ssl_verify=False  # Disable SSL verification
)
```

## Error Handling

The client provides detailed error information for authentication failures:

```python
from unraid_api import UnraidClient
from unraid_api.exceptions import AuthenticationError, ConnectionError

try:
    client = UnraidClient("192.168.1.10", api_key="invalid-key")
    system_info = client.get_system_info()
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except ConnectionError as e:
    print(f"Connection error: {e}")
```

## Next Steps

Now that you've successfully authenticated with your Unraid server, you can proceed to the [Quick Start](quick-start.md) section to learn how to perform common operations. 