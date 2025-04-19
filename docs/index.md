---
title: Home
description: Python Library for Unraid GraphQL API
---

# Unraid API: Python Library for Unraid GraphQL API

[![PyPI version](https://badge.fury.io/py/unraid-api.svg)](https://badge.fury.io/py/unraid-api)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/domalab/unraid-api/actions/workflows/test.yml/badge.svg)](https://github.com/domalab/unraid-api/actions/workflows/test.yml)

A comprehensive Python library that provides a clean, intuitive interface to Unraid's GraphQL API. It enables developers to programmatically control and monitor Unraid servers with both synchronous and asynchronous support, strong typing, and intelligent error handling.

## Features

- Complete coverage of Unraid GraphQL API endpoints
- Both synchronous and asynchronous client interfaces
- Strongly-typed Pydantic models
- Comprehensive error handling
- API key authentication
- Built-in query caching
- Real-time subscription support
- Extensive documentation and examples
- Command-line interface tool

## Quick Links

<div class="grid cards" markdown>

<div class="grid-item" markdown>

:fontawesome-solid-rocket: [Getting Started](getting-started/installation.md)

* Install and configure the Unraid API client

</div>

<div class="grid-item" markdown>

:fontawesome-solid-code: [API Reference](api-reference/overview.md)

* Explore the complete API documentation

</div>

<div class="grid-item" markdown>

:fontawesome-solid-terminal: [Command Line Interface](cli/overview.md)

* Learn how to use the built-in CLI

</div>

<div class="grid-item" markdown>

:fontawesome-brands-github: [Development](development/contributing.md)

* Contribute to the project and learn our development process

</div>

</div>

## Example Usage

```python
from unraid_api import UnraidClient

# Connect to Unraid server with API key
client = UnraidClient("192.168.1.10", api_key="your-api-key")

# Get system info
system_info = client.get_system_info()
print(f"System version: {system_info.version}")

# Get Docker containers
containers = client.docker.get_containers()
for container in containers:
    print(f"Container: {container.name}, Status: {container.status}")
```

## License

This project is licensed under the [MIT License](about/license.md). 