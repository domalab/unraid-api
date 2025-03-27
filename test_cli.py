#!/usr/bin/env python3
"""
Test script to verify that the CLI module of unraid_api works correctly.
"""

print("Testing unraid_api CLI imports...")

try:
    # Test importing the CLI client
    from unraid_api.cli.client import UnraidAPIClient, main
    
    print("✅ CLI client import successful")
    
    # Verify main function exists
    assert callable(main), "main is not callable"
    print("✅ CLI main function verification successful")
    
    # Test creating a CLI client instance
    cli = UnraidAPIClient(ip="example.com", key="fake_key", verify_ssl=False)
    print("✅ CLI client instantiation successful")
    
    # Verify some methods exist
    assert hasattr(cli, "connect"), "CLI client missing connect method"
    assert hasattr(cli, "execute_with_retry"), "CLI client missing execute_with_retry method"
    assert hasattr(cli, "handle_graphql_error"), "CLI client missing handle_graphql_error method"
    
    print("✅ CLI client methods verification successful")
    
    print("\n✅✅ All CLI tests passed successfully!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except AssertionError as e:
    print(f"❌ Assertion error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}") 