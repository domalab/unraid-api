---
layout: default
title: Command Line Interface
nav_order: 4
has_children: true
permalink: /content/cli
---

# Command Line Interface

The Unraid API library includes a command-line interface (CLI) that allows you to interact with Unraid servers from the command line. This section covers how to install, configure, and use the CLI.

## Installation

To install the CLI, you need to install the Unraid API library with the CLI extra:

```bash
pip install unraid-api[cli]
```

## Basic Usage

The CLI is accessed using the `unraid-cli` command:

```bash
unraid-cli --help
```

This will display the available commands and options.

## Authentication

To authenticate with the Unraid server, you need to provide an API key:

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY system
```

You can also set environment variables to avoid typing the IP and API key every time:

```bash
export UNRAID_IP=192.168.1.10
export UNRAID_API_KEY=YOUR_API_KEY

# Now you can run commands without specifying the IP and API key
unraid-cli system
```

## Available Commands

The CLI provides commands for interacting with different aspects of the Unraid server:

- `system` - Get system information
- `array` - Manage the array
- `disks` - Work with disks
- `docker` - Manage Docker containers
- `vms` - Manage virtual machines
- `notifications` - Manage notifications

## Next Steps

Explore the documentation for each command to learn more about the available options and how to use them:

- [System Command](system) - Get system information
- [Array Command](array) - Manage the array
- [Disks Command](disks) - Work with disks
- [Docker Command](docker) - Manage Docker containers
- [VMs Command](vms) - Manage virtual machines
