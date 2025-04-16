"""Async tests for the AsyncAuthManager class."""
import os
import tempfile

import pytest
import pytest_asyncio

from unraid_api.async_client import AsyncAuthManager


@pytest_asyncio.fixture
async def temp_file():
    """Create a temporary file and clean it up after the test."""
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()

    # Create a mock token file
    with open(temp_file.name, 'w') as f:
        f.write('{}')

    yield temp_file

    # Clean up
    if os.path.exists(temp_file.name):
        os.unlink(temp_file.name)


@pytest_asyncio.fixture
async def auth_manager(temp_file):
    """Return a test AsyncAuthManager instance."""
    return AsyncAuthManager(
        host="test-host",
        api_key="test-api-key",
        port=443,
        use_ssl=True,
        token_persistence_path=temp_file.name
    )


@pytest.mark.asyncio
async def test_init(auth_manager):
    """Test initialization of AsyncAuthManager."""
    assert auth_manager.host == "test-host"
    assert auth_manager.port == 443
    assert auth_manager.use_ssl is True
    assert auth_manager.token_persistence_path is not None
    assert auth_manager.api_key == "test-api-key"
    assert auth_manager._base_url == "https://test-host:443/graphql"


@pytest.mark.asyncio
async def test_is_authenticated_false(auth_manager):
    """Test is_authenticated returns False when not authenticated."""
    auth_manager.api_key = ""
    assert not auth_manager.is_authenticated()


@pytest.mark.asyncio
async def test_is_authenticated_true(auth_manager):
    """Test is_authenticated returns True when authenticated."""
    assert auth_manager.is_authenticated()


@pytest.mark.asyncio
async def test_get_auth_headers(auth_manager):
    """Test get_auth_headers returns correct headers."""
    # Call the method
    headers = await auth_manager.get_auth_headers()

    # Verify the result
    assert headers == {"x-api-key": "test-api-key"}




