---
layout: default
title: VMs Command
parent: Command Line Interface
nav_order: 5
---

# VMs Command

The `vms` command provides information about virtual machines running on your Unraid server. It displays details such as VM names, UUIDs, and current state (running, paused, or shutdown).

## Usage

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY vms [options]
```

## Output

The command outputs virtual machine information in a formatted table:

```bash
╭─────────────────────────────────────────────────────────────────────────────╮
│                           Virtual Machines                                  │
├───────────────┬─────────────────────────────────────────┬──────────────────┤
│ Name          │ UUID                                    │ State            │
├───────────────┼─────────────────────────────────────────┼──────────────────┤
│ Windows 10    │ 550e8400-e29b-41d4-a716-446655440000    │ RUNNING          │
│ Ubuntu Server │ 6ba7b810-9dad-11d1-80b4-00c04fd430c8    │ SHUTDOWN         │
│ Debian        │ 6ba7b811-9dad-11d1-80b4-00c04fd430c8    │ PAUSED           │
╰───────────────┴─────────────────────────────────────────┴──────────────────╯
```

The output includes:

- **Name**: The name of the virtual machine
- **UUID**: The unique identifier for the VM
- **State**: Current state of the VM (RUNNING, PAUSED, or SHUTDOWN)

## Options

The `vms` command supports the following options:

| Option | Description |
|--------|-------------|
| `--json` | Output in JSON format |
| `--raw` | Output raw data without formatting |
| `--no-header` | Hide the header row in the table |
| `--no-border` | Hide the table borders |

### Notes

- The VM information is only available if the VM service is running on the Unraid server
- If the VM service is not running, a message will be displayed indicating that VM information is not available
- The CLI gracefully handles errors when the VM service is not available

## Examples

### Get VM information in JSON format

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY vms --json
```

Output:
```json
{
  "domain": [
    {
      "name": "Windows 10",
      "uuid": "550e8400-e29b-41d4-a716-446655440000",
      "state": "RUNNING"
    },
    {
      "name": "Ubuntu Server",
      "uuid": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
      "state": "SHUTDOWN"
    },
    {
      "name": "Debian",
      "uuid": "6ba7b811-9dad-11d1-80b4-00c04fd430c8",
      "state": "PAUSED"
    }
  ]
}
```

### Get VM information without formatting

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY vms --raw
```

### Get VM information without header

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY vms --no-header
```

### Get VM information without borders

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY vms --no-border
```

## Limitations

The Unraid GraphQL API may return an error when trying to retrieve VM information if:

1. The VM service is not running on the Unraid server
2. There are no VMs configured on the server
3. The API key does not have permission to access VM information

In these cases, the CLI will display an appropriate error message and continue with other operations.
