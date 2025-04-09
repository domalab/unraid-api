---
layout: default
title: Home Assistant Integration
nav_order: 5
has_children: true
permalink: /content/home-assistant
---

# Home Assistant Integration

The Unraid API library includes a Home Assistant integration that allows you to monitor and control your Unraid server from Home Assistant. This section covers how to install, configure, and use the integration.

## Features

The Home Assistant integration provides the following features:

- System information sensors (version, uptime, memory usage)
- Array status sensors (state, capacity, usage)
- Disk sensors (temperature, SMART status)
- Docker container controls (start, stop, restart)
- VM controls (start, stop, restart)
- Array controls (start, stop, parity check)

## Installation

The Home Assistant integration is included in the `custom_components/unraid` directory of the repository. To install it:

1. Copy the `custom_components/unraid` directory to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Go to Settings > Devices & Services > Add Integration
4. Search for "Unraid" and follow the setup instructions

## Configuration

During setup, you'll need to provide:

- Unraid Server IP Address or Hostname
- API Key (generated as described in the [Authentication]({{ site.baseurl }}/content/getting-started/authentication) section)

The integration will automatically handle redirects to myunraid.net domains if your server is configured to use Unraid Connect.

## Available Sensors

The integration provides the following sensors:

### System Sensors
- System Version - Shows the Unraid OS version
- System Uptime - Shows system uptime in a human-readable format
- Memory Usage Percentage - Shows memory usage as percentage
- Memory Usage - Shows used memory in GB
- Memory Free - Shows free memory in GB
- Memory Total - Shows total memory in GB
- CPU Usage - Shows CPU usage

### Array Sensors
- Array Usage Percentage - Shows array usage as percentage
- Array Capacity - Shows total array capacity in TB
- Array Used - Shows used array space in TB
- Array Free - Shows free array space in TB

### Disk Sensors
- Disk Temperature - Shows temperature for each disk (where available)
- Disk SMART Status - Shows SMART status for each disk (where available)

### Binary Sensors
- Array Status - Shows if array is OK
- Parity Status - Shows if parity disk is OK
- Cache Status - Shows if cache disk is OK
- Server Connection - Shows if server is connected
- Docker Service - Shows if Docker service is running
- VM Service - Shows if VM service is running

## Services

The integration provides the following services:

### Array Services
- `unraid.start_array` - Start the array
- `unraid.stop_array` - Stop the array
- `unraid.start_parity_check` - Start a parity check
- `unraid.stop_parity_check` - Stop a parity check

### Docker Services
- `unraid.start_container` - Start a Docker container
- `unraid.stop_container` - Stop a Docker container
- `unraid.restart_container` - Restart a Docker container

### VM Services
- `unraid.start_vm` - Start a virtual machine
- `unraid.stop_vm` - Stop a virtual machine
- `unraid.restart_vm` - Restart a virtual machine

## Limitations

Due to limitations in the Unraid GraphQL API, the following sensors are not available:

- CPU Temperature - Not available in the API
- Motherboard Temperature - Not available in the API
- Fan Speeds - Not available in the API
- Network Traffic - Not available in the API
- Flash Device Usage (as a separate entity) - Not available in the API
- Log Filesystem Usage (as a separate entity) - Not available in the API

## Next Steps

Explore the documentation for more details on the integration:

- [Installation](installation) - Detailed installation instructions
- [Configuration](configuration) - Configuration options
- [Sensors](sensors) - Available sensors and their attributes
- [Services](services) - Available services and how to use them
- [Automations](automations) - Example automations
