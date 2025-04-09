---
layout: default
title: Array Management
parent: API Reference
nav_order: 2
---

# Array Management

The `array` resource provides methods for managing the Unraid array.

## Methods

### get_array_status

Get the status of the array.

<div class="api-method">
  <div class="method-signature">
    get_array_status() -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <p>None</p>
  </div>

  <div class="returns">
    <h4>Returns</h4>
    <p>A dictionary containing array status information with the following structure:</p>
    <ul>
      <li><code>state</code>: Array state (e.g., "STARTED", "STOPPED")</li>
      <li><code>size</code>: Array size in bytes</li>
      <li><code>used</code>: Used space in bytes</li>
      <li><code>free</code>: Free space in bytes</li>
      <li><code>devices</code>: List of devices in the array</li>
      <li><code>protected</code>: Whether the array is protected</li>
      <li><code>parityStatus</code>: Parity status information</li>
    </ul>
  </div>

  <div class="example">
    <h4>Example</h4>
    <pre><code class="language-python">
# Get array status
array_status = client.array.get_array_status()
print(f"Array state: {array_status.get('state')}")
print(f"Array size: {array_status.get('size') / (1024**3):.2f} GB")
print(f"Used space: {array_status.get('used') / (1024**3):.2f} GB")
print(f"Free space: {array_status.get('free') / (1024**3):.2f} GB")
print(f"Protected: {array_status.get('protected')}")
    </code></pre>
  </div>
</div>

### start_array

Start the array.

<div class="api-method">
  <div class="method-signature">
    start_array() -> Dict[str, Any]
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
    result = client.array.start_array()
    print(f"Array started: {result.get('message')}")
except Exception as e:
    print(f"Failed to start array: {e}")
    </code></pre>
  </div>
</div>

### stop_array

Stop the array.

<div class="api-method">
  <div class="method-signature">
    stop_array() -> Dict[str, Any]
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
    result = client.array.stop_array()
    print(f"Array stopped: {result.get('message')}")
except Exception as e:
    print(f"Failed to stop array: {e}")
    </code></pre>
  </div>
</div>

### start_parity_check

Start a parity check.

<div class="api-method">
  <div class="method-signature">
    start_parity_check(correcting: bool = True) -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <ul>
      <li><code>correcting</code>: Whether to correct errors (default: True)</li>
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
    # Start a parity check with error correction
    result = client.array.start_parity_check(correcting=True)
    print(f"Parity check started: {result.get('message')}")
except Exception as e:
    print(f"Failed to start parity check: {e}")
    </code></pre>
  </div>
</div>

### stop_parity_check

Stop a running parity check.

<div class="api-method">
  <div class="method-signature">
    stop_parity_check() -> Dict[str, Any]
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
    result = client.array.stop_parity_check()
    print(f"Parity check stopped: {result.get('message')}")
except Exception as e:
    print(f"Failed to stop parity check: {e}")
    </code></pre>
  </div>
</div>

### get_parity_status

Get the status of the parity check.

<div class="api-method">
  <div class="method-signature">
    get_parity_status() -> Dict[str, Any]
  </div>

  <div class="parameters">
    <h4>Parameters</h4>
    <p>None</p>
  </div>

  <div class="returns">
    <h4>Returns</h4>
    <p>A dictionary containing parity status information with the following structure:</p>
    <ul>
      <li><code>running</code>: Whether a parity check is running</li>
      <li><code>type</code>: Type of parity check</li>
      <li><code>progress</code>: Progress percentage</li>
      <li><code>position</code>: Current position</li>
      <li><code>size</code>: Total size</li>
      <li><code>speed</code>: Speed in bytes per second</li>
      <li><code>remainingTime</code>: Estimated remaining time in seconds</li>
      <li><code>errors</code>: Number of errors found</li>
    </ul>
  </div>

  <div class="example">
    <h4>Example</h4>
    <pre><code class="language-python">
# Get parity status
parity_status = client.array.get_parity_status()
if parity_status.get('running'):
    print(f"Parity check running: {parity_status.get('type')}")
    print(f"Progress: {parity_status.get('progress')}%")
    print(f"Speed: {parity_status.get('speed') / (1024**2):.2f} MB/s")
    print(f"Remaining time: {parity_status.get('remainingTime') / 60:.2f} minutes")
    print(f"Errors: {parity_status.get('errors')}")
else:
    print("No parity check running")
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
    
    # Get array status
    array_status = await client.array.get_array_status()
    print(f"Array state: {array_status.get('state')}")

asyncio.run(main())
```
