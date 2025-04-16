"""Tests for the user resource."""
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from typing import Dict, Any, List, Optional

from unraid_api.resources.user import UserResource, AsyncUserResource
from unraid_api.exceptions import APIError, OperationError


class TestUserResource:
    """Tests for the UserResource class."""

    def setup_method(self):
        """Set up the test."""
        self.client = MagicMock()
        self.resource = UserResource(self.client)

    def test_init(self):
        """Test initialization."""
        assert self.resource.client == self.client

    def test_get_users(self):
        """Test get_users method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "users": [
                {
                    "id": "user1",
                    "username": "testuser",
                    "name": "Test User",
                    "description": "Test user description",
                    "roles": ["admin"],
                    "lastLogin": "2023-01-01T00:00:00Z",
                    "email": "test@example.com"
                }
            ]
        }

        # Call the method
        result = self.resource.get_users()

        # Verify the result
        assert result == self.client.execute_query.return_value["users"]
        self.client.execute_query.assert_called_once_with(
            """
        query GetUsers {
            users {
                id
                username
                name
                description
                roles
                lastLogin
                email
            }
        }
        """
        )

    def test_get_users_error(self):
        """Test get_users method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing users field"):
            self.resource.get_users()

        self.client.execute_query.assert_called_once()

    def test_get_user(self):
        """Test get_user method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "user": {
                "id": "user1",
                "username": "testuser",
                "name": "Test User",
                "description": "Test user description",
                "roles": ["admin"],
                "lastLogin": "2023-01-01T00:00:00Z",
                "email": "test@example.com"
            }
        }

        # Call the method
        result = self.resource.get_user("user1")

        # Verify the result
        assert result == self.client.execute_query.return_value["user"]
        self.client.execute_query.assert_called_once_with(
            """
        query GetUser($id: String!) {
            user(id: $id) {
                id
                username
                name
                description
                roles
                lastLogin
                email
            }
        }
        """,
            {"id": "user1"}
        )

    def test_get_user_error(self):
        """Test get_user method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing user field"):
            self.resource.get_user("user1")

        self.client.execute_query.assert_called_once()

    def test_get_current_user(self):
        """Test get_current_user method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "currentUser": {
                "id": "user1",
                "username": "testuser",
                "name": "Test User",
                "description": "Test user description",
                "roles": ["admin"],
                "lastLogin": "2023-01-01T00:00:00Z",
                "email": "test@example.com"
            }
        }

        # Call the method
        result = self.resource.get_current_user()

        # Verify the result
        assert result == self.client.execute_query.return_value["currentUser"]
        self.client.execute_query.assert_called_once_with(
            """
        query GetCurrentUser {
            currentUser {
                id
                username
                name
                description
                roles
                lastLogin
                email
            }
        }
        """
        )

    def test_get_current_user_error(self):
        """Test get_current_user method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing currentUser field"):
            self.resource.get_current_user()

        self.client.execute_query.assert_called_once()

    def test_create_user_minimal(self):
        """Test create_user method with minimal parameters."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "createUser": {
                "success": True,
                "message": "User created",
                "user": {
                    "id": "user1",
                    "username": "testuser",
                    "name": None,
                    "description": None,
                    "roles": [],
                    "email": None
                }
            }
        }

        # Call the method
        result = self.resource.create_user("testuser", "password123")

        # Verify the result
        assert result == self.client.execute_query.return_value["createUser"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation CreateUser($input: CreateUserInput!) {
            createUser(input: $input) {
                success
                message
                user {
                    id
                    username
                    name
                    description
                    roles
                    email
                }
            }
        }
        """,
            {"input": {"username": "testuser", "password": "password123"}}
        )

    def test_create_user_full(self):
        """Test create_user method with all parameters."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "createUser": {
                "success": True,
                "message": "User created",
                "user": {
                    "id": "user1",
                    "username": "testuser",
                    "name": "Test User",
                    "description": "Test user description",
                    "roles": ["admin"],
                    "email": "test@example.com"
                }
            }
        }

        # Call the method
        result = self.resource.create_user(
            "testuser", 
            "password123", 
            name="Test User", 
            description="Test user description", 
            email="test@example.com", 
            roles=["admin"]
        )

        # Verify the result
        assert result == self.client.execute_query.return_value["createUser"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation CreateUser($input: CreateUserInput!) {
            createUser(input: $input) {
                success
                message
                user {
                    id
                    username
                    name
                    description
                    roles
                    email
                }
            }
        }
        """,
            {
                "input": {
                    "username": "testuser", 
                    "password": "password123",
                    "name": "Test User",
                    "description": "Test user description",
                    "email": "test@example.com",
                    "roles": ["admin"]
                }
            }
        )

    def test_create_user_error(self):
        """Test create_user method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "createUser": {
                "success": False,
                "message": "Username already exists",
                "user": None
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to create user: Username already exists"):
            self.resource.create_user("testuser", "password123")

        self.client.execute_query.assert_called_once()

    def test_update_user_minimal(self):
        """Test update_user method with minimal parameters."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "updateUser": {
                "success": True,
                "message": "User updated",
                "user": {
                    "id": "user1",
                    "username": "testuser",
                    "name": None,
                    "description": None,
                    "roles": [],
                    "email": None
                }
            }
        }

        # Call the method
        result = self.resource.update_user("user1")

        # Verify the result
        assert result == self.client.execute_query.return_value["updateUser"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation UpdateUser($id: String!, $input: UpdateUserInput!) {
            updateUser(id: $id, input: $input) {
                success
                message
                user {
                    id
                    username
                    name
                    description
                    roles
                    email
                }
            }
        }
        """,
            {"id": "user1", "input": {}}
        )

    def test_update_user_full(self):
        """Test update_user method with all parameters."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "updateUser": {
                "success": True,
                "message": "User updated",
                "user": {
                    "id": "user1",
                    "username": "newtestuser",
                    "name": "New Test User",
                    "description": "New test user description",
                    "roles": ["admin", "user"],
                    "email": "newtest@example.com"
                }
            }
        }

        # Call the method
        result = self.resource.update_user(
            "user1", 
            username="newtestuser", 
            name="New Test User", 
            description="New test user description", 
            email="newtest@example.com", 
            roles=["admin", "user"]
        )

        # Verify the result
        assert result == self.client.execute_query.return_value["updateUser"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation UpdateUser($id: String!, $input: UpdateUserInput!) {
            updateUser(id: $id, input: $input) {
                success
                message
                user {
                    id
                    username
                    name
                    description
                    roles
                    email
                }
            }
        }
        """,
            {
                "id": "user1",
                "input": {
                    "username": "newtestuser",
                    "name": "New Test User",
                    "description": "New test user description",
                    "email": "newtest@example.com",
                    "roles": ["admin", "user"]
                }
            }
        )

    def test_update_user_error(self):
        """Test update_user method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "updateUser": {
                "success": False,
                "message": "User not found",
                "user": None
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to update user: User not found"):
            self.resource.update_user("user1", username="newtestuser")

        self.client.execute_query.assert_called_once()

    def test_change_user_password(self):
        """Test change_user_password method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "changeUserPassword": {
                "success": True,
                "message": "Password changed"
            }
        }

        # Call the method
        result = self.resource.change_user_password("user1", "newpassword123")

        # Verify the result
        assert result == self.client.execute_query.return_value["changeUserPassword"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation ChangeUserPassword($id: String!, $password: String!) {
            changeUserPassword(id: $id, password: $password) {
                success
                message
            }
        }
        """,
            {"id": "user1", "password": "newpassword123"}
        )

    def test_change_user_password_error(self):
        """Test change_user_password method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "changeUserPassword": {
                "success": False,
                "message": "User not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to change user password: User not found"):
            self.resource.change_user_password("user1", "newpassword123")

        self.client.execute_query.assert_called_once()

    def test_delete_user(self):
        """Test delete_user method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "deleteUser": {
                "success": True,
                "message": "User deleted"
            }
        }

        # Call the method
        result = self.resource.delete_user("user1")

        # Verify the result
        assert result == self.client.execute_query.return_value["deleteUser"]
        self.client.execute_query.assert_called_once_with(
            """
        mutation DeleteUser($id: String!) {
            deleteUser(id: $id) {
                success
                message
            }
        }
        """,
            {"id": "user1"}
        )

    def test_delete_user_error(self):
        """Test delete_user method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "deleteUser": {
                "success": False,
                "message": "User not found"
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to delete user: User not found"):
            self.resource.delete_user("user1")

        self.client.execute_query.assert_called_once()


@pytest.mark.asyncio
class TestAsyncUserResource:
    """Tests for the AsyncUserResource class."""

    def setup_method(self):
        """Set up the test."""
        self.client = MagicMock()
        # Make execute_query a coroutine
        self.client.execute_query = AsyncMock()
        self.resource = AsyncUserResource(self.client)

    async def test_init(self):
        """Test initialization."""
        assert self.resource.client == self.client

    async def test_get_users(self):
        """Test get_users method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "users": [
                {
                    "id": "user1",
                    "username": "testuser",
                    "name": "Test User",
                    "description": "Test user description",
                    "roles": ["admin"],
                    "lastLogin": "2023-01-01T00:00:00Z",
                    "email": "test@example.com"
                }
            ]
        }

        # Call the method
        result = await self.resource.get_users()

        # Verify the result
        assert result == self.client.execute_query.return_value["users"]
        self.client.execute_query.assert_called_once()

    async def test_get_users_error(self):
        """Test get_users method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing users field"):
            await self.resource.get_users()

        self.client.execute_query.assert_called_once()

    async def test_get_user(self):
        """Test get_user method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "user": {
                "id": "user1",
                "username": "testuser",
                "name": "Test User",
                "description": "Test user description",
                "roles": ["admin"],
                "lastLogin": "2023-01-01T00:00:00Z",
                "email": "test@example.com"
            }
        }

        # Call the method
        result = await self.resource.get_user("user1")

        # Verify the result
        assert result == self.client.execute_query.return_value["user"]
        self.client.execute_query.assert_called_once()

    async def test_get_user_error(self):
        """Test get_user method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing user field"):
            await self.resource.get_user("user1")

        self.client.execute_query.assert_called_once()

    async def test_get_current_user(self):
        """Test get_current_user method."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "currentUser": {
                "id": "user1",
                "username": "testuser",
                "name": "Test User",
                "description": "Test user description",
                "roles": ["admin"],
                "lastLogin": "2023-01-01T00:00:00Z",
                "email": "test@example.com"
            }
        }

        # Call the method
        result = await self.resource.get_current_user()

        # Verify the result
        assert result == self.client.execute_query.return_value["currentUser"]
        self.client.execute_query.assert_called_once()

    async def test_get_current_user_error(self):
        """Test get_current_user method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {}

        # Call the method and verify it raises an exception
        with pytest.raises(APIError, match="Invalid response format: missing currentUser field"):
            await self.resource.get_current_user()

        self.client.execute_query.assert_called_once()

    async def test_create_user_minimal(self):
        """Test create_user method with minimal parameters."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "createUser": {
                "success": True,
                "message": "User created",
                "user": {
                    "id": "user1",
                    "username": "testuser",
                    "name": None,
                    "description": None,
                    "roles": [],
                    "email": None
                }
            }
        }

        # Call the method
        result = await self.resource.create_user("testuser", "password123")

        # Verify the result
        assert result == self.client.execute_query.return_value["createUser"]
        self.client.execute_query.assert_called_once()

    async def test_create_user_full(self):
        """Test create_user method with all parameters."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "createUser": {
                "success": True,
                "message": "User created",
                "user": {
                    "id": "user1",
                    "username": "testuser",
                    "name": "Test User",
                    "description": "Test user description",
                    "roles": ["admin"],
                    "email": "test@example.com"
                }
            }
        }

        # Call the method
        result = await self.resource.create_user(
            "testuser", 
            "password123", 
            name="Test User", 
            description="Test user description", 
            email="test@example.com", 
            roles=["admin"]
        )

        # Verify the result
        assert result == self.client.execute_query.return_value["createUser"]
        self.client.execute_query.assert_called_once()

    async def test_create_user_error(self):
        """Test create_user method with error."""
        # Mock the client's execute_query method
        self.client.execute_query.return_value = {
            "createUser": {
                "success": False,
                "message": "Username already exists",
                "user": None
            }
        }

        # Call the method and verify it raises an exception
        with pytest.raises(OperationError, match="Failed to create user: Username already exists"):
            await self.resource.create_user("testuser", "password123")

        self.client.execute_query.assert_called_once()
