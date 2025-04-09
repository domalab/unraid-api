---
layout: default
title: Virtual Machines
parent: API Reference
nav_order: 5
---

# Virtual Machines

The `vm` resource provides methods for managing virtual machines on the Unraid server.

## Methods

### get_vms

Get a list of all virtual machines.

<div class="api-method">
  <div class="method-signature">
    get_vms() -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <p>None</p>
  </div>

  <div class="returns">
    <h4>Returns</h4>
    <p>A dictionary containing information about virtual machines with the following structure:</p>
    <ul>
      <li><code>domain</code>: List of virtual machines
        <ul>
          <li><code>uuid</code>: VM UUID</li>
          <li><code>name</code>: VM name</li>
          <li><code>state</code>: VM state (e.g., "RUNNING", "SHUTOFF")</li>
          <li><code>memory</code>: Memory allocation in bytes</li>
          <li><code>vcpus</code>: Number of virtual CPUs</li>
          <li><code>autostart</code>: Whether autostart is enabled</li>
          <li><code>persistent</code>: Whether the VM is persistent</li>
          <li><code>devices</code>: List of devices attached to the VM</li>
        </ul>
      </li>
    </ul>
  </div>

  <div class="example">
    <h4>Example</h4>
    <pre><code class="language-python">
# Get all virtual machines
vms = client.vm.get_vms()
for vm in vms.get('domain', []):
    print(f"VM: {vm.get('name')}")
    print(f"  UUID: {vm.get('uuid')}")
    print(f"  State: {vm.get('state')}")
    print(f"  Memory: {vm.get('memory') / (1024**2):.2f} MB")
    print(f"  vCPUs: {vm.get('vcpus')}")
    print(f"  Autostart: {vm.get('autostart')}")
    </code></pre>
  </div>
</div>

### get_vm

Get information about a specific virtual machine.

<div class="api-method">
  <div class="method-signature">
    get_vm(vm_uuid: str) -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <ul>
      <li><code>vm_uuid</code>: The UUID of the virtual machine</li>
    </ul>
  </div>

  <div class="returns">
    <h4>Returns</h4>
    <p>A dictionary containing information about the virtual machine with the same structure as in <code>get_vms</code>.</p>
  </div>

  <div class="example">
    <h4>Example</h4>
    <pre><code class="language-python">
# Get information about a specific VM
vm = client.vm.get_vm("vm_uuid")
print(f"VM: {vm.get('name')}")
print(f"State: {vm.get('state')}")
print(f"Memory: {vm.get('memory') / (1024**2):.2f} MB")
print(f"vCPUs: {vm.get('vcpus')}")
    </code></pre>
  </div>
</div>

### start_vm

Start a virtual machine.

<div class="api-method">
  <div class="method-signature">
    start_vm(vm_uuid: str) -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <ul>
      <li><code>vm_uuid</code>: The UUID of the virtual machine to start</li>
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
    result = client.vm.start_vm("vm_uuid")
    print(f"VM started: {result.get('message')}")
except Exception as e:
    print(f"Failed to start VM: {e}")
    </code></pre>
  </div>
</div>

### stop_vm

Stop a virtual machine.

<div class="api-method">
  <div class="method-signature">
    stop_vm(vm_uuid: str, force: bool = False) -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <ul>
      <li><code>vm_uuid</code>: The UUID of the virtual machine to stop</li>
      <li><code>force</code>: Whether to force stop the VM (default: False)</li>
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
    # Gracefully stop a VM
    result = client.vm.stop_vm("vm_uuid")
    print(f"VM stopped: {result.get('message')}")
    
    # Force stop a VM
    result = client.vm.stop_vm("vm_uuid", force=True)
    print(f"VM force stopped: {result.get('message')}")
except Exception as e:
    print(f"Failed to stop VM: {e}")
    </code></pre>
  </div>
</div>

### restart_vm

Restart a virtual machine.

<div class="api-method">
  <div class="method-signature">
    restart_vm(vm_uuid: str) -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <ul>
      <li><code>vm_uuid</code>: The UUID of the virtual machine to restart</li>
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
    result = client.vm.restart_vm("vm_uuid")
    print(f"VM restarted: {result.get('message')}")
except Exception as e:
    print(f"Failed to restart VM: {e}")
    </code></pre>
  </div>
</div>

### pause_vm

Pause a virtual machine.

<div class="api-method">
  <div class="method-signature">
    pause_vm(vm_uuid: str) -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <ul>
      <li><code>vm_uuid</code>: The UUID of the virtual machine to pause</li>
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
    result = client.vm.pause_vm("vm_uuid")
    print(f"VM paused: {result.get('message')}")
except Exception as e:
    print(f"Failed to pause VM: {e}")
    </code></pre>
  </div>
</div>

### resume_vm

Resume a paused virtual machine.

<div class="api-method">
  <div class="method-signature">
    resume_vm(vm_uuid: str) -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <ul>
      <li><code>vm_uuid</code>: The UUID of the virtual machine to resume</li>
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
    result = client.vm.resume_vm("vm_uuid")
    print(f"VM resumed: {result.get('message')}")
except Exception as e:
    print(f"Failed to resume VM: {e}")
    </code></pre>
  </div>
</div>

### get_vm_screenshot

Get a screenshot of a virtual machine.

<div class="api-method">
  <div class="method-signature">
    get_vm_screenshot(vm_uuid: str) -> bytes
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <ul>
      <li><code>vm_uuid</code>: The UUID of the virtual machine</li>
    </ul>
  </div>

  <div class="returns">
    <h4>Returns</h4>
    <p>The screenshot as bytes in PNG format.</p>
  </div>

  <div class="example">
    <h4>Example</h4>
    <pre><code class="language-python">
# Get a screenshot of a VM
screenshot = client.vm.get_vm_screenshot("vm_uuid")

# Save the screenshot to a file
with open("vm_screenshot.png", "wb") as f:
    f.write(screenshot)
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
    
    # Get all virtual machines
    vms = await client.vm.get_vms()
    for vm in vms.get('domain', []):
        print(f"VM: {vm.get('name')} ({vm.get('state')})")

asyncio.run(main())
```
