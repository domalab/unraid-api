---
layout: default
title: Disk Operations
parent: API Reference
nav_order: 3
---

# Disk Operations

The `disk` resource provides methods for working with disks on the Unraid server.

## Methods

### get_disks

Get a list of all disks.

<div class="api-method">
  <div class="method-signature">
    get_disks() -> List[Dict[str, Any]]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <p>None</p>
  </div>

  <div class="returns">
    <h4>Returns</h4>
    <p>A list of dictionaries, each containing information about a disk with the following structure:</p>
    <ul>
      <li><code>id</code>: Disk ID</li>
      <li><code>name</code>: Disk name</li>
      <li><code>device</code>: Device path</li>
      <li><code>type</code>: Disk type (e.g., "data", "parity", "cache", "flash")</li>
      <li><code>size</code>: Disk size in bytes</li>
      <li><code>used</code>: Used space in bytes</li>
      <li><code>free</code>: Free space in bytes</li>
      <li><code>temperature</code>: Disk temperature in Celsius</li>
      <li><code>status</code>: Disk status</li>
      <li><code>health</code>: Disk health status</li>
      <li><code>mounted</code>: Whether the disk is mounted</li>
      <li><code>spindown</code>: Whether the disk is spun down</li>
      <li><code>filesystem</code>: Filesystem type</li>
    </ul>
  </div>

  <div class="example">
    <h4>Example</h4>
    <pre><code class="language-python">
# Get all disks
disks = client.disk.get_disks()
for disk in disks:
    print(f"Disk: {disk.get('name')} ({disk.get('type')})")
    print(f"  Size: {disk.get('size') / (1024**3):.2f} GB")
    print(f"  Used: {disk.get('used') / (1024**3):.2f} GB")
    print(f"  Free: {disk.get('free') / (1024**3):.2f} GB")
    print(f"  Temperature: {disk.get('temperature')}°C")
    print(f"  Status: {disk.get('status')}")
    print(f"  Health: {disk.get('health')}")
    print(f"  Mounted: {disk.get('mounted')}")
    print(f"  Filesystem: {disk.get('filesystem')}")
    </code></pre>
  </div>
</div>

### get_disk

Get information about a specific disk.

<div class="api-method">
  <div class="method-signature">
    get_disk(disk_id: str) -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <ul>
      <li><code>disk_id</code>: The ID of the disk</li>
    </ul>
  </div>

  <div class="returns">
    <h4>Returns</h4>
    <p>A dictionary containing information about the disk with the same structure as in <code>get_disks</code>.</p>
  </div>

  <div class="example">
    <h4>Example</h4>
    <pre><code class="language-python">
# Get information about a specific disk
disk = client.disk.get_disk("sda")
print(f"Disk: {disk.get('name')} ({disk.get('type')})")
print(f"Size: {disk.get('size') / (1024**3):.2f} GB")
print(f"Temperature: {disk.get('temperature')}°C")
print(f"Status: {disk.get('status')}")
print(f"Health: {disk.get('health')}")
    </code></pre>
  </div>
</div>

### get_disk_smart

Get SMART information for a disk.

<div class="api-method">
  <div class="method-signature">
    get_disk_smart(disk_id: str) -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <ul>
      <li><code>disk_id</code>: The ID of the disk</li>
    </ul>
  </div>

  <div class="returns">
    <h4>Returns</h4>
    <p>A dictionary containing SMART information for the disk with the following structure:</p>
    <ul>
      <li><code>status</code>: SMART status (e.g., "OK", "FAIL")</li>
      <li><code>supported</code>: Whether SMART is supported</li>
      <li><code>enabled</code>: Whether SMART is enabled</li>
      <li><code>temperature</code>: Disk temperature in Celsius</li>
      <li><code>attributes</code>: List of SMART attributes</li>
    </ul>
  </div>

  <div class="example">
    <h4>Example</h4>
    <pre><code class="language-python">
# Get SMART information for a disk
smart_info = client.disk.get_disk_smart("sda")
print(f"SMART status: {smart_info.get('status')}")
print(f"SMART supported: {smart_info.get('supported')}")
print(f"SMART enabled: {smart_info.get('enabled')}")
print(f"Temperature: {smart_info.get('temperature')}°C")

# Print SMART attributes
for attribute in smart_info.get('attributes', []):
    print(f"Attribute: {attribute.get('name')}")
    print(f"  ID: {attribute.get('id')}")
    print(f"  Value: {attribute.get('value')}")
    print(f"  Worst: {attribute.get('worst')}")
    print(f"  Threshold: {attribute.get('threshold')}")
    print(f"  Raw: {attribute.get('raw')}")
    print(f"  Status: {attribute.get('status')}")
    </code></pre>
  </div>
</div>

### mount_disk

Mount a disk.

<div class="api-method">
  <div class="method-signature">
    mount_disk(disk_id: str) -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <ul>
      <li><code>disk_id</code>: The ID of the disk to mount</li>
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
    result = client.disk.mount_disk("sda")
    print(f"Disk mounted: {result.get('message')}")
except Exception as e:
    print(f"Failed to mount disk: {e}")
    </code></pre>
  </div>
</div>

### unmount_disk

Unmount a disk.

<div class="api-method">
  <div class="method-signature">
    unmount_disk(disk_id: str) -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <ul>
      <li><code>disk_id</code>: The ID of the disk to unmount</li>
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
    result = client.disk.unmount_disk("sda")
    print(f"Disk unmounted: {result.get('message')}")
except Exception as e:
    print(f"Failed to unmount disk: {e}")
    </code></pre>
  </div>
</div>

### spindown_disk

Spin down a disk.

<div class="api-method">
  <div class="method-signature">
    spindown_disk(disk_id: str) -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <ul>
      <li><code>disk_id</code>: The ID of the disk to spin down</li>
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
    result = client.disk.spindown_disk("sda")
    print(f"Disk spun down: {result.get('message')}")
except Exception as e:
    print(f"Failed to spin down disk: {e}")
    </code></pre>
  </div>
</div>

### spinup_disk

Spin up a disk.

<div class="api-method">
  <div class="method-signature">
    spinup_disk(disk_id: str) -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <ul>
      <li><code>disk_id</code>: The ID of the disk to spin up</li>
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
    result = client.disk.spinup_disk("sda")
    print(f"Disk spun up: {result.get('message')}")
except Exception as e:
    print(f"Failed to spin up disk: {e}")
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
    
    # Get all disks
    disks = await client.disk.get_disks()
    for disk in disks:
        print(f"Disk: {disk.get('name')} ({disk.get('type')})")

asyncio.run(main())
```
