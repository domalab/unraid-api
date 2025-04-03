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
# Get disk information (includes temperature and SMART status)
disks = await client.disk.get_disks()

# Display disk temperature
for disk in disks:
    temp = disk.get("temperature")
    if temp is not None and temp > 0:
        print(f"Disk {disk['name']} temperature: {temp}°C")

    # Display SMART status
    smart_status = disk.get("smartStatus")
    if smart_status:
        print(f"Disk {disk['name']} SMART status: {smart_status}")

# Get specific disk with detailed information
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

# Get spindown delay setting
spindown_delay = await client.info.get_spindown_delay()
print(f"Disk spindown delay: {spindown_delay} minutes")

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

### Exception Details

1. **AuthenticationError**: Raised when there's an issue with authentication, such as an invalid API key.
   ```python
   try:
       await client.array.get_array_status()
   except AuthenticationError as e:
       print(f"Authentication failed: {e}")
       # Prompt user to check their API key
   ```

2. **ConnectionError**: Raised when the client can't connect to the Unraid server.
   ```python
   try:
       await client.disk.get_disks()
   except ConnectionError as e:
       print(f"Connection failed: {e}")
       # Check if the Unraid server is online and reachable
   ```

3. **APIError**: Raised when the API returns an error response.
   ```python
   try:
       await client.vm.start_vm("non_existent_vm")
   except APIError as e:
       print(f"API error: {e}")
       # Handle specific API errors based on the error message
   ```

4. **ValidationError**: Raised when input validation fails.
   ```python
   try:
       await client.disk.mount_disk("")
   except ValidationError as e:
       print(f"Validation error: {e}")
       # Fix the invalid input
   ```

5. **OperationError**: Raised when an operation fails.
   ```python
   try:
       await client.array.stop_array()
   except OperationError as e:
       print(f"Operation failed: {e}")
       # Handle the specific operation failure
   ```

6. **RateLimitError**: Raised when the API rate limit is exceeded.
   ```python
   try:
       # Making too many requests in a short time
       for _ in range(100):
           await client.array.get_array_status()
   except RateLimitError as e:
       print(f"Rate limit exceeded: {e}")
       # Implement backoff strategy or reduce request frequency
   ```

## Home Assistant Integration Examples

### Basic Integration Setup

```python
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from unraid_api import UnraidClient

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Unraid from a config entry."""
    host = entry.data["host"]
    api_key = entry.data["api_key"]

    client = UnraidClient(host=host, api_key=api_key)

    # Test the connection
    try:
        system_info = await client.info.get_system_info()
        hass.data[DOMAIN][entry.entry_id] = client
        return True
    except Exception as e:
        return False
```

### Creating Sensors for Disk Temperature

```python
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up Unraid disk temperature sensors."""
    client = hass.data[DOMAIN][entry.entry_id]

    try:
        disks = await client.disk.get_disks()
        sensors = []

        for disk in disks:
            if disk.get("temperature") is not None:
                sensors.append(UnraidDiskTemperatureSensor(client, disk))

        async_add_entities(sensors, True)
    except Exception as e:
        # Handle error
        pass

class UnraidDiskTemperatureSensor(SensorEntity):
    """Sensor for Unraid disk temperature."""

    def __init__(self, client, disk):
        """Initialize the sensor."""
        self._client = client
        self._disk = disk
        self._attr_name = f"Unraid {disk['name']} Temperature"
        self._attr_unique_id = f"unraid_disk_{disk['id']}_temperature"
        self._attr_native_unit_of_measurement = "°C"
        self._attr_device_class = "temperature"
        self._attr_state_class = "measurement"

    async def async_update(self):
        """Update the sensor."""
        try:
            disk = await self._client.disk.get_disk(self._disk["id"])
            self._attr_native_value = disk.get("temperature")
        except Exception as e:
            # Handle error
            pass
```

### Creating Binary Sensors for Disk SMART Status

```python
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up Unraid disk SMART status sensors."""
    client = hass.data[DOMAIN][entry.entry_id]

    try:
        disks = await client.disk.get_disks()
        sensors = []

        for disk in disks:
            if disk.get("smartStatus") is not None:
                sensors.append(UnraidDiskSmartSensor(client, disk))

        async_add_entities(sensors, True)
    except Exception as e:
        # Handle error
        pass

class UnraidDiskSmartSensor(BinarySensorEntity):
    """Binary sensor for Unraid disk SMART status."""

    def __init__(self, client, disk):
        """Initialize the sensor."""
        self._client = client
        self._disk = disk
        self._attr_name = f"Unraid {disk['name']} SMART Status"
        self._attr_unique_id = f"unraid_disk_{disk['id']}_smart"
        self._attr_device_class = "problem"

    async def async_update(self):
        """Update the sensor."""
        try:
            disk = await self._client.disk.get_disk(self._disk["id"])
            # True means there's a problem (SMART status is not PASSED)
            self._attr_is_on = disk.get("smartStatus") != "PASSED"
        except Exception as e:
            # Handle error
            pass
```

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