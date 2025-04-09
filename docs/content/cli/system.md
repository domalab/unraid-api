---
layout: default
title: System Command
parent: Command Line Interface
nav_order: 1
---

# System Command

The `system` command provides information about the Unraid server.

## Usage

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY system
```

## Output

The command outputs system information in a formatted table:

```
+---------------------------+---------------------------+
| SYSTEM INFORMATION        |                           |
+---------------------------+---------------------------+
| OS                        | Unraid 7.0 x86_64         |
| Kernel                    | 6.6.78-Unraid             |
| Uptime                    | 36 days, 5 hours          |
| CPU                       | Intel Core i7-8700K       |
| Cores/Threads             | 6/12                      |
| Memory Total              | 32.0 GB                   |
| Memory Used               | 16.5 GB (51.6%)           |
| Memory Free               | 15.5 GB (48.4%)           |
| System Manufacturer       | ASRock                    |
| System Model              | Z370 Pro4                 |
+---------------------------+---------------------------+
```

## Options

The `system` command supports the following options:

| Option | Description |
|--------|-------------|
| `--json` | Output in JSON format |
| `--raw` | Output raw data without formatting |
| `--no-header` | Hide the header row in the table |
| `--no-border` | Hide the table borders |

## Examples

### Get system information in JSON format

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY system --json
```

Output:
```json
{
  "os": {
    "platform": "linux",
    "distro": "Unraid",
    "release": "7.0 x86_64",
    "kernel": "6.6.78-Unraid",
    "uptime": 3153600
  },
  "cpu": {
    "manufacturer": "Intel",
    "brand": "Core i7-8700K",
    "cores": 6,
    "threads": 12
  },
  "memory": {
    "total": 34359738368,
    "used": 17716740096,
    "free": 16642998272
  },
  "system": {
    "manufacturer": "ASRock",
    "model": "Z370 Pro4"
  }
}
```

### Get system information without formatting

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY system --raw
```

### Get system information without header

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY system --no-header
```

### Get system information without borders

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY system --no-border
```
