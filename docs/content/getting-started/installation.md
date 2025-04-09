---
layout: default
title: Installation
parent: Getting Started
nav_order: 1
---

# Installation

This guide will walk you through the process of installing the Unraid API Python library.

## Requirements

- Python 3.7 or higher
- pip (Python package installer)

## Installing from PyPI

The easiest way to install the Unraid API library is using pip:

```bash
pip install unraid-api
```

This will install the library and all its dependencies.

## Installing with CLI Support

If you want to use the command-line interface, install with the CLI extra:

```bash
pip install unraid-api[cli]
```

## Installing from Source

You can also install the library directly from the source code:

```bash
git clone https://github.com/domalab/unraid-api.git
cd pyUNRAID
pip install -e .
```

To install with CLI support from source:

```bash
pip install -e ".[cli]"
```

## Verifying Installation

You can verify that the installation was successful by importing the library in Python:

```python
import unraid_api
print(unraid_api.__version__)
```

Or, if you installed with CLI support, by running the CLI command:

```bash
unraid-cli --version
```

## Next Steps

Now that you have installed the Unraid API library, you need to:

1. [Enable the GraphQL API](authentication#enabling-the-graphql-api) on your Unraid server
2. [Generate an API key](authentication#generating-an-api-key) for authentication
3. [Connect to your Unraid server](basic-usage)
