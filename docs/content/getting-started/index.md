---
layout: default
title: Getting Started
nav_order: 2
has_children: true
permalink: /content/getting-started
---

# Getting Started with Unraid API

This section will guide you through the process of setting up and using the Unraid API Python library. You'll learn how to install the library, enable the GraphQL API on your Unraid server, and create your first connection.

## Quick Start

1. Install the library:
   ```bash
   pip install unraid-api
   ```

2. Enable the GraphQL API on your Unraid server
3. Generate an API key
4. Connect to your Unraid server:
   ```python
   from unraid_api import UnraidClient
   
   client = UnraidClient("192.168.1.10", api_key="your-api-key")
   system_info = client.info.get_system_info()
   print(f"Unraid version: {system_info.get('os', {}).get('release')}")
   ```

## Next Steps

- [Installation](installation) - Detailed installation instructions
- [Authentication](authentication) - How to authenticate with the Unraid GraphQL API
- [Basic Usage](basic-usage) - Basic usage examples
- [Error Handling](error-handling) - How to handle errors
