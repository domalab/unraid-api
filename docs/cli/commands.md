---
title: CLI Commands
description: Reference for all available commands in the Unraid API CLI
---

# CLI Commands

This page provides a comprehensive reference for all commands available in the Unraid API CLI.

## General Commands

### `unraid-cli info`

Display information about the connected Unraid server.

**Usage:**
```bash
unraid-cli info
```

**Output Example:**
```
Unraid Server Information
-------------------------
Server: MyUnraidServer
Version: 6.10.3
OS: Unraid OS
IP Address: 192.168.1.10
Uptime: 15 days, 7 hours, 23 minutes
CPU: Intel(R) Core(TM) i7-10700 CPU @ 2.90GHz (16 cores)
Memory: 32GB (75% used)
```

### `unraid-cli status`

Display the current status of the Unraid server, including array status, CPU load, memory usage, and network status.

**Usage:**
```bash
unraid-cli status
```

**Options:**
* `--json`: Output in JSON format
* `--compact`: Display compact status view

### `unraid-cli version`

Display the version of the Unraid API CLI.

**Usage:**
```bash
unraid-cli version
```

## Array Commands

### `unraid-cli array list`

List all disks in the array.

**Usage:**
```bash
unraid-cli array list [OPTIONS]
```

**Options:**
* `--json`: Output in JSON format
* `--filter STATUS`: Filter by disk status (active, disabled, etc.)

**Example:**
```bash
unraid-cli array list --filter active
```

### `unraid-cli array status`

Show the current status of the array.

**Usage:**
```bash
unraid-cli array status
```

**Output Example:**
```
Array Status
------------
Status: Normal
Protection Mode: Parity
Size: 40 TB
Used: 25 TB (62.5%)
Free: 15 TB (37.5%)
```

### `unraid-cli array start`

Start the array.

**Usage:**
```bash
unraid-cli array start
```

### `unraid-cli array stop`

Stop the array.

**Usage:**
```bash
unraid-cli array stop [OPTIONS]
```

**Options:**
* `--force`: Force array stop even if devices are busy

### `unraid-cli parity check`

Start a parity check.

**Usage:**
```bash
unraid-cli parity check [OPTIONS]
```

**Options:**
* `--status`: Check current parity check status
* `--stop`: Stop current parity check
* `--correcting`: Start a correcting parity check

## Docker Commands

### `unraid-cli docker list`

List all Docker containers.

**Usage:**
```bash
unraid-cli docker list [OPTIONS]
```

**Options:**
* `--all`: Show all containers (including stopped)
* `--running`: Show only running containers
* `--json`: Output in JSON format

**Example:**
```bash
unraid-cli docker list --running
```

### `unraid-cli docker start`

Start a Docker container.

**Usage:**
```bash
unraid-cli docker start CONTAINER_ID
```

**Example:**
```bash
unraid-cli docker start plex
```

### `unraid-cli docker stop`

Stop a Docker container.

**Usage:**
```bash
unraid-cli docker stop [OPTIONS] CONTAINER_ID
```

**Options:**
* `--timeout SECONDS`: Timeout in seconds before forcing stop (default: 10)

### `unraid-cli docker restart`

Restart a Docker container.

**Usage:**
```bash
unraid-cli docker restart CONTAINER_ID
```

### `unraid-cli docker logs`

View logs from a Docker container.

**Usage:**
```bash
unraid-cli docker logs [OPTIONS] CONTAINER_ID
```

**Options:**
* `--tail N`: Show last N lines (default: all)
* `--follow`: Follow log output
* `--timestamps`: Show timestamps

**Example:**
```bash
unraid-cli docker logs --tail 50 --follow plex
```

### `unraid-cli docker stats`

Display resource usage statistics for Docker containers.

**Usage:**
```bash
unraid-cli docker stats [OPTIONS]
```

**Options:**
* `--json`: Output in JSON format
* `--no-stream`: Display current statistics only, do not stream

## VM Commands

### `unraid-cli vm list`

List all virtual machines.

**Usage:**
```bash
unraid-cli vm list [OPTIONS]
```

**Options:**
* `--all`: Show all VMs (including stopped)
* `--running`: Show only running VMs
* `--json`: Output in JSON format

### `unraid-cli vm start`

Start a virtual machine.

**Usage:**
```bash
unraid-cli vm start VM_ID
```

### `unraid-cli vm stop`

Stop a virtual machine.

**Usage:**
```bash
unraid-cli vm stop [OPTIONS] VM_ID
```

**Options:**
* `--force`: Force VM to stop (hard power off)

### `unraid-cli vm restart`

Restart a virtual machine.

**Usage:**
```bash
unraid-cli vm restart [OPTIONS] VM_ID
```

**Options:**
* `--force`: Force restart (hard reset)

### `unraid-cli vm info`

Display detailed information about a virtual machine.

**Usage:**
```bash
unraid-cli vm info VM_ID
```

## System Commands

### `unraid-cli system reboot`

Reboot the Unraid server.

**Usage:**
```bash
unraid-cli system reboot [OPTIONS]
```

**Options:**
* `--force`: Force reboot without confirmation
* `--delayed MINUTES`: Schedule reboot after specified minutes

### `unraid-cli system shutdown`

Shutdown the Unraid server.

**Usage:**
```bash
unraid-cli system shutdown [OPTIONS]
```

**Options:**
* `--force`: Force shutdown without confirmation
* `--delayed MINUTES`: Schedule shutdown after specified minutes

### `unraid-cli system stats`

Display system resource usage statistics.

**Usage:**
```bash
unraid-cli system stats [OPTIONS]
```

**Options:**
* `--json`: Output in JSON format
* `--watch SECONDS`: Update every SECONDS (like top)
* `--cpu`: Show only CPU statistics
* `--memory`: Show only memory statistics
* `--network`: Show only network statistics

**Example:**
```bash
unraid-cli system stats --watch 2
```

## User Commands

### `unraid-cli user list`

List all users.

**Usage:**
```bash
unraid-cli user list
```

### `unraid-cli user create`

Create a new user.

**Usage:**
```bash
unraid-cli user create [OPTIONS] USERNAME
```

**Options:**
* `--password PASSWORD`: Set user password
* `--role ROLE`: Set user role (admin, user, etc.)
* `--description DESC`: Set user description

### `unraid-cli user delete`

Delete a user.

**Usage:**
```bash
unraid-cli user delete USERNAME
```

### `unraid-cli user password`

Change a user's password.

**Usage:**
```bash
unraid-cli user password USERNAME
```

## Notification Commands

### `unraid-cli notification list`

List all notifications.

**Usage:**
```bash
unraid-cli notification list [OPTIONS]
```

**Options:**
* `--all`: Include archived notifications
* `--json`: Output in JSON format

### `unraid-cli notification create`

Create a new notification.

**Usage:**
```bash
unraid-cli notification create [OPTIONS]
```

**Options:**
* `--title TITLE`: Notification title
* `--message MESSAGE`: Notification message
* `--importance LEVEL`: Importance level (normal, warning, alert)
* `--icon ICON`: Icon name
* `--link URL`: Action link

**Example:**
```bash
unraid-cli notification create --title "Backup Complete" --message "Weekly backup finished successfully" --importance normal
```

### `unraid-cli notification archive`

Archive a notification.

**Usage:**
```bash
unraid-cli notification archive NOTIFICATION_ID
```

### `unraid-cli notification delete`

Delete a notification.

**Usage:**
```bash
unraid-cli notification delete NOTIFICATION_ID
```

## Configuration Commands

### `unraid-cli config get`

Get a configuration value.

**Usage:**
```bash
unraid-cli config get [SECTION] KEY
```

**Example:**
```bash
unraid-cli config get server url
```

### `unraid-cli config set`

Set a configuration value.

**Usage:**
```bash
unraid-cli config set [SECTION] KEY VALUE
```

**Example:**
```bash
unraid-cli config set server url http://192.168.1.10
```

### `unraid-cli config list`

List all configuration values.

**Usage:**
```bash
unraid-cli config list [SECTION]
```

**Example:**
```bash
unraid-cli config list server
```

## Advanced Commands

### `unraid-cli exec`

Execute a command on the Unraid server.

**Usage:**
```bash
unraid-cli exec COMMAND
```

**Example:**
```bash
unraid-cli exec "ls -la /mnt/user/"
```

!!! warning
    This command requires administrator privileges and should be used with caution.

### `unraid-cli monitor`

Monitor Unraid server in real-time.

**Usage:**
```bash
unraid-cli monitor [OPTIONS]
```

**Options:**
* `--interval SECONDS`: Update interval in seconds (default: 2)
* `--resources`: Monitor system resources
* `--array`: Monitor array status
* `--docker`: Monitor Docker containers
* `--vm`: Monitor virtual machines

**Example:**
```bash
unraid-cli monitor --resources --docker --interval 5
``` 