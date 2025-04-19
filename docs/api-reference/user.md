---
title: User API
description: User management with the Unraid API
---

# User API

The User API allows you to manage users on your Unraid server. This includes retrieving, creating, updating, and deleting users.

## Available Methods

### get_users

Retrieves a list of all users on the Unraid server.

```python
def get_users() -> List[UserModel]
```

**Returns**:
A list of `UserModel` objects representing each user.

**Example**:

```python
# Synchronous client
from unraid_api import UnraidClient

client = UnraidClient("192.168.1.10", api_key="your-api-key")
users = client.user.get_users()

for user in users:
    print(f"User: {user.username}, Role: {user.role}")
```

```python
# Asynchronous client
import asyncio
from unraid_api import AsyncUnraidClient

async def main():
    client = AsyncUnraidClient("192.168.1.10", api_key="your-api-key")
    users = await client.user.get_users()
    
    for user in users:
        print(f"User: {user.username}, Role: {user.role}")

asyncio.run(main())
```

### get_user

Retrieves information about a specific user.

```python
def get_user(username: str) -> UserModel
```

**Parameters**:

- `username` (str): The username of the user to retrieve.

**Returns**:
A `UserModel` object representing the specified user.

**Raises**:

- `APIError`: If the user does not exist or cannot be accessed.

**Example**:

```python
# Get a specific user
user = client.user.get_user(username="admin")
print(f"User: {user.username}, Role: {user.role}")
```

### create_user

Creates a new user on the Unraid server.

```python
def create_user(username: str, password: str, role: str = "user", description: str = "") -> UserModel
```

**Parameters**:

- `username` (str): The username for the new user.
- `password` (str): The password for the new user.
- `role` (str, optional): The role to assign to the user. Default is "user".
- `description` (str, optional): A description for the user. Default is an empty string.

**Returns**:
A `UserModel` object representing the newly created user.

**Raises**:

- `APIError`: If the user cannot be created.

**Example**:

```python
# Create a new user
new_user = client.user.create_user(
    username="john_doe",
    password="secure_password",
    role="administrator",
    description="John Doe - IT Department"
)
print(f"Created user: {new_user.username}")
```

### update_user

Updates an existing user on the Unraid server.

```python
def update_user(username: str, password: str = None, role: str = None, description: str = None) -> UserModel
```

**Parameters**:

- `username` (str): The username of the user to update.
- `password` (str, optional): The new password for the user. If `None`, the password is not changed.
- `role` (str, optional): The new role for the user. If `None`, the role is not changed.
- `description` (str, optional): The new description for the user. If `None`, the description is not changed.

**Returns**:
A `UserModel` object representing the updated user.

**Raises**:

- `APIError`: If the user does not exist or cannot be updated.

**Example**:

```python
# Update an existing user
updated_user = client.user.update_user(
    username="john_doe",
    password="new_secure_password",
    role="user",
    description="John Doe - Marketing Department"
)
print(f"Updated user: {updated_user.username}")
```

### delete_user

Deletes a user from the Unraid server.

```python
def delete_user(username: str) -> bool
```

**Parameters**:

- `username` (str): The username of the user to delete.

**Returns**:
`True` if the user was successfully deleted, `False` otherwise.

**Raises**:

- `APIError`: If the user does not exist or cannot be deleted.

**Example**:

```python
# Delete a user
result = client.user.delete_user(username="john_doe")
if result:
    print("User deleted successfully")
```

### change_password

Changes the password for a user.

```python
def change_password(username: str, password: str) -> bool
```

**Parameters**:

- `username` (str): The username of the user.
- `password` (str): The new password for the user.

**Returns**:
`True` if the password was successfully changed, `False` otherwise.

**Raises**:

- `APIError`: If the user does not exist or the password cannot be changed.

**Example**:

```python
# Change a user's password
result = client.user.change_password(
    username="john_doe",
    password="very_secure_new_password"
)
if result:
    print("Password changed successfully")
```

## Model Reference

### UserModel

Represents a user on the Unraid server.

**Properties**:

| Name | Type | Description |
|------|------|-------------|
| `username` | str | The user's username |
| `role` | str | The user's role (e.g., "administrator", "user") |
| `description` | str | User description |
| `created_at` | datetime | When the user was created |
| `last_login` | datetime | Last login timestamp |
| `permissions` | List[str] | List of user permissions | 