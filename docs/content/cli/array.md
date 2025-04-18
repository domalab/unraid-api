---
layout: default
title: Array Command
parent: Command Line Interface
nav_order: 2
---

# Array Command

The `array` command provides information about the Unraid array and allows you to manage it. This command displays detailed information about the array status, including state, capacity, parity disks, data disks, and cache disks. It also shows parity check status if a check is in progress.

## Usage

```bash
unraid-cli --ip 192.168.1.10 --key YOUR_API_KEY array [options]
```

## Output

The command outputs array information in a formatted table:

```
╭────────────────┬─────────────────────────────────────────────────────────╮
│ Property       │ Value                                                   │
├────────────────┼─────────────────────────────────────────────────────────┤
│ State          │ STARTED                                                 │
│ Filesystem State│ STARTED                                                │
│ Parity Check   │ RUNNING                                                │
│ Parity Action  │ check P                                                │
│ Parity Progress│ 45% (4.5TB)                                            │
│ Progress Details│ Checking parity... 45% complete, 12 hours remaining    │
│ Total Capacity │ 40.0 TB                                                │
│ Used Space     │ 25.6 TB (64.0%)                                         │
│ Free Space     │ 14.4 TB (36.0%)                                         │
│ Boot Device    │ Ultra Fit (sda) - vfat                                 │
│ Parity Disks   │ 1                                                       │
│ Parity 1       │ WDC_WD100EFAX-68LHPN0_JEKV15MZ - DISK_OK               │
│ Array Disks    │ 4                                                       │
│ Disk 1         │ ST10000VN0008-2JJ101_ZJV01234 - DISK_OK - xfs          │
│ Disk 2         │ ST10000VN0008-2JJ101_ZJV01235 - DISK_OK - xfs          │
│ Disk 3         │ ST10000VN0008-2JJ101_ZJV01236 - DISK_OK - xfs          │
│ Disk 4         │ ST10000VN0008-2JJ101_ZJV01237 - DISK_OK - xfs          │
│ Cache Disks    │ 1                                                       │
│ Cache 1        │ Samsung_SSD_860_EVO_1TB_S4XBNF1234567 - DISK_OK - btrfs│
╰────────────────┴─────────────────────────────────────────────────────────╯
```

The output includes:

- **State**: Current state of the array (STARTED or STOPPED)
- **Filesystem State**: State of the filesystem
- **Parity Check**: Shows if a parity check is running
- **Parity Action**: Type of parity operation (check, sync, etc.)
- **Parity Progress**: Progress percentage and position
- **Progress Details**: Human-readable progress information
- **Total Capacity**: Total storage capacity of the array
- **Used/Free Space**: Storage usage statistics
- **Boot Device**: Information about the boot device
- **Parity Disks**: List of parity disks with status
- **Array Disks**: List of data disks with status and filesystem type
- **Cache Disks**: List of cache disks with status and filesystem type

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

### Notes

- The array state is determined by checking both the array state and the mdState from the vars data
- Parity check information is automatically displayed when a check is in progress
- Filesystem types (xfs, btrfs, zfs, vfat) are shown for each disk when available
- Disk spindown status is shown when available

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
╭────────────────┬─────────────────────────────────────────────────────────╮
│ Property       │ Value                                                   │
├────────────────┼─────────────────────────────────────────────────────────┤
│ Running        │ Yes                                                     │
│ Type           │ Parity Check                                            │
│ Progress       │ 45.2%                                                   │
│ Position       │ 4.5 TB                                                  │
│ Size           │ 10.0 TB                                                 │
│ Speed          │ 125.6 MB/s                                              │
│ Remaining Time │ 12 hours, 34 minutes                                    │
│ Errors         │ 0                                                       │
╰────────────────┴─────────────────────────────────────────────────────────╯
```

The parity check status shows detailed information about the current or most recent parity check operation, including progress, speed, and estimated completion time.
