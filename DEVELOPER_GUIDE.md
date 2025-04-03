# Unraid API Developer Guide for Home Assistant

This guide provides detailed information for Home Assistant developers on how to integrate the unraid-api Python library into their Unraid integrations.

## Table of Contents
1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Authentication](#authentication)
4. [Available Resources](#available-resources)
5. [Error Handling](#error-handling)
6. [Home Assistant Integration Examples](#home-assistant-integration-examples)
7. [Best Practices](#best-practices)

## Installation

The unraid-api library can be installed using pip:

```bash
pip install unraid-api
```

For Home Assistant integrations, add the following to your `manifest.json`:

```json
{
  "dependencies": ["unraid-api>=0.1.3"]
}
```

## Basic Usage

The library provides both synchronous and asynchronous clients. For Home Assistant integrations, you'll typically want to use the asynchronous client.

### Asynchronous Client

```python
from unraid_api import AsyncUnraidClient

async def setup_unraid_client(host: str, api_key: str) -> AsyncUnraidClient:
    """Set up the Unraid client."""
    client = AsyncUnraidClient(
        host=host,
        port=443,  # Default port
        use_ssl=True,  # Use SSL by default
        verify_ssl=False,  # Don't verify SSL certificates by default
        api_key=api_key
    )
    return client
```

### Synchronous Client

```python
from unraid_api import UnraidClient

def setup_unraid_client(host: str, api_key: str) -> UnraidClient:
    """Set up the Unraid client."""
    client = UnraidClient(
        host=host,
        port=443,
        use_ssl=True,
        verify_ssl=False,
        api_key=api_key
    )
    return client
```

## Authentication

The Unraid GraphQL API only supports API key authentication. Username/password authentication is not supported.

### API Key Authentication

```python
# Using API Key
client = AsyncUnraidClient(
    host="your-unraid-server",
    api_key="your-api-key"
)
```

API keys should be created in the Unraid WebUI under Settings > Management Access > API Keys.

## Available Resources

The library provides access to various Unraid resources through the client:

### Array Operations
```python
# Get array status (includes boot device and pool devices)
array_status = await client.array.get_array_status()

# Access boot device information
boot_device = array_status.get("boot")
if boot_device:
    print(f"Boot device: {boot_device['name']} ({boot_device['device']})")
    if boot_device.get("fsType"):
        print(f"Filesystem type: {boot_device['fsType']}")

# Access cache pools information
caches = array_status.get("caches", [])
for cache in caches:
    print(f"Cache: {cache['id']}")
    for pool in cache.get("pools", []):
        print(f"  Pool: {pool['name']} - Size: {pool['size']} - Used: {pool['used']}")
        for device in pool.get("devices", []):
            print(f"    Device: {device['name']} ({device['device']})")

# Start array
await client.array.start_array()

# Stop array
await client.array.stop_array()
```

### Docker Operations
```python
# Get all containers
containers = await client.docker.get_containers()

# Start container
await client.docker.start_container("container_name")

# Stop container
await client.docker.stop_container("container_name")

# Restart container
await client.docker.restart_container("container_name")
```

### System Information
```python
# Get system info (includes CPU and motherboard temperature)
system_info = await client.info.get_system_info()

# Access CPU temperature
cpu_temp = system_info["cpu"]["temperature"]

# Access motherboard temperature
motherboard_temp = system_info["system"]["temperature"]

# Reboot server
await client.info.reboot()

# Shutdown server
await client.info.shutdown()
```

### Disk Operations
```python
# Get disk information
disks = await client.disk.get_disks()

# Get specific disk (includes spindown status)
disk = await client.disk.get_disk("disk_id")

# Check filesystem type
if disk.get("fsType"):
    print(f"Filesystem type: {disk['fsType']}")

# Check if disk is spun down
if disk.get("spindownStatus") == "spundown":
    print(f"Disk is spun down. Last spindown time: {disk.get('lastSpindownTime')}")

# Get SMART data for a disk
smart_data = await client.disk.get_disk_smart("disk_id")

# Check SMART status
if smart_data.get("status") == "PASSED":
    print("SMART status is good")

# Access SMART attributes
for attribute in smart_data.get("attributes", []):
    print(f"Attribute {attribute['id']}: {attribute['name']} = {attribute['value']}")

# Mount disk
await client.disk.mount_disk("disk_id")

# Unmount disk
await client.disk.unmount_disk("disk_id")
```

### VM Operations
```python
# Get all VMs
vms = await client.vm.get_vms()

# Start VM
await client.vm.start_vm("vm_name")

# Stop VM
await client.vm.stop_vm("vm_name")
```

## Error Handling

The library provides specific exceptions for different error scenarios:

```python
from unraid_api.exceptions import (
    AuthenticationError,
    ConnectionError,
    APIError,
    ValidationError,
    OperationError,
    RateLimitError
)

try:
    await client.array.start_array()
except AuthenticationError:
    # Handle authentication errors
    pass
except ConnectionError:
    # Handle connection errors
    pass
except APIError as e:
    # Handle API errors
    pass
except ValidationError:
    # Handle validation errors
    pass
except OperationError:
    # Handle operation errors
    pass
except RateLimitError:
    # Handle rate limit errors
    pass
```

## Home Assistant Integration Examples

### Basic Integration Setup

```python
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_API_KEY
from unraid_api import AsyncUnraidClient

class UnraidDataUpdateCoordinator:
    """Data update coordinator for Unraid."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the coordinator."""
        self.hass = hass
        self.config_entry = config_entry
        self.client = None

    async def async_setup(self) -> None:
        """Set up the coordinator."""
        self.client = AsyncUnraidClient(
            host=self.config_entry.data[CONF_HOST],
            api_key=self.config_entry.data[CONF_API_KEY],
        )

    async def async_update_data(self) -> dict:
        """Update data."""
        try:
            system_info = await self.client.info.get_system_info()
            array_status = await self.client.array.get_array_status()
            containers = await self.client.docker.get_containers()

            return {
                "system_info": system_info,
                "array_status": array_status,
                "containers": containers,
            }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with Unraid: {err}")
```

### Creating Sensors

```python
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

class UnraidArrayStatusSensor(SensorEntity):
    """Representation of Unraid array status sensor."""

    def __init__(self, coordinator: UnraidDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._attr_name = "Unraid Array Status"
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_array_status"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["array_status"]["status"]

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.last_update_success

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Unraid sensors."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([UnraidArrayStatusSensor(coordinator)])
```

### Creating Services

```python
from homeassistant.core import ServiceCall
from homeassistant.helpers.typing import ConfigType

async def async_setup_services(hass: HomeAssistant, config: ConfigType) -> None:
    """Set up services for Unraid integration."""

    async def async_start_array(call: ServiceCall) -> None:
        """Service to start the Unraid array."""
        coordinator = hass.data[DOMAIN][call.data["entry_id"]]
        await coordinator.client.array.start_array()

    async def async_stop_array(call: ServiceCall) -> None:
        """Service to stop the Unraid array."""
        coordinator = hass.data[DOMAIN][call.data["entry_id"]]
        await coordinator.client.array.stop_array()

    hass.services.async_register(
        DOMAIN,
        SERVICE_START_ARRAY,
        async_start_array,
        schema=START_ARRAY_SERVICE_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_STOP_ARRAY,
        async_stop_array,
        schema=STOP_ARRAY_SERVICE_SCHEMA,
    )
```

## Best Practices

1. **Use Async Client**: Always use the `AsyncUnraidClient` for Home Assistant integrations to maintain non-blocking operations.

2. **Error Handling**: Implement comprehensive error handling using the provided exceptions.

3. **Rate Limiting**: Be mindful of API rate limits and implement appropriate delays between requests.

4. **Data Caching**: Use Home Assistant's data update coordinator to cache data and prevent excessive API calls.

5. **Configuration Validation**: Validate all configuration data before creating the client.

6. **Resource Cleanup**: Properly close connections and clean up resources when the integration is unloaded.

7. **Logging**: Implement appropriate logging for debugging and error tracking.

8. **Type Hints**: Use type hints throughout your integration code for better maintainability.

## Additional Resources

- [Home Assistant Integration Documentation](https://developers.home-assistant.io/docs/creating_integration)
- [unraid-api GitHub Repository](https://github.com/domalab/unraid-api)