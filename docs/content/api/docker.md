---
layout: default
title: Docker Containers
parent: API Reference
nav_order: 4
---

# Docker Containers

The `docker` resource provides methods for managing Docker containers on the Unraid server.

## Methods

### get_containers

Get a list of all Docker containers.

<div class="api-method">
  <div class="method-signature">
    get_containers() -> List[Dict[str, Any]]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <p>None</p>
  </div>

  <div class="returns">
    <h4>Returns</h4>
    <p>A list of dictionaries, each containing information about a Docker container with the following structure:</p>
    <ul>
      <li><code>id</code>: Container ID</li>
      <li><code>names</code>: List of container names</li>
      <li><code>image</code>: Container image</li>
      <li><code>imageID</code>: Image ID</li>
      <li><code>command</code>: Command</li>
      <li><code>created</code>: Creation timestamp</li>
      <li><code>state</code>: Container state (e.g., "running", "exited")</li>
      <li><code>status</code>: Container status</li>
      <li><code>ports</code>: Exposed ports</li>
      <li><code>labels</code>: Container labels</li>
      <li><code>mounts</code>: Container mounts</li>
      <li><code>networkSettings</code>: Network settings</li>
    </ul>
  </div>

  <div class="example">
    <h4>Example</h4>
    <pre><code class="language-python">
# Get all Docker containers
containers = client.docker.get_containers()
for container in containers:
    print(f"Container: {container.get('names')[0]}")
    print(f"  ID: {container.get('id')}")
    print(f"  Image: {container.get('image')}")
    print(f"  State: {container.get('state')}")
    print(f"  Status: {container.get('status')}")
    </code></pre>
  </div>
</div>

### get_container

Get information about a specific Docker container.

<div class="api-method">
  <div class="method-signature">
    get_container(container_id: str) -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <ul>
      <li><code>container_id</code>: The ID of the container</li>
    </ul>
  </div>

  <div class="returns">
    <h4>Returns</h4>
    <p>A dictionary containing information about the container with the same structure as in <code>get_containers</code>.</p>
  </div>

  <div class="example">
    <h4>Example</h4>
    <pre><code class="language-python">
# Get information about a specific container
container = client.docker.get_container("container_id")
print(f"Container: {container.get('names')[0]}")
print(f"State: {container.get('state')}")
print(f"Status: {container.get('status')}")
    </code></pre>
  </div>
</div>

### start_container

Start a Docker container.

<div class="api-method">
  <div class="method-signature">
    start_container(container_id: str) -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <ul>
      <li><code>container_id</code>: The ID of the container to start</li>
    </ul>
  </div>

  <div class="returns">
    <h4>Returns</h4>
    <p>A dictionary containing the result of the operation:</p>
    <ul>
      <li><code>success</code>: Whether the operation was successful</li>
      <li><code>message</code>: A message describing the result</li>
    </ul>
  </div>

  <div class="example">
    <h4>Example</h4>
    <pre><code class="language-python">
try:
    result = client.docker.start_container("container_id")
    print(f"Container started: {result.get('message')}")
except Exception as e:
    print(f"Failed to start container: {e}")
    </code></pre>
  </div>
</div>

### stop_container

Stop a Docker container.

<div class="api-method">
  <div class="method-signature">
    stop_container(container_id: str) -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <ul>
      <li><code>container_id</code>: The ID of the container to stop</li>
    </ul>
  </div>

  <div class="returns">
    <h4>Returns</h4>
    <p>A dictionary containing the result of the operation:</p>
    <ul>
      <li><code>success</code>: Whether the operation was successful</li>
      <li><code>message</code>: A message describing the result</li>
    </ul>
  </div>

  <div class="example">
    <h4>Example</h4>
    <pre><code class="language-python">
try:
    result = client.docker.stop_container("container_id")
    print(f"Container stopped: {result.get('message')}")
except Exception as e:
    print(f"Failed to stop container: {e}")
    </code></pre>
  </div>
</div>

### restart_container

Restart a Docker container.

<div class="api-method">
  <div class="method-signature">
    restart_container(container_id: str) -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <ul>
      <li><code>container_id</code>: The ID of the container to restart</li>
    </ul>
  </div>

  <div class="returns">
    <h4>Returns</h4>
    <p>A dictionary containing the result of the operation:</p>
    <ul>
      <li><code>success</code>: Whether the operation was successful</li>
      <li><code>message</code>: A message describing the result</li>
    </ul>
  </div>

  <div class="example">
    <h4>Example</h4>
    <pre><code class="language-python">
try:
    result = client.docker.restart_container("container_id")
    print(f"Container restarted: {result.get('message')}")
except Exception as e:
    print(f"Failed to restart container: {e}")
    </code></pre>
  </div>
</div>

### remove_container

Remove a Docker container.

<div class="api-method">
  <div class="method-signature">
    remove_container(container_id: str, force: bool = False) -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <ul>
      <li><code>container_id</code>: The ID of the container to remove</li>
      <li><code>force</code>: Whether to force removal (default: False)</li>
    </ul>
  </div>

  <div class="returns">
    <h4>Returns</h4>
    <p>A dictionary containing the result of the operation:</p>
    <ul>
      <li><code>success</code>: Whether the operation was successful</li>
      <li><code>message</code>: A message describing the result</li>
    </ul>
  </div>

  <div class="example">
    <h4>Example</h4>
    <pre><code class="language-python">
try:
    # Remove a container
    result = client.docker.remove_container("container_id")
    print(f"Container removed: {result.get('message')}")
    
    # Force remove a container
    result = client.docker.remove_container("container_id", force=True)
    print(f"Container force removed: {result.get('message')}")
except Exception as e:
    print(f"Failed to remove container: {e}")
    </code></pre>
  </div>
</div>

### get_container_logs

Get logs for a Docker container.

<div class="api-method">
  <div class="method-signature">
    get_container_logs(container_id: str, tail: int = 100) -> str
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <ul>
      <li><code>container_id</code>: The ID of the container</li>
      <li><code>tail</code>: Number of lines to return from the end of the logs (default: 100)</li>
    </ul>
  </div>

  <div class="returns">
    <h4>Returns</h4>
    <p>A string containing the container logs.</p>
  </div>

  <div class="example">
    <h4>Example</h4>
    <pre><code class="language-python">
# Get logs for a container
logs = client.docker.get_container_logs("container_id")
print(logs)

# Get the last 10 lines of logs
logs = client.docker.get_container_logs("container_id", tail=10)
print(logs)
    </code></pre>
  </div>
</div>

### get_container_stats

Get statistics for a Docker container.

<div class="api-method">
  <div class="method-signature">
    get_container_stats(container_id: str) -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <ul>
      <li><code>container_id</code>: The ID of the container</li>
    </ul>
  </div>

  <div class="returns">
    <h4>Returns</h4>
    <p>A dictionary containing statistics for the container with the following structure:</p>
    <ul>
      <li><code>cpu</code>: CPU usage statistics</li>
      <li><code>memory</code>: Memory usage statistics</li>
      <li><code>network</code>: Network usage statistics</li>
      <li><code>blockIO</code>: Block I/O statistics</li>
    </ul>
  </div>

  <div class="example">
    <h4>Example</h4>
    <pre><code class="language-python">
# Get statistics for a container
stats = client.docker.get_container_stats("container_id")
print(f"CPU usage: {stats.get('cpu', {}).get('usage')}%")
print(f"Memory usage: {stats.get('memory', {}).get('usage')} / {stats.get('memory', {}).get('limit')} bytes")
print(f"Network RX: {stats.get('network', {}).get('rx_bytes')} bytes")
print(f"Network TX: {stats.get('network', {}).get('tx_bytes')} bytes")
    </code></pre>
  </div>
</div>

## Asynchronous Usage

All methods are also available in the asynchronous client:

```python
import asyncio
from unraid_api import AsyncUnraidClient

async def main():
    client = AsyncUnraidClient("192.168.1.10", api_key="your-api-key")
    
    # Get all Docker containers
    containers = await client.docker.get_containers()
    for container in containers:
        print(f"Container: {container.get('names')[0]} ({container.get('state')})")

asyncio.run(main())
```
