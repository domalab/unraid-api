---
title: Error Handling
description: Handling errors when using the Unraid API
---

# Error Handling

Proper error handling is crucial when working with the Unraid API to ensure your application can gracefully handle failures and provide meaningful feedback to users.

## Exception Types

The Unraid API defines several exception types that you might encounter:

```python
from unraid_api.exceptions import (
    UnraidAPIError,
    AuthenticationError,
    ConnectionError,
    NotFoundError,
    ValidationError,
    TimeoutError,
    ServerError,
)
```

| Exception | Description |
| --- | --- |
| `UnraidAPIError` | Base exception for all API errors |
| `AuthenticationError` | Raised when authentication fails |
| `ConnectionError` | Raised when connection to the Unraid server fails |
| `NotFoundError` | Raised when a requested resource is not found |
| `ValidationError` | Raised when input validation fails |
| `TimeoutError` | Raised when a request times out |
| `ServerError` | Raised when the Unraid server returns an error |

## Basic Error Handling

Here's a basic example of catching and handling exceptions:

```python
from unraid_api import UnraidClient
from unraid_api.exceptions import UnraidAPIError, AuthenticationError

try:
    client = UnraidClient("http://tower.local", "token123")
    vms = client.vm.get_vms()
except AuthenticationError:
    print("Authentication failed. Please check your API token.")
except UnraidAPIError as e:
    print(f"An API error occurred: {e}")
```

## Handling Specific Errors

For more granular error handling:

```python
from unraid_api import UnraidClient
from unraid_api.exceptions import (
    UnraidAPIError,
    AuthenticationError,
    ConnectionError,
    NotFoundError,
    ValidationError,
    TimeoutError,
    ServerError,
)

try:
    client = UnraidClient("http://tower.local", "token123")
    vm = client.vm.get_vm("non-existent-vm")
except AuthenticationError:
    print("Authentication failed. Please check your API token.")
except ConnectionError:
    print("Could not connect to the Unraid server. Please check network connectivity.")
except NotFoundError:
    print("The VM was not found. Please check the VM ID.")
except ValidationError as e:
    print(f"Validation error: {e}")
except TimeoutError:
    print("The request timed out. The server may be busy.")
except ServerError as e:
    print(f"Server error: {e}")
except UnraidAPIError as e:
    print(f"An unexpected API error occurred: {e}")
```

## Error Information

All exceptions provide detailed information about what went wrong:

```python
try:
    vm = client.vm.get_vm("my-vm")
except UnraidAPIError as e:
    print(f"Status code: {e.status_code}")  # HTTP status code if available
    print(f"Error message: {e.message}")    # Error message
    print(f"Request ID: {e.request_id}")    # Request ID for debugging (if available)
    print(f"Details: {e.details}")          # Additional error details (if available)
```

## Async Error Handling

When using the async client, error handling works the same way with async/await syntax:

```python
import asyncio
from unraid_api import AsyncUnraidClient
from unraid_api.exceptions import UnraidAPIError

async def main():
    try:
        client = AsyncUnraidClient("http://tower.local", "token123")
        vms = await client.vm.get_vms()
    except UnraidAPIError as e:
        print(f"An API error occurred: {e}")

asyncio.run(main())
```

## Custom Error Handling

You can create a custom error handler function for reusability:

```python
def handle_api_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AuthenticationError:
            print("Authentication failed. Please check your API token.")
        except ConnectionError:
            print("Could not connect to the Unraid server.")
        except NotFoundError:
            print("The requested resource was not found.")
        except ValidationError as e:
            print(f"Validation error: {e}")
        except TimeoutError:
            print("The request timed out.")
        except ServerError as e:
            print(f"Server error: {e}")
        except UnraidAPIError as e:
            print(f"An unexpected API error occurred: {e}")
        return None
    return wrapper

@handle_api_error
def get_all_vms(client):
    return client.vm.get_vms()

# Usage
client = UnraidClient("http://tower.local", "token123")
vms = get_all_vms(client)
if vms:
    print(f"Found {len(vms)} VMs")
```

## Retry Logic

For transient errors, you might want to implement retry logic:

```python
import time
from unraid_api import UnraidClient
from unraid_api.exceptions import ConnectionError, TimeoutError

def with_retries(max_retries=3, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    retries += 1
                    if retries == max_retries:
                        raise
                    print(f"Attempt {retries} failed. Retrying in {delay} seconds...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@with_retries(max_retries=3, delay=2)
def start_vm(client, vm_id):
    return client.vm.start_vm(vm_id)

# Usage
client = UnraidClient("http://tower.local", "token123")
result = start_vm(client, "windows10")
```

## Best Practices

1. **Always handle exceptions**: Don't let API exceptions crash your application.
2. **Be specific**: Catch specific exceptions first, then broader ones.
3. **Log errors**: Log detailed error information for debugging.
4. **Implement retries**: Use retry logic for transient failures.
5. **Provide feedback**: Give clear error messages to users.
6. **Check status**: Verify the success of operations that return a boolean result.

By implementing proper error handling, you'll create a more robust application that provides a better user experience, even when things go wrong. 