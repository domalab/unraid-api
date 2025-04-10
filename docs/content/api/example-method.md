---
layout: default
title: Example API Method
parent: API Reference
nav_order: 99
---

# Example API Method

This page demonstrates the API method documentation format.

{% include toc.html html=content %}

## Overview

The Unraid API provides a clean, intuitive interface to Unraid's GraphQL API. This example shows how API methods are documented.

{% include inline-ad.html %}

## Basic Usage

Here's a basic example of using the API:

```python
from unraid_api import UnraidAPI

# Initialize the client
client = UnraidAPI(host="192.168.1.100", api_key="your-api-key")

# Get system information
system_info = client.get_system_info()
print(f"Unraid Version: {system_info.version}")
```

## API Methods

{% include api-method.html 
  title="Get System Information" 
  type="GET"
  description="Retrieves basic system information from the Unraid server."
  parameters=site.data.api_params.system_info
  example="client.get_system_info()"
  response='{
  "version": "6.9.2",
  "title": "Tower",
  "description": "Main Unraid Server",
  "uptime": "10 days, 4 hours, 30 minutes",
  "cpu_usage": 15.2,
  "memory_usage": 45.8
}'
%}

{% include api-method.html 
  title="Get Array Status" 
  type="GET"
  description="Retrieves the current status of the Unraid array."
  parameters=site.data.api_params.array_status
  example="client.get_array_status()"
  response='{
  "status": "Started",
  "protected": true,
  "size": "40 TB",
  "used": "25 TB",
  "free": "15 TB",
  "devices": 8
}'
%}

{% include sidebar-ad.html %}

## Error Handling

The API uses custom exceptions to handle errors:

```python
from unraid_api import UnraidAPI, UnraidConnectionError

try:
    client = UnraidAPI(host="192.168.1.100", api_key="invalid-key")
    system_info = client.get_system_info()
except UnraidConnectionError as e:
    print(f"Connection error: {e}")
```

## Advanced Usage

For more advanced usage, you can use the asynchronous client:

```python
import asyncio
from unraid_api import AsyncUnraidAPI

async def main():
    client = AsyncUnraidAPI(host="192.168.1.100", api_key="your-api-key")
    system_info = await client.get_system_info()
    array_status = await client.get_array_status()
    
    print(f"Unraid Version: {system_info.version}")
    print(f"Array Status: {array_status.status}")
    
    await client.close()

asyncio.run(main())
```

{% include inline-ad.html %}
