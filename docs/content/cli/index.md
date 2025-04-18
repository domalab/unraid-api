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

- `system` - Get system information (CPU, memory, OS details)
- `array` - Manage the array (status, parity check, disks)
- `disks` - List all disks with basic information
- `disk` - Get detailed information about a specific disk
- `smart` - Get SMART data for a specific disk
- `docker` - Manage Docker containers
- `vms` - Manage virtual machines
- `notifications` - Manage notifications
- `all` - Get all available information

## Examples

### Get System Information

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY --query system
```

### Get Array Status

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY --query array
```

### List All Disks

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY --query disks
```

### Get Detailed Information About a Specific Disk

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY --query disk --disk-id "disk:sda"
```

### Get SMART Data for a Specific Disk

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY --query smart --disk-id "disk:sda"
```

### List Docker Containers

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY --query docker
```

### List Virtual Machines

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY --query vms
```

## Next Steps

Explore the documentation for each command to learn more about the available options and how to use them:

- [System Command](system) - Get system information
- [Array Command](array) - Manage the array
- [Disks Command](disks) - Work with disks
- [Docker Command](docker) - Manage Docker containers
- [VMs Command](vms) - Manage virtual machines
