# PyUnraid: Python Library for Unraid GraphQL API - Product Requirements Document

## 1. Elevator Pitch

PyUnraid is a comprehensive Python library that provides a clean, intuitive interface to Unraid's GraphQL API. It enables developers to programmatically control and monitor Unraid servers with both synchronous and asynchronous support, strong typing, and intelligent error handling. This library follows Home Assistant integration guidelines while serving broader automation needs for DevOps engineers, self-hosters, and IT professionals who want to script, automate, and extend their Unraid server capabilities.

## 2. Who is this app for

- **Home Assistant Integrators**: Developers creating integrations for the Home Assistant platform
- **DevOps/Self-hosters**: Technical users who want to automate Unraid management tasks
- **Dashboard/App Developers**: Creators building custom UIs for Unraid on mobile/tablet or web
- **IT Admins in Small Offices**: Professionals managing Unraid servers with scripting needs
- **Plugin/Extension Developers**: Those building add-ons that need structured access to Unraid data

## 3. Functional Requirements

### Core API Functionality
- Expose essential Unraid GraphQL API endpoints:
  - **System Control**: startArray, stopArray, shutdown, reboot, parityCheck operations
  - **Disk Management**: Add/remove/mount/unmount disks, get disk info
  - **Notifications**: Create/archive/delete notifications
  - **User & API Key Management**: Tools for access provisioning
  - **Authentication**: Login, connectSignIn with automatic token management
  - **Query Wrappers**: System info, configuration, docker containers, VMs, shares

### Technical Features
- **Authentication Management**:
  - Support for username/password authentication
  - Automatic token refresh and management
  - Optional token persistence
  - Future support for Unraid Connect login

- **API Interaction**:
  - Both synchronous and asynchronous interfaces
  - Auto-reconnect and retry logic for unstable connections
  - Comprehensive error handling with Python exceptions
  - Request/response logging for debugging

- **Data Models**:
  - Strongly-typed Python classes (using Pydantic or dataclasses)
  - Complete object models for all API responses
  - Input validation before sending requests

- **Schema Handling**:
  - Auto schema introspection
  - Client-side validation
  - Warnings for deprecated fields

### Extensibility Features
- CLI tool or REPL interface for direct shell usage
- Extension points for custom GraphQL queries
- Comprehensive documentation and examples

### Package Requirements
- Follows Home Assistant library guidelines:
  - Source distribution packages available
  - Issue tracker enabled
  - OSI-approved license
  - Proper metadata

## 4. User Stories

### As a Home Assistant Integrator
- I want to install the library via PyPI so I can integrate it into my Home Assistant setup
- I want to query system status information so I can display it on my dashboard
- I want to control array operations so I can automate maintenance tasks
- I want to receive notifications so I can alert on important events

### As a DevOps Engineer
- I want to use async functions so I can integrate with my existing automation scripts
- I want to script recurring tasks so I can automate Unraid management
- I want to handle authentication securely so I can safely store credentials
- I want comprehensive error handling so my scripts are robust

### As a Dashboard Developer
- I want to fetch real-time data so I can display it on my custom dashboard
- I want typed responses so I can rely on the data structure
- I want to batch multiple queries so I can minimize API calls

### As an IT Admin
- I want to monitor multiple Unraid servers so I can manage my infrastructure
- I want to schedule backups and maintenance so I can ensure system reliability
- I want to manage users and permissions so I can control access

### As a Plugin Developer
- I want to access Unraid configurations so I can extend functionality
- I want to integrate with existing Unraid features so my plugin works seamlessly
- I want to use a library that handles authentication so I can focus on my plugin logic

## 5. User Interface

As a Python library, PyUnraid does not have a traditional user interface. However, the following interface elements are critical:

### API Interface
- Clean, consistent method naming following Python conventions
- Logical organization of modules based on functionality
- Both object-oriented and functional approaches where appropriate

### Code Examples
```python
# Simple synchronous example
from pyunraid import UnraidClient

# Connect to Unraid server
client = UnraidClient("192.168.1.10")
client.login("username", "password")

# Get system info
system_info = client.get_system_info()
print(f"System version: {system_info.version}")

# Start the array
client.system.start_array()
```

```python
# Async example
import asyncio
from pyunraid.async_client import AsyncUnraidClient

async def main():
    client = AsyncUnraidClient("192.168.1.10")
    await client.login("username", "password")
    
    # Get all Docker containers
    containers = await client.docker.get_containers()
    for container in containers:
        print(f"Container: {container.name}, Status: {container.status}")
    
    # Perform a parity check
    await client.system.start_parity_check()

asyncio.run(main())
```

### CLI Interface (Future Feature)
Command-line interface for direct interaction:
```bash
# Example CLI usage
pyunraid --host 192.168.1.10 --user admin system info
pyunraid --host 192.168.1.10 --user admin docker list
pyunraid --host 192.168.1.10 --user admin array start
```

### Documentation
- Comprehensive API documentation with examples
- Quick start guide
- Advanced usage patterns
- Integration examples (Home Assistant, scripts, etc.)

Software Requirements Specification: PyUnraid
System Design

Client-library architecture for Unraid GraphQL API with comprehensive type coverage
Domain-specific modules organized by API resources (array, disk, docker, VM, notifications, etc.)
Both synchronous and asynchronous operation support
Hierarchical error handling with descriptive exception types
Authentication management with token refresh and persistence
Support for both queries, mutations, and subscriptions (real-time updates)

Architecture Pattern

Repository pattern for API resource abstraction
Facade pattern to simplify complex GraphQL operations
Factory pattern for client instantiation
Strategy pattern for sync/async operation modes
Observer pattern for subscription handling and event notifications

State Management

JWT token authentication state with auto-refresh capability
Connection state tracking with intelligent reconnection
Subscription state management for real-time data streams
Robust caching mechanism for frequently accessed data
Configuration persistence for client settings

Data Flow

Authentication → GraphQL operation construction → Request execution → Response parsing → Object mapping
Automatic schema validation for outgoing requests
Typed response handling with Pydantic models
Real-time data subscription flow with event callbacks
Background processes for token refresh and connection maintenance

Technical Stack

Python 3.9+ as base language
httpx for HTTP requests (supporting both sync and async)
Pydantic for data modeling and validation
graphql-core for schema handling and query construction
typeguard for runtime type checking
pytest for comprehensive testing
AsyncIO for asynchronous operations
websockets for GraphQL subscriptions

Authentication Process

Username/password authentication via login mutation
API key authentication support (createApiKey)
JWT token storage and automatic renewal
Connect SSO integration via connectSignIn mutation
Session persistence with configurable backends
Secure credential handling and token management

Route Design

Hierarchical module organization:

client.py (main synchronous client)
async_client.py (async client)
auth.py (authentication management)
resources/

array.py (array operations)
disk.py (disk management)
docker.py (container operations)
vm.py (virtual machine operations)
notification.py (notification handling)
user.py (user management)
info.py (system information)
config.py (configuration operations)


models/ (Pydantic models for all resource types)
exceptions.py (custom exception hierarchy)
subscription.py (real-time data handling)



API Design

Resource-specific client classes with focused functionality
Complete mapping of all API operations:

Array: startArray, stopArray, addDiskToArray, removeDiskFromArray, etc.
Disk: mountArrayDisk, unmountArrayDisk, clearArrayDiskStatistics, etc.
Parity: startParityCheck, pauseParityCheck, resumeParityCheck, cancelParityCheck
System: shutdown, reboot
User: addUser, deleteUser, addRoleForUser
Docker: container and network operations
VM: domain management
Notifications: createNotification, archiveNotification, etc.


Comprehensive model definitions for all schema types
Support for all scalar types including custom types (JSON, UUID, Long, etc.)
Subscription support for real-time data (array, parityHistory, dockerContainers, etc.)

Database Design ERD

Not applicable for client library
Client-side caching considerations:

Resource-based cache for query results
TTL-based cache invalidation policies
Mutation-aware cache invalidation
Subscription-updated cache for real-time data
Optional disk persistence for offline operation
