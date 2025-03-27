#!/usr/bin/env python3
"""
Comprehensive test script for PyUnraid Library

This script tests multiple aspects of the PyUnraid library to ensure
it correctly interfaces with the Unraid GraphQL API.
"""

import os
import sys
import logging
import json
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Import the pyunraid library - adjust paths if needed
try:
    from pyunraid.pyunraid.client import UnraidClient
except ImportError:
    sys.path.append("./pyunraid")
    try:
        from pyunraid.client import UnraidClient
    except ImportError:
        logger.error("Could not import UnraidClient. Make sure pyunraid is installed or in the path.")
        sys.exit(1)

# Configuration
UNRAID_HOST = "192-168-20-21.68d348e016dd91382cd87993289f845857f74c1e.myunraid.net"
UNRAID_PORT = 443
UNRAID_API_KEY = "d19cc212ffe54c88397398237f87791e75e8161e9d78c41509910ceb8f07e688"
USE_SSL = True

# Test results tracking
test_results = {
    "passed": [],
    "failed": []
}

def run_test(test_name: str, test_func):
    """Run a test function and track results."""
    logger.info(f"Running test: {test_name}")
    try:
        result = test_func()
        if result:
            test_results["passed"].append(test_name)
            logger.info(f"✅ Test passed: {test_name}")
            return True
        else:
            test_results["failed"].append(test_name)
            logger.error(f"❌ Test failed: {test_name}")
            return False
    except Exception as e:
        test_results["failed"].append(test_name)
        logger.error(f"❌ Test failed: {test_name} - Exception: {str(e)}")
        return False

def get_client():
    """Get a configured UnraidClient instance."""
    client = UnraidClient(
        host=UNRAID_HOST,
        port=UNRAID_PORT,
        use_ssl=USE_SSL,
        verify_ssl=False,
        api_key=UNRAID_API_KEY
    )
    return client

def test_client_initialization():
    """Test client initialization and redirect discovery."""
    client = get_client()
    # Just testing if we can create a client without exceptions
    return client is not None

def test_system_info():
    """Test retrieving system information."""
    client = get_client()
    try:
        info = client.info.get_system_info()
        logger.info(f"System Info: {json.dumps(info, indent=2)}")
        # Check if we got valid data back
        return (
            isinstance(info, dict) and
            "cpu" in info and 
            "memory" in info and 
            "os" in info
        )
    except Exception as e:
        logger.error(f"Error getting system info: {e}")
        return False

def test_array_status():
    """Test retrieving array status."""
    client = get_client()
    try:
        array = client.array.get_array_status()
        logger.info(f"Array Status: {json.dumps(array, indent=2)}")
        # Check if we got valid data back
        return isinstance(array, dict) and "state" in array
    except Exception as e:
        logger.error(f"Error getting array status: {e}")
        return False

def test_disk_info():
    """Test retrieving disk information."""
    client = get_client()
    try:
        disks = client.disk.get_disks()
        logger.info(f"Found {len(disks) if disks else 0} disks")
        return isinstance(disks, list)
    except Exception as e:
        logger.error(f"Error getting disk info: {e}")
        return False

def test_docker_containers():
    """Test retrieving Docker container information."""
    client = get_client()
    try:
        containers = client.docker.get_containers()
        logger.info(f"Found {len(containers) if containers else 0} Docker containers")
        return isinstance(containers, list)
    except Exception as e:
        logger.error(f"Error getting Docker containers: {e}")
        return False

def test_vms():
    """Test retrieving VM information."""
    client = get_client()
    try:
        vms = client.vm.get_vms()
        if "domain" in vms and isinstance(vms["domain"], list):
            logger.info(f"Found {len(vms['domain'])} VMs")
            return True
        else:
            logger.info(f"VM data structure: {json.dumps(vms, indent=2)}")
            return isinstance(vms, dict)
    except Exception as e:
        logger.error(f"Error getting VMs: {e}")
        return False

def test_error_handling():
    """Test error handling with an invalid query."""
    client = get_client()
    try:
        # This should raise a GraphQLError
        client.execute_query("query { nonExistentField }")
        logger.error("Error handling test failed - expected an exception")
        return False
    except Exception as e:
        logger.info(f"Error correctly handled: {e}")
        return True

def test_custom_query():
    """Test executing a custom GraphQL query."""
    client = get_client()
    try:
        query = """
        query {
            info {
                os {
                    platform
                    distro
                    release
                }
            }
        }
        """
        result = client.execute_query(query)
        logger.info(f"Custom query result: {json.dumps(result, indent=2)}")
        return "info" in result and "os" in result["info"]
    except Exception as e:
        logger.error(f"Error executing custom query: {e}")
        return False

def test_notifications():
    """Test retrieving notifications."""
    client = get_client()
    try:
        notifications = client.notification.get_notifications()
        logger.info(f"Found notifications: {json.dumps(notifications, indent=2)}")
        return isinstance(notifications, dict)
    except Exception as e:
        logger.error(f"Error getting notifications: {e}")
        return False

def main():
    """Run all tests and report results."""
    logger.info("Starting PyUnraid library tests")
    logger.info(f"Testing against Unraid server: {UNRAID_HOST}:{UNRAID_PORT}")
    
    # Core functionality tests
    run_test("Client initialization", test_client_initialization)
    run_test("System information", test_system_info)
    run_test("Array status", test_array_status)
    run_test("Disk information", test_disk_info)
    
    # Feature tests
    run_test("Docker containers", test_docker_containers)
    run_test("Virtual machines", test_vms)
    run_test("Notifications", test_notifications)
    
    # Technical tests
    run_test("Error handling", test_error_handling)
    run_test("Custom query", test_custom_query)
    
    # Print summary
    logger.info("\n----- TEST SUMMARY -----")
    logger.info(f"Total tests: {len(test_results['passed']) + len(test_results['failed'])}")
    logger.info(f"Passed: {len(test_results['passed'])}")
    logger.info(f"Failed: {len(test_results['failed'])}")
    
    if test_results["failed"]:
        logger.info("\nFailed tests:")
        for test in test_results["failed"]:
            logger.info(f"  - {test}")
    
    logger.info("\nTest run complete")
    
    # Return success if all tests passed
    return len(test_results["failed"]) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 