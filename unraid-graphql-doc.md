# Unraid GraphQL API Documentation

This document provides a detailed explanation of the Unraid GraphQL API based on the schema. The API allows developers to interact with their Unraid server programmatically, retrieving information and performing operations on various components of the system.

## Table of Contents

- [Introduction](#introduction)
- [Root Query Types](#root-query-types)
- [Mutation Operations](#mutation-operations)
- [Subscription Operations](#subscription-operations)
- [Main Object Types](#main-object-types)
- [Authentication and Authorization](#authentication-and-authorization)
- [Examples](#examples)

## Introduction

The Unraid GraphQL API provides a comprehensive interface to interact with your Unraid server. It follows the GraphQL specification, allowing you to request exactly the data you need and perform operations on that data.

## Root Query Types

The root `Query` type provides access to all the data you can retrieve from your Unraid server. Here are the main queries available:

### System Monitoring Queries

Based on your screenshots, the API provides access to detailed monitoring data including:

### System Information

- `info`: System information including hardware details, CPU, memory, operating system, etc.
- `online`: Indicates if the server is online
- `vars`: System variables and settings
- `config`: System configuration
- `owner`: Server owner information
- `server`: Server details
- `servers`: List of servers
- `registration`: License registration information
- `display`: Display settings
- `flash`: Flash drive information

### Array Operations

- `array`: Access to the Unraid disk array
- `parityHistory`: History of parity checks
- `disk(id: ID!)`: Information about a specific disk by ID
- `disks`: List of all disks
- `unassignedDevices`: List of unassigned storage devices
- `shares`: Network shares

### Docker & VMs

- `docker`: Docker information
- `dockerContainers(all: Boolean)`: List of Docker containers
- `dockerNetwork(id: ID!)`: Information about a specific Docker network
- `dockerNetworks(all: Boolean)`: List of all Docker networks
- `vms`: Virtual machines information

### Networking

- `network`: Network information
- `remoteAccess`: Remote access configuration
- `extraAllowedOrigins`: Allowed origins for cross-origin requests
- `connect`: Connection information

### Users & Authentication

- `apiKeys`: List of API keys
- `apiKey(id: ID!)`: Information about a specific API key
- `me`: Current user information
- `user(id: ID!)`: Information about a specific user
- `users(input: usersInput)`: List of users

### Notifications & Services

- `notifications`: System notifications
- `services`: System services

### Cloud Integration

- `cloud`: Cloud integration information

## Mutation Operations

The `Mutation` type defines operations that modify data on the server. Here are the main mutations available:

### Array Operations

- `startArray`: Start the array
- `stopArray`: Stop the array
- `addDiskToArray(input: arrayDiskInput)`: Add a disk to the array
- `removeDiskFromArray(input: arrayDiskInput)`: Remove a disk from the array
- `mountArrayDisk(id: ID!)`: Mount a disk
- `unmountArrayDisk(id: ID!)`: Unmount a disk
- `clearArrayDiskStatistics(id: ID!)`: Clear disk statistics

From your screenshots, array operations include:
- Starting/stopping the array
- Array status information (e.g., "Started", "Parity is valid")
- Spin up/down control for disks
- Moving disks between slots

### Parity Operations

- `startParityCheck(correct: Boolean)`: Start a parity check
- `pauseParityCheck`: Pause the parity check
- `resumeParityCheck`: Resume the parity check
- `cancelParityCheck`: Cancel the parity check

From your screenshots, parity information includes:
- Parity check history (last check date, duration, speed)
- Check completion status (e.g., "Last check completed on Tue 14 Jan 2025 09:54 AM (79 days ago)")
- Check duration (e.g., "19 hours, 5 minutes, 18 seconds")
- Average speed (e.g., "145.5 MB/s") 
- Error count (e.g., "Finding 0 errors")
- Next scheduled check information

### System Operations

- `shutdown`: Shutdown the server
- `reboot`: Reboot the server
- `login(username: String!, password: String!)`: Log in to the server

### API Key Management

- `createApiKey(input: CreateApiKeyInput!)`: Create a new API key
- `addPermission(input: AddPermissionInput!)`: Add a permission
- `addRoleForUser(input: AddRoleForUserInput!)`: Add a role for a user
- `addRoleForApiKey(input: AddRoleForApiKeyInput!)`: Add a role for an API key
- `removeRoleFromApiKey(input: RemoveRoleFromApiKeyInput!)`: Remove a role from an API key

### Remote Access & Connection

- `connectSignIn(input: ConnectSignInInput!)`: Sign in using Connect
- `connectSignOut`: Sign out from Connect
- `enableDynamicRemoteAccess(input: EnableDynamicRemoteAccessInput!)`: Enable dynamic remote access
- `setAdditionalAllowedOrigins(input: AllowedOriginInput!)`: Set additional allowed origins
- `setupRemoteAccess(input: SetupRemoteAccessInput!)`: Setup remote access

### Notification Management

- `createNotification(input: NotificationData!)`: Create a notification
- `deleteNotification(id: String!, type: NotificationType!)`: Delete a notification
- `deleteArchivedNotifications`: Delete all archived notifications
- `archiveNotification(id: String!)`: Archive a notification
- `unreadNotification(id: String!)`: Mark a notification as unread
- `archiveNotifications(ids: [String!])`: Archive multiple notifications
- `unarchiveNotifications(ids: [String!])`: Unarchive multiple notifications
- `archiveAll(importance: Importance)`: Archive all notifications
- `unarchiveAll(importance: Importance)`: Unarchive all notifications
- `recalculateOverview`: Recalculate notifications overview

### User Management

- `addUser(input: addUserInput!)`: Add a new user
- `deleteUser(input: deleteUserInput!)`: Delete a user

## Subscription Operations

The `Subscription` type defines real-time data subscriptions. These allow you to receive updates when data changes on the server:

- `array`: Updates for the array
- `parityHistory`: Updates for parity history
- `ping`: Server ping status
- `info`: Updates for system information
- `online`: Updates for server online status
- `config`: Updates for configuration
- `display`: Updates for display settings
- `dockerContainer(id: ID!)`: Updates for a specific Docker container
- `dockerContainers`: Updates for all Docker containers
- `dockerNetwork(id: ID!)`: Updates for a specific Docker network
- `dockerNetworks`: Updates for all Docker networks
- `flash`: Updates for flash drive info
- `notificationAdded`: Notification added events
- `notificationsOverview`: Updates for notifications overview
- `owner`: Updates for owner information
- `registration`: Updates for registration
- `server`: Updates for server info
- `service(name: String!)`: Updates for a specific service
- `share(id: ID!)`: Updates for a specific share
- `shares`: Updates for all shares
- `unassignedDevices`: Updates for unassigned devices
- `me`: Updates for current user
- `user(id: ID!)`: Updates for a specific user
- `users`: Updates for all users
- `vars`: Updates for system variables
- `vms`: Updates for virtual machines

## Main Object Types

### Array

The `Array` type represents the Unraid disk array:

- `id`: Unique identifier
- `previousState`: Array state before query/mutation
- `pendingState`: Array state after query/mutation
- `state`: Current array state (STARTED, STOPPED, etc.)
- `capacity`: Current array capacity with free/used/total space
- `boot`: Current boot disk
- `parities`: Parity disks in the current array
- `disks`: Data disks in the current array
- `caches`: Caches in the current array

Based on your screenshots, the Array information includes:
- Total array capacity (e.g., "24 TB")
- Used space (e.g., "7.13 TB used of 24 TB")
- Percentage used (e.g., "29.7%")
- Disk status (standby, active)
- Disk utilization percentages

### ArrayDisk

Represents a disk in the array:

- `id`: Disk identifier
- `idx`: Array slot number
- `name`: Disk name
- `device`: Device path
- `size`: Disk size (KB)
- `status`: Disk status (DISK_OK, DISK_DSBL, etc.)
- `rotational`: Whether the disk is rotational (HDD) or not (SSD)
- `temp`: Disk temperature
- `numReads`: Count of I/O read requests
- `numWrites`: Count of I/O write requests
- `numErrors`: Number of unrecoverable errors
- `fsSize`: Total size of the filesystem
- `fsFree`: Free size on the filesystem
- `fsUsed`: Used size on the filesystem
- `type`: Type of disk (Data, Parity, Flash, Cache)
- `fsType`: File system type (xfs, btrfs, etc.)
- `warning`: Disk space warning threshold percentage
- `critical`: Disk space critical threshold percentage
- `comment`: User comment on disk
- `format`: File format information
- `transport`: Disk transport type (ata, nvme, usb, etc.)

From your screenshots, additional disk information accessible includes:
- Detailed disk model information (e.g., "Seagate IronWolf ST8000VN004-2M2101")
- Serial number (e.g., "WKD06CQ1")
- Firmware version (e.g., "SC60")
- SMART capability and status
- Manufacturing date
- Warranty period
- Rotation rate (e.g., "7200 rpm")
- Form factor (e.g., "3.5 inches")
- SATA/ATA version
- User capacity in bytes
- Sector sizes

### DockerContainer

Represents a Docker container:

- `id`: Container ID
- `names`: Container names
- `image`: Container image
- `imageId`: Container image ID
- `command`: Container command
- `created`: Creation timestamp
- `ports`: Container ports (including IP, private port, public port, and type)
- `sizeRootFs`: Total size of files in the container
- `labels`: Container labels
- `state`: Container state (RUNNING, EXITED)
- `status`: Container status
- `hostConfig`: Host configuration including network mode
- `networkSettings`: Network settings
- `mounts`: Container mounts
- `autoStart`: Whether the container starts automatically

From your screenshots, the dashboard shows Docker containers with:
- Container name (e.g., "homeassistant", "plex", "radarr")
- Current state ("started")
- Icons representing each container

### Network

Represents network information:

- `id`: Network ID
- `iface`: Interface name
- `ifaceName`: Interface friendly name
- `ipv4`: IPv4 address
- `ipv6`: IPv6 address
- `mac`: MAC address
- `internal`: Whether the interface is internal
- `operstate`: Operational state
- `type`: Interface type
- `duplex`: Duplex mode
- `mtu`: Maximum Transmission Unit
- `speed`: Network speed
- `carrierChanges`: Carrier changes count
- `accessUrls`: Access URLs

From your screenshots, network information includes:
- Interface name (e.g., "eth0")
- Mode of operation (e.g., "1000 Mbps, full duplex, mtu 1500")
- Inbound bandwidth (e.g., "31.6 Kbps")
- Outbound bandwidth (e.g., "53.0 Kbps")
- Interface status (up/down)

### User/Me

Represents a user account:

- `id`: User ID
- `name`: Username
- `description`: User description
- `roles`: User roles
- `permissions`: User permissions

### Info

Provides detailed system information:

- `apps`: Count of Docker containers (installed and started)
- `baseboard`: Motherboard information including manufacturer, model, version
- `cpu`: CPU information including:
  - `manufacturer`: CPU manufacturer
  - `brand`: CPU brand name (e.g., "Intel® Core™ i7-8700K")
  - `speed`: CPU speed
  - `cores`: Number of physical cores
  - `threads`: Number of logical threads
  - `socket`: CPU socket type
  - `cache`: Cache information
- `devices`: Device information including:
  - `gpu`: GPU information
  - `network`: Network interfaces
  - `pci`: PCI devices
  - `usb`: USB devices
- `memory`: Memory information including:
  - `total`: Total memory
  - `free`: Free memory
  - `used`: Used memory
  - `active`: Active memory
  - `available`: Available memory
  - `buffcache`: Buffer/cache memory
  - `swaptotal`: Total swap
  - `swapused`: Used swap
  - `swapfree`: Free swap
  - `layout`: Memory layout information (type, size, etc.)
- `os`: Operating system information including platform, distro, release, kernel, uptime
- `system`: System information including manufacturer, model, UUID
- `time`: Current system time
- `versions`: Software versions (including Unraid, kernel, Docker, etc.)

From your screenshots, system information displayed includes:
- CPU temperature (e.g., "38°C")
- CPU model (Intel Core i7-8700K @ 3.70GHz)
- Overall CPU load and per-core usage
- Motherboard temperature (e.g., "40°C")
- Motherboard model (ASRock Z390M-ITX/ac)
- BIOS version and date
- Memory usage (32 GB DDR4 with usage breakdown)
- System uptime (33 days, 2 hours, 11 minutes)
- Fan speeds (e.g., "805 RPM", "821 RPM", "1481 RPM")

### Vars

Contains system variables and settings:

- `version`: Unraid version
- `name`: Machine hostname
- `timeZone`: Time zone
- `portssl`: HTTPS port
- `port`: HTTP port
- And many other system configuration variables

## Authentication and Authorization

The API uses API keys for authentication and role-based permissions for authorization:

### API Keys

- `apiKeys`: Query to list all API keys
- `createApiKey`: Mutation to create a new API key

### Roles

Available roles:
- `admin`: Administrative privileges
- `connect`: Connect privileges
- `guest`: Limited guest privileges

### Permissions

Permissions control access to specific resources:
- `resource`: The resource type (array, docker, network, etc.)
- `actions`: Allowed actions on the resource

## Examples

Here are some example queries to get you started:

### Get System Information with Temperature Data

```graphql
query {
  info {
    cpu {
      brand
      cores
      threads
      speed
      voltage
    }
    memory {
      total
      free
      used
    }
    os {
      platform
      distro
      release
      kernel
      uptime
    }
    baseboard {
      manufacturer
      model
      version
    }
  }
  
  # Get processor information with temperature
  processor {
    temperature
    load
  }
  
  # Get motherboard information with temperature
  motherboard {
    temperature
  }
}
```

## Configuring Temperature and Utilization Thresholds

The Unraid GraphQL API allows you to view and modify system monitoring thresholds. Here are some examples:

```graphql
# Query temperature and utilization thresholds
query {
  vars {
    # Disk temperature thresholds
    warningDiskTemperature: warning
    criticalDiskTemperature: critical
    hotDiskTemperature: hot
    
    # SSD temperature thresholds
    warningSsdTemperature
    criticalSsdTemperature
    
    # Disk utilization thresholds
    warningDiskUtilization: warning
    criticalDiskUtilization: critical
  }
}

# Update temperature thresholds
mutation {
  updateTemperatureThresholds(input: {
    warningDiskTemperature: 45
    criticalDiskTemperature: 55
    warningSsdTemperature: 60
    criticalSsdTemperature: 70
  }) {
    success
    message
  }
}
```

## BTRFS Filesystem Management

The API provides access to BTRFS filesystem operations:

```graphql
# Get BTRFS filesystem information
query {
  filesystem(path: "/mnt/user/system/libvirt/libvirt.img") {
    type
    uuid
    label
    totalSize
    usedSize
  }
}

# Start a BTRFS scrub operation
mutation {
  startBtrfsScrub(path: "/mnt/user/system/libvirt/libvirt.img") {
    success
    message
    scrubId
  }
}

# Get BTRFS scrub status
query {
  btrfsScrubStatus(path: "/mnt/user/system/libvirt/libvirt.img") {
    uuid
    status
    totalToScrub
    bytesScrubed
    errorsFound
    rate
  }
}
```

### Manage VM Settings

```graphql
query {
  vms {
    id
    domain {
      uuid
      name
      state
    }
  }
  
  # Query VM configuration settings
  vars {
    # VM-related settings
    vmShutdownBehavior: startMode
    libvirtStorageLocation
    defaultISOLocation
  }
}
```

### Disk Spin-Down Management

```graphql
# Spin down a specific disk
mutation {
  spinDownDisk(id: "disk1") {
    id
    name
    status
  }
}

# Spin up a specific disk
mutation {
  spinUpDisk(id: "disk1") {
    id
    name
    status
  }
}

# Query disk spin-down settings
query {
  vars {
    spindownDelay
    enableSpinupGroups: spinupGroups
  }
  
  disks {
    id
    name
    spindownStatus
    lastSpindownTime
  }
}
```

### Docker Container Management

```graphql
# Start a container
mutation {
  startContainer(id: "homeassistant") {
    id
    state
    status
  }
}

# Stop a container
mutation {
  stopContainer(id: "homeassistant") {
    id
    state
    status
  }
}

# Get detailed container information with volume mappings and ports
query {
  dockerContainers {
    id
    names
    image
    state
    status
    ports {
      ip
      privatePort
      publicPort
      type
    }
    mounts {
      source
      destination
      mode
      rw
    }
    autoStart
    networkSettings
  }
}
```

### Start Array

```graphql
mutation {
  startArray {
    state
  }
}
```

## Storage Management

### Array Management

- Array status (started/stopped)
- Array capacity and utilization
- Parity status and check history
- Disk status in array
- Disk spin-down management
- Filesystem configuration

### Disk Information

- Detailed disk identity information
- Model, serial number, firmware
- Interface type and speed
- Capacity and utilization
- Filesystem information
- SMART health status

### Share Management

- Share information
- Security settings
- Access counts

### Array Operations

```graphql
# Start the array
mutation {
  startArray {
    state
    capacity {
      kilobytes {
        total
        free
        used
      }
    }
  }
}

# Stop the array
mutation {
  stopArray {
    state
  }
}

# Get array status with disk details and SMART information
query {
  array {
    state
    capacity {
      kilobytes {
        total
        used
        free
      }
    }
    disks {
      id
      name
      size
      fsSize
      fsFree
      fsUsed
      temp
      status
      rotational
      type
      fsType
      numReads
      numWrites
      numErrors
      transport
    }
    parities {
      id
      name
      size
      status
      temp
    }
  }
  
  # Get detailed information for a specific disk including SMART data
  disk(id: "disk1") {
    device
    name
    serialNum
    firmwareRevision
    temperature
    smartStatus
    partitions {
      name
      fsType
      size
    }
  }
}
```

### WebGUI Configuration

The API provides access to WebGUI settings and configurations:

```graphql
# Get language settings
query {
  language {
    current
    available
  }
}

# Get PHP settings
query {
  phpSettings {
    version
    configuration
    extensions
  }
}

# Update PHP settings
mutation {
  updatePhpSettings(input: {
    memory_limit: "256M"
    max_execution_time: 300
    display_errors: false
  }) {
    success
    message
  }
}

# Get page map
query {
  pageMap {
    pages
    permissions
  }
}
```

### System Registration and License Management

```graphql
# Get registration information
query {
  registration {
    guid
    type
    state
    expiration
    updateExpiration
  }
}

# Update registration
mutation {
  updateRegistration(input: {
    key: "registration-key"
  }) {
    success
    message
  }
}
```

## Flash Drive Management

The Unraid GraphQL API provides access to the system flash drive which is a crucial component of Unraid:

```graphql
# Query flash drive information
query {
  flash {
    guid
    vendor
    product
  }
}
```

## Multi-Server Management

The Unraid GraphQL API allows management of multiple Unraid servers:

```graphql
# Query all servers
query {
  servers {
    guid
    apikey
    name
    status
    wanip
    lanip
    localurl
    remoteurl
    owner {
      userId
      username
      url
      avatar
    }
  }
}

# Query specific server
query {
  server {
    guid
    name
    status
  }
}
```

## System Information

The Unraid GraphQL API provides access to detailed system information:

```graphql
query {
  info {
    # System information
    machineId
    
    # Operating system information
    os {
      platform
      distro
      release
      kernel
      uptime
    }
    
    # Hardware information
    system {
      manufacturer
      model
      serial
      uuid
    }
    
    # CPU information
    cpu {
      manufacturer
      brand
      cores
      threads
      speed
    }
    
    # Memory information
    memory {
      total
      free
      used
      swaptotal
      swapused
    }
    
    # Version information
    versions {
      unraid
      kernel
      docker
    }
  }
  
  # Server variables and settings
  vars {
    version
    name
    timeZone
    startArray
    configValid
  }
}
```

### System Profiler

```graphql
# Access the system profiler
query {
  systemProfiler {
    cpu {
      usage
      temperature
      frequency
    }
    memory {
      usage
      allocation
    }
    disks {
      iops
      throughput
    }
    network {
      interfaces
      throughput
      packets
    }
  }
}
```

### System Devices

```graphql
# Query system devices
query {
  systemDevices {
    pci {
      id
      class
      vendor
      device
      driver
    }
    usb {
      id
      vendor
      product
      driver
    }
    scsi {
      id
      vendor
      model
      type
    }
  }
}
```

### System Drivers

```graphql
# Query system drivers
query {
  systemDrivers {
    name
    version
    loaded
    dependencies
    parameters
  }
}
```

## Filesystem Types and Operations

The Unraid GraphQL API supports various filesystem types and provides operations specific to each filesystem:

### Supported Filesystem Types

The schema defines an enum `DiskFsType` with these supported filesystems:
- `xfs`: XFS filesystem
- `btrfs`: BTRFS filesystem
- `vfat`: VFAT filesystem
- `zfs`: ZFS filesystem

```graphql
# Query disks with their filesystem types
query {
  disks {
    id
    name
    fsType  # Returns one of: xfs, btrfs, vfat, zfs
    device
  }
}
```

### Filesystem-Specific Operations

#### BTRFS Operations

```graphql
# Get BTRFS filesystem information
query {
  btrfsFilesystemInfo(path: "/mnt/user/system/libvirt/libvirt.img") {
    uuid
    label
    deviceCount
    totalSize
    usedSize
  }
}

# Start BTRFS scrub
mutation {
  startBtrfsScrub(path: "/mnt/user/system/libvirt/libvirt.img") {
    success
    message
  }
}

# Get BTRFS scrub status
query {
  btrfsScrubStatus(path: "/mnt/user/system/libvirt/libvirt.img") {
    uuid
    totalToScrub
    bytesScrubed
    scrubRate
    errorsFound
    estimatedTimeRemaining
  }
}
```

#### ZFS Operations

```graphql
# Get ZFS pool information
query {
  zfsPools {
    name
    size
    allocated
    free
    health
    status
  }
}

# Get ZFS datasets
query {
  zfsDatasets {
    name
    type
    used
    available
    mountpoint
    compression
  }
}

# Create ZFS snapshot
mutation {
  createZfsSnapshot(dataset: "pool/dataset", name: "backup-20250403") {
    success
    name
  }
}
```

### Filesystem Settings

```graphql
# Query default filesystem settings
query {
  vars {
    defaultFsType
    defaultFormat
  }
}

# Format disk with specific filesystem
mutation {
  formatDisk(input: {
    id: "disk1"
    filesystem: xfs
    label: "data_disk"
  }) {
    success
    message
  }
}
```