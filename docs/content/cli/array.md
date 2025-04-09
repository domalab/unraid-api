---
layout: default
title: Array Command
parent: Command Line Interface
nav_order: 2
---

# Array Command

The `array` command provides information about the Unraid array and allows you to manage it.

## Usage

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY array [options]
```

## Output

The command outputs array information in a formatted table:

```
+---------------------------+---------------------------+
| ARRAY INFORMATION         |                           |
+---------------------------+---------------------------+
| State                     | STARTED                   |
| Size                      | 40.0 TB                   |
| Used                      | 25.6 TB (64.0%)           |
| Free                      | 14.4 TB (36.0%)           |
| Protected                 | Yes                       |
+---------------------------+---------------------------+

+---------------------------+---------------------------+---------------------------+
| DEVICE                    | STATUS                    | SIZE                     |
+---------------------------+---------------------------+---------------------------+
| Parity 1                  | DISK_OK                   | 10.0 TB                  |
| Disk 1                    | DISK_OK                   | 10.0 TB                  |
| Disk 2                    | DISK_OK                   | 10.0 TB                  |
| Disk 3                    | DISK_OK                   | 10.0 TB                  |
| Disk 4                    | DISK_OK                   | 10.0 TB                  |
| Cache 1                   | DISK_OK                   | 1.0 TB                   |
+---------------------------+---------------------------+---------------------------+
```

## Options

The `array` command supports the following options:

| Option | Description |
|--------|-------------|
| `--json` | Output in JSON format |
| `--raw` | Output raw data without formatting |
| `--no-header` | Hide the header row in the table |
| `--no-border` | Hide the table borders |
| `--start` | Start the array |
| `--stop` | Stop the array |
| `--parity-check` | Start a parity check |
| `--parity-check-cancel` | Cancel a running parity check |
| `--parity-check-status` | Show parity check status |

## Examples

### Get array information in JSON format

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY array --json
```

Output:
```json
{
  "state": "STARTED",
  "size": 43980465111040,
  "used": 28147497671065,
  "free": 15832967439975,
  "protected": true,
  "devices": [
    {
      "type": "parity",
      "name": "Parity 1",
      "status": "DISK_OK",
      "size": 10995116277760
    },
    {
      "type": "data",
      "name": "Disk 1",
      "status": "DISK_OK",
      "size": 10995116277760
    },
    {
      "type": "data",
      "name": "Disk 2",
      "status": "DISK_OK",
      "size": 10995116277760
    },
    {
      "type": "data",
      "name": "Disk 3",
      "status": "DISK_OK",
      "size": 10995116277760
    },
    {
      "type": "data",
      "name": "Disk 4",
      "status": "DISK_OK",
      "size": 10995116277760
    },
    {
      "type": "cache",
      "name": "Cache 1",
      "status": "DISK_OK",
      "size": 1099511627776
    }
  ]
}
```

### Start the array

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY array --start
```

Output:
```
Array started successfully.
```

### Stop the array

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY array --stop
```

Output:
```
Array stopped successfully.
```

### Start a parity check

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY array --parity-check
```

Output:
```
Parity check started successfully.
```

### Cancel a running parity check

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY array --parity-check-cancel
```

Output:
```
Parity check cancelled successfully.
```

### Show parity check status

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY array --parity-check-status
```

Output:
```
+---------------------------+---------------------------+
| PARITY CHECK STATUS       |                           |
+---------------------------+---------------------------+
| Running                   | Yes                       |
| Type                      | Parity Check              |
| Progress                  | 45.2%                     |
| Position                  | 4.5 TB                    |
| Size                      | 10.0 TB                   |
| Speed                     | 125.6 MB/s                |
| Remaining Time            | 12 hours, 34 minutes      |
| Errors                    | 0                         |
+---------------------------+---------------------------+
```
