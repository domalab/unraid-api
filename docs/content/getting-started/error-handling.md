---
layout: default
title: Error Handling
parent: Getting Started
nav_order: 4
---

# Error Handling

The Unraid API library provides comprehensive error handling to help you diagnose and resolve issues. This guide covers the different types of errors you might encounter and how to handle them.

## Exception Types

The library defines several exception types to help you identify and handle specific error conditions:

| Exception Type | Description |
|----------------|-------------|
| `APIError` | Base exception for all API errors |
| `AuthenticationError` | Raised when authentication fails |
| `ConnectionError` | Raised when the server cannot be reached |
| `GraphQLError` | Raised when a GraphQL error occurs |
| `OperationError` | Raised when an operation fails |

## Basic Error Handling

Here's a basic example of how to handle errors:

```python
from unraid_api import UnraidClient
from unraid_api.exceptions import (
    APIError,
    AuthenticationError,
    ConnectionError,
    GraphQLError,
    OperationError,
)

try:
    # Connect to Unraid server
    client = UnraidClient("192.168.1.10", api_key="your-api-key")
    
    # Perform an operation
    system_info = client.info.get_system_info()
    
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
    # Handle authentication error (e.g., prompt for a new API key)
    
except ConnectionError as e:
    print(f"Connection error: {e}")
    # Handle connection error (e.g., check network, server status)
    
except GraphQLError as e:
    print(f"GraphQL error: {e}")
    # Handle GraphQL error (e.g., invalid query)
    
except OperationError as e:
    print(f"Operation failed: {e}")
    # Handle operation error (e.g., array already started)
    
except APIError as e:
    print(f"API error: {e}")
    # Handle other API errors
```

## Handling Specific Operations

Different operations may require specific error handling. Here are some examples:

### Starting the Array

```python
try:
    client.array.start_array()
    print("Array started successfully")
except OperationError as e:
    if "already started" in str(e).lower():
        print("Array is already started")
    else:
        print(f"Failed to start array: {e}")
```

### Managing Docker Containers

```python
try:
    client.docker.start_container("container_id")
    print("Container started successfully")
except OperationError as e:
    if "already running" in str(e).lower():
        print("Container is already running")
    else:
        print(f"Failed to start container: {e}")
```

## Asynchronous Error Handling

When using the asynchronous client, error handling works the same way:

```python
import asyncio
from unraid_api import AsyncUnraidClient
from unraid_api.exceptions import (
    APIError,
    AuthenticationError,
    ConnectionError,
    GraphQLError,
    OperationError,
)

async def main():
    try:
        # Connect to Unraid server
        client = AsyncUnraidClient("192.168.1.10", api_key="your-api-key")
        
        # Perform an operation
        system_info = await client.info.get_system_info()
        
    except AuthenticationError as e:
        print(f"Authentication failed: {e}")
        
    except ConnectionError as e:
        print(f"Connection error: {e}")
        
    except GraphQLError as e:
        print(f"GraphQL error: {e}")
        
    except OperationError as e:
        print(f"Operation failed: {e}")
        
    except APIError as e:
        print(f"API error: {e}")

# Run the async function
asyncio.run(main())
```

## Logging

The Unraid API library uses Python's built-in logging module. You can configure logging to get more information about what's happening:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for detailed logs
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

# The library logs to the 'unraid_api' logger
logger = logging.getLogger("unraid_api")
```

## Common Error Scenarios

Here are some common error scenarios and how to handle them:

### Authentication Errors

If you encounter an `AuthenticationError`, check that:
- The API key is correct
- The API key has the necessary permissions
- The API key has not been revoked

### Connection Errors

If you encounter a `ConnectionError`, check that:
- The Unraid server is running
- The server is reachable from your network
- The GraphQL API is enabled on the server
- The port is correct (usually 443 for HTTPS, 80 for HTTP)

### GraphQL Errors

If you encounter a `GraphQLError`, check that:
- The query or mutation is valid
- The variables are correct
- The requested fields exist in the schema

### Operation Errors

If you encounter an `OperationError`, check the error message for details about what went wrong. Common issues include:
- Trying to start an array that's already started
- Trying to stop an array that's already stopped
- Trying to start a VM that's already running
- Trying to stop a VM that's already stopped

## Next Steps

Now that you understand how to handle errors, you can:

1. [Explore the API reference]({{ site.baseurl }}/content/api/overview)
2. [Use the command-line interface]({{ site.baseurl }}/content/cli/overview)
3. [Integrate with Home Assistant]({{ site.baseurl }}/content/home-assistant/overview)
