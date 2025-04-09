---
layout: default
title: Installation
parent: Home Assistant Integration
nav_order: 1
---

# Installation

This guide will walk you through the process of installing the Unraid integration for Home Assistant.

## Prerequisites

Before you begin, make sure you have:

1. A running Home Assistant instance
2. An Unraid server with the GraphQL API enabled
3. An API key for authentication (see [Authentication]({{ site.baseurl }}/content/getting-started/authentication))

## Installation Methods

There are two ways to install the Unraid integration:

### Method 1: Manual Installation

1. Download the repository from GitHub:
   ```bash
   git clone https://github.com/domalab/pyUNRAID.git
   ```

2. Copy the `custom_components/unraid` directory to your Home Assistant `custom_components` directory:
   ```bash
   cp -r pyUNRAID/custom_components/unraid /path/to/homeassistant/custom_components/
   ```

3. Restart Home Assistant:
   ```bash
   ha core restart
   ```

### Method 2: HACS Installation

If you have [HACS](https://hacs.xyz/) (Home Assistant Community Store) installed, you can add the Unraid integration as a custom repository:

1. Open Home Assistant
2. Go to HACS > Integrations
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add the repository URL: `https://github.com/domalab/pyUNRAID`
6. Select "Integration" as the category
7. Click "Add"
8. Search for "Unraid" in HACS
9. Click "Install"
10. Restart Home Assistant

## Adding the Integration

After installation, you need to add the integration to Home Assistant:

1. Open Home Assistant
2. Go to Settings > Devices & Services
3. Click "Add Integration"
4. Search for "Unraid"
5. Click on the Unraid integration

## Configuration

During setup, you'll need to provide:

1. **Unraid Server IP Address or Hostname**: The IP address or hostname of your Unraid server (e.g., `192.168.1.10` or `unraid.local`)
2. **API Key**: The API key you generated for authentication

The integration will automatically handle redirects to myunraid.net domains if your server is configured to use Unraid Connect.

## Verifying Installation

After adding the integration, you should see the Unraid device in your Home Assistant instance:

1. Go to Settings > Devices & Services
2. Click on the Unraid integration
3. You should see your Unraid server listed as a device
4. Click on the device to see the available entities

## Troubleshooting

If you encounter issues during installation:

### Integration Not Found

If the integration doesn't appear in the list of available integrations:

1. Make sure you've copied the `custom_components/unraid` directory to the correct location
2. Check that the directory structure is correct:
   ```
   custom_components/
   └── unraid/
       ├── __init__.py
       ├── manifest.json
       ├── config_flow.py
       └── ...
   ```
3. Restart Home Assistant

### Connection Issues

If you can't connect to your Unraid server:

1. Make sure the GraphQL API is enabled on your Unraid server
2. Check that the IP address or hostname is correct
3. Verify that the API key is valid
4. Check if your Unraid server is accessible from your Home Assistant instance

### Logs

To check the logs for more information:

1. Go to Settings > System > Logs
2. Filter for "unraid" to see logs related to the integration

## Next Steps

After successful installation, you can:

1. [Configure the integration](configuration)
2. [Explore the available sensors](sensors)
3. [Use the available services](services)
4. [Create automations](automations)
