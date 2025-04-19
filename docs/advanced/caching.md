---
title: Caching
description: Using the caching features of the Unraid API
---

# Caching

The Unraid API client includes a caching system to improve performance and reduce the load on your Unraid server. This guide explains how to use and configure caching effectively.

## Why Use Caching?

Caching provides several benefits:

1. **Reduced Server Load**: Fewer API calls to your Unraid server
2. **Improved Performance**: Faster response times for repeated requests
3. **Enhanced User Experience**: More responsive applications
4. **Reduced Network Traffic**: Less data transferred over the network
5. **Consistent Data**: Option to use cached data during network issues

## Default Caching Behavior

By default, the Unraid API client uses a simple in-memory cache with the following settings:

- Basic "GET" operations are cached for 30 seconds
- Mutation operations (changes that modify data) bypass the cache and invalidate related cached data
- Cache is disabled for real-time subscriptions

## Configuring Cache Options

You can customize caching behavior when creating a client:

```python
from unraid_api import UnraidClient

# Default caching (in-memory, 30-second TTL)
client = UnraidClient("http://tower.local", "token123")

# Disable caching entirely
client = UnraidClient(
    "http://tower.local", 
    "token123", 
    cache_enabled=False
)

# Custom cache TTL (time-to-live) in seconds
client = UnraidClient(
    "http://tower.local", 
    "token123", 
    cache_ttl=60  # Cache for 60 seconds
)
```

## Advanced Caching Configuration

For more advanced caching needs, you can specify different cache durations for different types of resources:

```python
from unraid_api import UnraidClient

client = UnraidClient(
    "http://tower.local",
    "token123",
    cache_config={
        "default": 30,         # Default TTL for all resources
        "system_info": 300,    # Cache system info for 5 minutes
        "vm_list": 60,         # Cache VM lists for 1 minute
        "disk_status": 120,    # Cache disk status for 2 minutes
        "docker_containers": 45 # Cache container lists for 45 seconds
    }
)
```

## Custom Cache Backends

You can provide a custom cache implementation by implementing the `CacheBackend` interface:

```python
from unraid_api import UnraidClient
from unraid_api.cache import CacheBackend
import redis

class RedisCacheBackend(CacheBackend):
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def get(self, key):
        value = self.redis.get(key)
        if value:
            return json.loads(value)
        return None
    
    def set(self, key, value, ttl=None):
        self.redis.set(key, json.dumps(value), ex=ttl)
    
    def delete(self, key):
        self.redis.delete(key)
    
    def clear(self):
        # Clear only keys related to this application
        for key in self.redis.keys("unraid_api:*"):
            self.redis.delete(key)

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Create client with Redis cache backend
client = UnraidClient(
    "http://tower.local",
    "token123",
    cache_backend=RedisCacheBackend(redis_client)
)
```

## Selectively Bypassing Cache

You can bypass the cache for specific operations when needed:

```python
# Normal cached request
vms = client.vm.get_vms()

# Force a fresh request bypassing cache
vms = client.vm.get_vms(bypass_cache=True)

# For methods that don't have an explicit bypass_cache parameter
client.cache.disable()
vms = client.vm.get_vms()
client.cache.enable()
```

## Clearing the Cache

You can manually clear the cache when needed:

```python
# Clear entire cache
client.cache.clear()

# Clear cache for a specific resource type
client.cache.clear_resource_type("vm")

# Clear cache for a specific item
client.cache.clear_item("vm", "windows10")
```

## Cache Invalidation

The client automatically invalidates related cached data when you perform mutation operations. For example:

```python
# This data gets cached
vms = client.vm.get_vms()

# This invalidates the cached VM data
client.vm.start_vm("windows10")

# This will make a fresh request because the cache was invalidated
vms = client.vm.get_vms()
```

## Async Support

Caching works the same way with the async client:

```python
import asyncio
from unraid_api import AsyncUnraidClient

async def main():
    client = AsyncUnraidClient(
        "http://tower.local",
        "token123",
        cache_ttl=60
    )
    
    # First call fetches and caches
    vms = await client.vm.get_vms()
    
    # Second call uses cache
    vms_again = await client.vm.get_vms()
    
    # Force fresh data
    vms_fresh = await client.vm.get_vms(bypass_cache=True)

asyncio.run(main())
```

## Debugging Cache Behavior

You can enable cache debugging to see when cache hits and misses occur:

```python
from unraid_api import UnraidClient
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create client with cache debugging
client = UnraidClient(
    "http://tower.local",
    "token123",
    cache_debug=True
)

# This will log cache activity
vms = client.vm.get_vms()  # Cache miss (logged)
vms = client.vm.get_vms()  # Cache hit (logged)
```

## Caching Strategies

Here are some strategies for effective caching:

1. **Static Data**: Use longer TTLs for rarely changing data like system information
2. **Dynamic Data**: Use shorter TTLs for frequently changing data like VM status
3. **Critical Operations**: Bypass cache for operations where real-time data is crucial
4. **User Preferences**: Provide users with options to control caching behavior
5. **Stale-While-Revalidate**: Consider implementing a pattern where stale data is shown while fresh data is fetched

## Performance Considerations

- Memory usage increases with cache size - consider using an external cache for large datasets
- Very short TTLs may negate the benefits of caching
- Very long TTLs may result in stale data
- Consider application needs when tuning cache parameters

By effectively using the caching system, you can create more responsive and efficient applications that interact with your Unraid server. 