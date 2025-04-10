---
layout: default
title: GraphQL API Reference
parent: API Reference
nav_order: 1
---

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

The root query types provide entry points to fetch data from the Unraid server. These are the main queries you can perform:

### System Information

Retrieve information about the Unraid system.

```graphql
query {
  system {
    version
    uptime
    temperature
    model
    memory {
      total
      used
      free
    }
    cpu {
      model
      cores
      threads
      usage
    }
  }
}
```

### Array Status

Get the current status of the Unraid array.

```graphql
query {
  array {
    status
    started
    protected
    size
    used
    free
    devices {
      name
      size
      free
      status
    }
  }
}
```

### Disk Information

Retrieve information about disks in the Unraid system.

```graphql
query {
  disks {
    name
    device
    size
    temperature
    status
    type
    fsType
    mountpoint
    serial
    model
  }
}
```

### Docker Containers

Get information about Docker containers running on the Unraid server.

```graphql
query {
  docker {
    containers {
      id
      name
      image
      status
      state
      created
      ports
      volumes
    }
  }
}
```

### Virtual Machines

Retrieve information about virtual machines on the Unraid server.

```graphql
query {
  vms {
    name
    id
    status
    memory
    vcpus
    disks {
      name
      size
      type
    }
    networks {
      name
      type
      mac
    }
  }
}
```

### User Information

Get information about Unraid users.

```graphql
query {
  users {
    name
    uid
    gid
    groups
    home
    shell
  }
}
```

### Shares

Retrieve information about shares on the Unraid server.

```graphql
query {
  shares {
    name
    path
    size
    free
    devices
    users {
      name
      access
    }
  }
}
```

## Mutation Operations

Mutations allow you to modify data on the Unraid server. These are the main operations you can perform:

### Array Operations

#### Start Array

Starts the Unraid array.

```graphql
mutation {
  startArray {
    success
    message
  }
}
```

#### Stop Array

Stops the Unraid array.

```graphql
mutation {
  stopArray {
    success
    message
  }
}
```

#### Start Parity Check

Starts a parity check operation.

```graphql
mutation {
  startParityCheck(
    options: {
      correcting: true
      full: false
    }
  ) {
    success
    message
  }
}
```

#### Stop Parity Check

Stops an ongoing parity check operation.

```graphql
mutation {
  stopParityCheck {
    success
    message
  }
}
```

### Docker Operations

#### Start Container

Starts a Docker container.

```graphql
mutation {
  startContainer(id: "container_id") {
    success
    message
  }
}
```

#### Stop Container

Stops a Docker container.

```graphql
mutation {
  stopContainer(id: "container_id") {
    success
    message
  }
}
```

#### Restart Container

Restarts a Docker container.

```graphql
mutation {
  restartContainer(id: "container_id") {
    success
    message
  }
}
```

#### Remove Container

Removes a Docker container.

```graphql
mutation {
  removeContainer(id: "container_id", force: true) {
    success
    message
  }
}
```

#### Pull Image

Pulls a Docker image.

```graphql
mutation {
  pullImage(image: "image:tag") {
    success
    message
  }
}
```

### VM Operations

#### Start VM

Starts a virtual machine.

```graphql
mutation {
  startVM(id: "vm_id") {
    success
    message
  }
}
```

#### Stop VM

Stops a virtual machine.

```graphql
mutation {
  stopVM(id: "vm_id", force: false) {
    success
    message
  }
}
```

#### Restart VM

Restarts a virtual machine.

```graphql
mutation {
  restartVM(id: "vm_id") {
    success
    message
  }
}
```

#### Pause VM

Pauses a virtual machine.

```graphql
mutation {
  pauseVM(id: "vm_id") {
    success
    message
  }
}
```

#### Resume VM

Resumes a paused virtual machine.

```graphql
mutation {
  resumeVM(id: "vm_id") {
    success
    message
  }
}
```

### User Operations

#### Add User

Adds a new user to the Unraid system.

```graphql
mutation {
  addUser(
    input: {
      name: "username"
      password: "password"
      description: "User description"
    }
  ) {
    success
    message
  }
}
```

#### Update User

Updates an existing user.

```graphql
mutation {
  updateUser(
    name: "username"
    input: {
      password: "new_password"
      description: "Updated description"
    }
  ) {
    success
    message
  }
}
```

#### Delete User

Deletes a user from the Unraid system.

```graphql
mutation {
  deleteUser(name: "username") {
    success
    message
  }
}
```

### Share Operations

#### Add Share

Adds a new share to the Unraid system.

```graphql
mutation {
  addShare(
    input: {
      name: "share_name"
      path: "/mnt/user/share_name"
      description: "Share description"
    }
  ) {
    success
    message
  }
}
```

#### Update Share

Updates an existing share.

```graphql
mutation {
  updateShare(
    name: "share_name"
    input: {
      description: "Updated description"
      accessMode: "public"
    }
  ) {
    success
    message
  }
}
```

#### Delete Share

Deletes a share from the Unraid system.

```graphql
mutation {
  deleteShare(name: "share_name") {
    success
    message
  }
}
```

## Subscription Operations

Subscriptions allow you to receive real-time updates from the Unraid server. These are the main subscriptions you can use:

### Array Status Updates

Subscribe to array status changes.

```graphql
subscription {
  arrayStatusChanged {
    status
    started
    protected
    size
    used
    free
  }
}
```

### Docker Container Updates

Subscribe to Docker container status changes.

```graphql
subscription {
  containerStatusChanged {
    id
    name
    status
    state
  }
}
```

### VM Status Updates

Subscribe to virtual machine status changes.

```graphql
subscription {
  vmStatusChanged {
    id
    name
    status
  }
}
```

### Disk Status Updates

Subscribe to disk status changes.

```graphql
subscription {
  diskStatusChanged {
    name
    status
    temperature
  }
}
```

### System Resource Updates

Subscribe to system resource usage updates.

```graphql
subscription {
  systemResourcesChanged {
    cpu {
      usage
    }
    memory {
      used
      free
    }
  }
}
```

## Main Object Types

These are the main object types returned by the Unraid GraphQL API:

### System

Represents the Unraid system.

| Field | Type | Description |
|-------|------|-------------|
| version | String | The Unraid version |
| uptime | Int | System uptime in seconds |
| temperature | Float | System temperature in Celsius |
| model | String | Server model |
| memory | Memory | Memory information |
| cpu | CPU | CPU information |

### Memory

Represents memory information.

| Field | Type | Description |
|-------|------|-------------|
| total | Int | Total memory in bytes |
| used | Int | Used memory in bytes |
| free | Int | Free memory in bytes |

### CPU

Represents CPU information.

| Field | Type | Description |
|-------|------|-------------|
| model | String | CPU model |
| cores | Int | Number of physical cores |
| threads | Int | Number of threads |
| usage | Float | CPU usage percentage |

### Array

Represents the Unraid array.

| Field | Type | Description |
|-------|------|-------------|
| status | String | Array status (e.g., "Started", "Stopped") |
| started | Boolean | Whether the array is started |
| protected | Boolean | Whether the array is protected |
| size | Int | Total array size in bytes |
| used | Int | Used space in bytes |
| free | Int | Free space in bytes |
| devices | [Device] | Array devices |

### Device

Represents a disk device in the Unraid array.

| Field | Type | Description |
|-------|------|-------------|
| name | String | Device name (e.g., "sda") |
| size | Int | Device size in bytes |
| free | Int | Free space in bytes |
| status | String | Device status |
| type | String | Device type (e.g., "data", "parity") |
| fsType | String | Filesystem type |
| mountpoint | String | Mount point |
| serial | String | Device serial number |
| model | String | Device model |

### Docker

Represents Docker information.

| Field | Type | Description |
|-------|------|-------------|
| containers | [Container] | List of Docker containers |

### Container

Represents a Docker container.

| Field | Type | Description |
|-------|------|-------------|
| id | String | Container ID |
| name | String | Container name |
| image | String | Container image |
| status | String | Container status |
| state | String | Container state |
| created | String | Creation timestamp |
| ports | [Port] | Exposed ports |
| volumes | [Volume] | Mounted volumes |

### Port

Represents a Docker container port mapping.

| Field | Type | Description |
|-------|------|-------------|
| internal | Int | Internal port |
| external | Int | External port |
| protocol | String | Protocol (e.g., "tcp", "udp") |

### Volume

Represents a Docker container volume.

| Field | Type | Description |
|-------|------|-------------|
| host | String | Host path |
| container | String | Container path |
| mode | String | Access mode |

### VM

Represents a virtual machine.

| Field | Type | Description |
|-------|------|-------------|
| id | String | VM ID |
| name | String | VM name |
| status | String | VM status |
| memory | Int | Allocated memory in bytes |
| vcpus | Int | Number of virtual CPUs |
| disks | [VMDisk] | VM disks |
| networks | [VMNetwork] | VM network interfaces |

### VMDisk

Represents a virtual machine disk.

| Field | Type | Description |
|-------|------|-------------|
| name | String | Disk name |
| size | Int | Disk size in bytes |
| type | String | Disk type |

### VMNetwork

Represents a virtual machine network interface.

| Field | Type | Description |
|-------|------|-------------|
| name | String | Interface name |
| type | String | Interface type |
| mac | String | MAC address |

### User

Represents an Unraid user.

| Field | Type | Description |
|-------|------|-------------|
| name | String | Username |
| uid | Int | User ID |
| gid | Int | Group ID |
| groups | [String] | User groups |
| home | String | Home directory |
| shell | String | User shell |

### Share

Represents an Unraid share.

| Field | Type | Description |
|-------|------|-------------|
| name | String | Share name |
| path | String | Share path |
| size | Int | Share size in bytes |
| free | Int | Free space in bytes |
| devices | [String] | Devices used by the share |
| users | [ShareUser] | User access information |

### ShareUser

Represents user access to a share.

| Field | Type | Description |
|-------|------|-------------|
| name | String | Username |
| access | String | Access level |

## Authentication and Authorization

The Unraid GraphQL API uses API keys for authentication. You need to include your API key in the request headers:

```
{
  "Authorization": "Bearer YOUR_API_KEY"
}
```

To generate an API key, go to the Unraid web interface, navigate to Settings > Management Access, and generate a new API key.

## Examples

### Fetching System Information

```graphql
query {
  system {
    version
    uptime
    memory {
      total
      used
      free
    }
    cpu {
      model
      cores
      threads
      usage
    }
  }
}
```

### Starting the Array

```graphql
mutation {
  startArray {
    success
    message
  }
}
```

### Monitoring Container Status

```graphql
subscription {
  containerStatusChanged {
    id
    name
    status
    state
  }
}
```

### Fetching Disk Information

```graphql
query {
  disks {
    name
    size
    temperature
    status
    type
  }
}
```

### Starting a VM

```graphql
mutation {
  startVM(id: "vm_id") {
    success
    message
  }
}
```

This documentation provides a comprehensive overview of the Unraid GraphQL API. For more detailed information, refer to the schema definition or contact Unraid support.
