---
title: CLI Overview
description: Overview of the Unraid API command-line interface
---

# Command-Line Interface Overview

The Unraid API library includes a command-line interface (CLI) that allows you to interact with your Unraid server directly from the terminal. This provides a quick way to perform common operations without writing Python code.

## Installation

The CLI is automatically installed when you install the Unraid API package:

```bash
pip install unraid-api
```

## Basic Usage

The CLI can be accessed using the `unraid-cli` command:

```bash
unraid-cli --ip 192.168.1.10 --api-key YOUR_API_KEY [command]
```

### Global Options

| Option | Description |
|--------|-------------|
| `--ip` | The IP address or hostname of your Unraid server |
| `--api-key` | Your Unraid API key |
| `--timeout` | Connection timeout in seconds (default: 10) |
| `--ssl-verify` | Whether to verify SSL certificates (default: True) |
| `--follow-redirects` | Whether to follow redirects (default: True) |
| `--help` | Show help message and exit |
| `--version` | Show version and exit |

## Available Commands

The CLI organizes commands into categories that mirror the library's resources:

### System Commands

```bash
# Get system information
unraid-cli --ip 192.168.1.10 --api-key YOUR_API_KEY system info

# Reboot the system
unraid-cli --ip 192.168.1.10 --api-key YOUR_API_KEY system reboot

# Shutdown the system
unraid-cli --ip 192.168.1.10 --api-key YOUR_API_KEY system shutdown
```

### Docker Commands

```bash
# List all Docker containers
unraid-cli --ip 192.168.1.10 --api-key YOUR_API_KEY docker list

# Start a container
unraid-cli --ip 192.168.1.10 --api-key YOUR_API_KEY docker start CONTAINER_NAME

# Stop a container
unraid-cli --ip 192.168.1.10 --api-key YOUR_API_KEY docker stop CONTAINER_NAME

# Restart a container
unraid-cli --ip 192.168.1.10 --api-key YOUR_API_KEY docker restart CONTAINER_NAME
```

### Array Commands

```bash
# Get array status
unraid-cli --ip 192.168.1.10 --api-key YOUR_API_KEY array status

# Start the array
unraid-cli --ip 192.168.1.10 --api-key YOUR_API_KEY array start

# Stop the array
unraid-cli --ip 192.168.1.10 --api-key YOUR_API_KEY array stop

# Start a parity check
unraid-cli --ip 192.168.1.10 --api-key YOUR_API_KEY array parity-check
```

### VM Commands

```bash
# List all VMs
unraid-cli --ip 192.168.1.10 --api-key YOUR_API_KEY vm list

# Start a VM
unraid-cli --ip 192.168.1.10 --api-key YOUR_API_KEY vm start VM_NAME

# Stop a VM
unraid-cli --ip 192.168.1.10 --api-key YOUR_API_KEY vm stop VM_NAME

# Restart a VM
unraid-cli --ip 192.168.1.10 --api-key YOUR_API_KEY vm restart VM_NAME
```

## Output Formats

By default, the CLI outputs results in a human-readable format. You can change the output format with the `--format` option:

```bash
# Output as JSON
unraid-cli --ip 192.168.1.10 --api-key YOUR_API_KEY --format json docker list

# Output as YAML
unraid-cli --ip 192.168.1.10 --api-key YOUR_API_KEY --format yaml docker list

# Output as Table (default)
unraid-cli --ip 192.168.1.10 --api-key YOUR_API_KEY --format table docker list
```

## Configuration File

To avoid typing the IP and API key for every command, you can create a configuration file:

1. Create a file at `~/.unraid-cli/config.yaml` with the following content:

   ```yaml
   default:
     ip: 192.168.1.10
     api_key: YOUR_API_KEY
   
   # You can define multiple servers
   backup:
     ip: 192.168.1.11
     api_key: ANOTHER_API_KEY
   ```

2. Use the `--profile` option to select a server:

   ```bash
   # Use the default server
   unraid-cli docker list
   
   # Use a specific server
   unraid-cli --profile backup docker list
   ```

## Next Steps

For detailed information on each command, see the [Commands](commands.md) page. 