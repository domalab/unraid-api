"""Tests for the client module."""
from unraid_api.client import UnraidClient


def test_init(client, host, api_key, port, use_ssl):
    """Test initialization of UnraidClient."""
    assert client.host == host
    assert client.port == port
    assert client.use_ssl == use_ssl
    assert client.verify_ssl is False
    assert client.api_key == api_key
    assert client._base_url == f"https://{host}:{port}/graphql"
    assert client._followed_url is None
    assert client._headers["Content-Type"] == "application/json"
    assert client._headers["x-api-key"] == api_key


def test_set_api_key(client):
    """Test setting API key."""
    client.set_api_key("new-api-key")
    assert client.api_key == "new-api-key"
    assert client._headers["x-api-key"] == "new-api-key"


# We're not testing execute_query directly because it's mocked in the fixture


def test_get_system_info(client):
    """Test get_system_info method."""
    # Call the method
    result = client.get_system_info()

    # Verify the result
    assert result == {"os": {"platform": "linux"}, "cpu": {}, "memory": {}, "system": {}}

    # Verify the call to info.get_system_info
    client.info.get_system_info.assert_called_once()
