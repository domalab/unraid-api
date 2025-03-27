#!/usr/bin/env python3
"""
Test script to verify that the restructured unraid_api package works correctly.
"""

print("Testing unraid_api imports...")

try:
    # Test basic imports
    from unraid_api import UnraidClient, AsyncUnraidClient
    from unraid_api.exceptions import UnraidAPIError, AuthenticationError
    
    print("✅ Basic imports successful")
    
    # Test resources imports
    from unraid_api.resources.array import ArrayResource
    from unraid_api.resources.docker import DockerResource
    from unraid_api.resources.vm import VMResource
    
    print("✅ Resource imports successful")
    
    # Test model imports
    from unraid_api.models.array import ArrayStatus
    from unraid_api.models.docker import DockerContainer
    from unraid_api.models.vm import VM
    
    print("✅ Model imports successful")
    
    # Attempt to create a client instance
    client = UnraidClient(host="example.com", api_key="fake_key", verify_ssl=False)
    print("✅ Client instantiation successful")
    
    # Check if the main components/attributes are available
    assert hasattr(client, "array"), "Client missing array resource"
    assert hasattr(client, "docker"), "Client missing docker resource"
    assert hasattr(client, "vm"), "Client missing vm resource"
    assert hasattr(client, "disk"), "Client missing disk resource"
    assert hasattr(client, "info"), "Client missing info resource"
    assert hasattr(client, "user"), "Client missing user resource"
    assert hasattr(client, "notification"), "Client missing notification resource"
    assert hasattr(client, "config"), "Client missing config resource"
    
    print("✅ Client resources verification successful")
    
    print("\n✅✅ All tests passed successfully!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except AssertionError as e:
    print(f"❌ Assertion error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}") 