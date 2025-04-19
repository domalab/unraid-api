---
title: Installation
description: How to install and set up the Unraid API client
---

# Installation

## Prerequisites

Before installing the `unraid-api` library, make sure you have:

- Python 3.7 or higher
- pip (Python package installer)
- An Unraid server with the GraphQL API enabled

## Installing the Package

You can install the package using pip:

```bash
pip install unraid-api
```

This will install the latest stable version of the library from PyPI.

!!! note
    While the package is installed with `pip install unraid-api`, you import it in your code using `import unraid_api` or `from unraid_api import UnraidClient`.

## Development Installation

If you want to install the development version directly from GitHub:

```bash
pip install git+https://github.com/domalab/unraid-api.git
```

## Enabling the Unraid GraphQL API

Before you can use this library, you need to enable the GraphQL API on your Unraid server and generate an API key.

### Enabling the GraphQL Sandbox

1. Enable developer mode using the CLI on your Unraid server:

   ```bash
   unraid-api developer
   ```

2. Follow the prompts to enable the sandbox. This will allow you to access the Apollo Sandbox interface.

3. Access the GraphQL playground by navigating to:

   ```plaintext
   http://YOUR_SERVER_IP/graphql
   ```

### Creating an API Key

1. Use the CLI on your Unraid server to create an API key:

   ```bash
   unraid-api apikey --create
   ```

2. Follow the prompts to set:
   - Name
   - Description
   - Roles
   - Permissions

3. The generated API key should be used with this library as shown in the examples in the [Quick Start](quick-start.md) section.

## Verifying the Installation

You can verify that the installation was successful by running:

```python
import unraid_api
print(unraid_api.__version__)
```

This should print the version number of the installed library.

## Next Steps

Once you have installed the library and set up an API key, you can proceed to the [Authentication](authentication.md) section to learn how to connect to your Unraid server. 