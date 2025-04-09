---
layout: default
title: System Information
parent: API Reference
nav_order: 1
---

# System Information

The `info` resource provides methods for retrieving information about the Unraid server.

## Methods

### get_system_info

Get system information.

<div class="api-method">
  <div class="method-signature">
    get_system_info() -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <p>None</p>
  </div>

  <div class="returns">
    <h4>Returns</h4>
    <p>A dictionary containing system information with the following structure:</p>
    <ul>
      <li><code>os</code>: Operating system information
        <ul>
          <li><code>platform</code>: Platform (e.g., "linux")</li>
          <li><code>distro</code>: Distribution (e.g., "Unraid")</li>
          <li><code>release</code>: Release version (e.g., "7.0 x86_64")</li>
          <li><code>kernel</code>: Kernel version</li>
          <li><code>uptime</code>: System uptime in seconds</li>
        </ul>
      </li>
      <li><code>cpu</code>: CPU information
        <ul>
          <li><code>manufacturer</code>: CPU manufacturer (e.g., "Intel")</li>
          <li><code>brand</code>: CPU brand (e.g., "Core™ i7-8700K")</li>
          <li><code>cores</code>: Number of physical cores</li>
          <li><code>threads</code>: Number of threads</li>
        </ul>
      </li>
      <li><code>memory</code>: Memory information
        <ul>
          <li><code>total</code>: Total memory in bytes</li>
          <li><code>free</code>: Free memory in bytes</li>
          <li><code>used</code>: Used memory in bytes</li>
        </ul>
      </li>
      <li><code>system</code>: System information
        <ul>
          <li><code>manufacturer</code>: System manufacturer</li>
          <li><code>model</code>: System model</li>
        </ul>
      </li>
    </ul>
  </div>

  <div class="example">
    <h4>Example</h4>
    <pre><code class="language-python">
# Get system information
system_info = client.info.get_system_info()

# Access specific information
os_info = system_info.get("os", {})
cpu_info = system_info.get("cpu", {})
memory_info = system_info.get("memory", {})
system_details = system_info.get("system", {})

# Print system information
print(f"OS: {os_info.get('distro')} {os_info.get('release')}")
print(f"Kernel: {os_info.get('kernel')}")
print(f"Uptime: {os_info.get('uptime')}")
print(f"CPU: {cpu_info.get('brand')} ({cpu_info.get('cores')} cores, {cpu_info.get('threads')} threads)")
print(f"Memory: {memory_info.get('total') / (1024**3):.2f} GB total, {memory_info.get('used') / (1024**3):.2f} GB used")
print(f"System: {system_details.get('manufacturer')} {system_details.get('model')}")
    </code></pre>
  </div>
</div>

### reboot

Reboot the Unraid server.

<div class="api-method">
  <div class="method-signature">
    reboot() -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <p>None</p>
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
    result = client.info.reboot()
    print(f"Reboot initiated: {result.get('message')}")
except Exception as e:
    print(f"Failed to reboot: {e}")
    </code></pre>
  </div>
</div>

### shutdown

Shutdown the Unraid server.

<div class="api-method">
  <div class="method-signature">
    shutdown() -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <p>None</p>
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
    result = client.info.shutdown()
    print(f"Shutdown initiated: {result.get('message')}")
except Exception as e:
    print(f"Failed to shutdown: {e}")
    </code></pre>
  </div>
</div>

### get_spindown_delay

Get the spindown delay setting.

<div class="api-method">
  <div class="method-signature">
    get_spindown_delay() -> str
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <p>None</p>
  </div>

  <div class="returns">
    <h4>Returns</h4>
    <p>The spindown delay in minutes as a string.</p>
  </div>

  <div class="example">
    <h4>Example</h4>
    <pre><code class="language-python">
# Get spindown delay
spindown_delay = client.info.get_spindown_delay()
print(f"Spindown delay: {spindown_delay} minutes")
    </code></pre>
  </div>
</div>

### get_docker_info

Get Docker information.

<div class="api-method">
  <div class="method-signature">
    get_docker_info() -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <p>None</p>
  </div>

  <div class="returns">
    <h4>Returns</h4>
    <p>A dictionary containing Docker information with the following structure:</p>
    <ul>
      <li><code>enabled</code>: Whether Docker is enabled</li>
      <li><code>version</code>: Docker version</li>
      <li><code>status</code>: Docker service status</li>
      <li><code>rootPath</code>: Docker root path</li>
      <li><code>configPath</code>: Docker configuration path</li>
      <li><code>imagePath</code>: Docker image path</li>
      <li><code>autostart</code>: Whether Docker autostart is enabled</li>
      <li><code>networkDefault</code>: Default Docker network</li>
      <li><code>customNetworks</code>: Custom Docker networks</li>
      <li><code>privileged</code>: Whether privileged mode is enabled</li>
      <li><code>logRotation</code>: Log rotation settings</li>
    </ul>
  </div>

  <div class="example">
    <h4>Example</h4>
    <pre><code class="language-python">
# Get Docker information
docker_info = client.info.get_docker_info()
print(f"Docker enabled: {docker_info.get('enabled')}")
print(f"Docker version: {docker_info.get('version')}")
print(f"Docker status: {docker_info.get('status')}")
    </code></pre>
  </div>
</div>

### get_vm_info

Get VM information.

<div class="api-method">
  <div class="method-signature">
    get_vm_info() -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <p>None</p>
  </div>

  <div class="returns">
    <h4>Returns</h4>
    <p>A dictionary containing VM information with the following structure:</p>
    <ul>
      <li><code>enabled</code>: Whether VMs are enabled</li>
      <li><code>version</code>: VM service version</li>
      <li><code>status</code>: VM service status</li>
      <li><code>corePath</code>: VM core path</li>
      <li><code>configPath</code>: VM configuration path</li>
      <li><code>imagePath</code>: VM image path</li>
      <li><code>autostart</code>: Whether VM autostart is enabled</li>
      <li><code>winVmCount</code>: Number of Windows VMs</li>
      <li><code>linuxVmCount</code>: Number of Linux VMs</li>
      <li><code>otherVmCount</code>: Number of other VMs</li>
      <li><code>CPUisolatedCores</code>: CPU cores isolated for VMs</li>
      <li><code>PCIeiommuGroups</code>: PCIe IOMMU groups</li>
    </ul>
  </div>

  <div class="example">
    <h4>Example</h4>
    <pre><code class="language-python">
# Get VM information
vm_info = client.info.get_vm_info()
print(f"VMs enabled: {vm_info.get('enabled')}")
print(f"VM version: {vm_info.get('version')}")
print(f"VM status: {vm_info.get('status')}")
print(f"Windows VMs: {vm_info.get('winVmCount')}")
print(f"Linux VMs: {vm_info.get('linuxVmCount')}")
print(f"Other VMs: {vm_info.get('otherVmCount')}")
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
    
    # Get system information
    system_info = await client.info.get_system_info()
    print(f"Unraid version: {system_info.get('os', {}).get('release')}")

asyncio.run(main())
```
