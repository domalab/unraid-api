---
title: Real-time Subscriptions
description: Working with real-time data subscriptions in the Unraid API
---

# Real-time Subscriptions

The Unraid API supports real-time subscriptions to various resources, allowing you to monitor for changes and receive updates as they occur. This is especially useful for building dashboards, monitoring systems, or applications that need to react to changes on your Unraid server.

!!! note
    Real-time subscriptions are only available with the asynchronous client (`AsyncUnraidClient`).

## How Subscriptions Work

Subscriptions use GraphQL subscriptions over WebSockets to establish a persistent connection with the Unraid server. When changes occur to the subscribed resource, the server pushes updates to the client automatically.

The library handles the WebSocket connection management, authentication, and message parsing, providing you with a simple async generator interface.

## Basic Usage

Here's a simple example of subscribing to Docker container updates:

```python
import asyncio
from unraid_api import AsyncUnraidClient

async def monitor_containers():
    client = AsyncUnraidClient("192.168.1.10", api_key="your-api-key")
    
    # Subscribe to container updates
    async for container in client.docker.subscribe_to_containers():
        print(f"Container update: {container.name} is now {container.status}")
        
        # React to specific status changes
        if container.status == "running":
            print(f"Container {container.name} has started!")
        elif container.status == "stopped":
            print(f"Container {container.name} has stopped!")

asyncio.run(monitor_containers())
```

## Available Subscriptions

### Docker Containers

```python
async def monitor_docker():
    async for container in client.docker.subscribe_to_containers():
        print(f"Container: {container.name}, Status: {container.status}")
```

### Virtual Machines

```python
async def monitor_vms():
    async for vm in client.vm.subscribe_to_vms():
        print(f"VM: {vm.name}, Status: {vm.status}")
```

### Array Status

```python
async def monitor_array():
    async for status in client.array.subscribe_to_array_status():
        print(f"Array status: {status.status}")
        if status.parity_check_progress is not None:
            print(f"Parity check: {status.parity_check_progress:.2f}%")
```

### System Resources

```python
async def monitor_system_resources():
    async for resources in client.system.subscribe_to_system_resources():
        print(f"CPU: {resources.cpu.usage_percent}%")
        print(f"Memory: {resources.memory.used / resources.memory.total * 100:.2f}%")
```

### Notifications

```python
async def monitor_notifications():
    async for notification in client.notification.subscribe_to_notifications():
        print(f"New notification: {notification.title}")
        print(f"Message: {notification.message}")
```

## Handling Connection Issues

The library automatically handles reconnection attempts if the WebSocket connection is interrupted. However, you might want to implement additional error handling in your application:

```python
import asyncio
from unraid_api import AsyncUnraidClient
from unraid_api.exceptions import ConnectionError, AuthenticationError

async def monitor_with_error_handling():
    client = AsyncUnraidClient("192.168.1.10", api_key="your-api-key")
    
    while True:
        try:
            async for container in client.docker.subscribe_to_containers():
                print(f"Container update: {container.name} is now {container.status}")
        except ConnectionError as e:
            print(f"Connection error: {e}")
            print("Retrying in 5 seconds...")
            await asyncio.sleep(5)  # Wait before retrying
        except AuthenticationError as e:
            print(f"Authentication error: {e}")
            break  # Exit the loop on authentication error
        except Exception as e:
            print(f"Unexpected error: {e}")
            await asyncio.sleep(10)  # Wait longer for other errors

asyncio.run(monitor_with_error_handling())
```

## Canceling Subscriptions

To cancel a subscription, you can simply break out of the async for loop or cancel the task running the subscription:

```python
import asyncio
from unraid_api import AsyncUnraidClient

async def main():
    client = AsyncUnraidClient("192.168.1.10", api_key="your-api-key")
    
    # Create a task for the subscription
    monitor_task = asyncio.create_task(monitor_containers(client))
    
    # Run for 60 seconds then cancel
    await asyncio.sleep(60)
    monitor_task.cancel()
    
    try:
        await monitor_task
    except asyncio.CancelledError:
        print("Monitoring canceled")

async def monitor_containers(client):
    async for container in client.docker.subscribe_to_containers():
        print(f"Container update: {container.name} is now {container.status}")

asyncio.run(main())
```

## Multiple Subscriptions

You can run multiple subscriptions concurrently:

```python
import asyncio
from unraid_api import AsyncUnraidClient

async def main():
    client = AsyncUnraidClient("192.168.1.10", api_key="your-api-key")
    
    # Run all monitors concurrently
    await asyncio.gather(
        monitor_containers(client),
        monitor_vms(client),
        monitor_array(client)
    )

async def monitor_containers(client):
    async for container in client.docker.subscribe_to_containers():
        print(f"Container: {container.name}, Status: {container.status}")

async def monitor_vms(client):
    async for vm in client.vm.subscribe_to_vms():
        print(f"VM: {vm.name}, Status: {vm.status}")

async def monitor_array(client):
    async for status in client.array.subscribe_to_array_status():
        print(f"Array status: {status.status}")

asyncio.run(main())
```

## Subscription Timeouts

By default, subscriptions will attempt to stay connected indefinitely. You can set a timeout for the subscription by using `asyncio.wait_for`:

```python
import asyncio
from unraid_api import AsyncUnraidClient
from asyncio import TimeoutError

async def main():
    client = AsyncUnraidClient("192.168.1.10", api_key="your-api-key")
    
    try:
        # Run the subscription with a 5-minute timeout
        await asyncio.wait_for(monitor_containers(client), timeout=300)
    except TimeoutError:
        print("Subscription timed out after 5 minutes")

async def monitor_containers(client):
    async for container in client.docker.subscribe_to_containers():
        print(f"Container: {container.name}, Status: {container.status}")

asyncio.run(main())
``` 