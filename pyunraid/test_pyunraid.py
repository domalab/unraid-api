#!/usr/bin/env python3
"""Test script for PyUnraid."""

import os
import time
import logging
import urllib3
import asyncio
from pyunraid import UnraidClient, AsyncUnraidClient
from pyunraid.exceptions import AuthenticationError, ConnectionError

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to see more detailed logs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Server details
# The server connect hostname from the redirect
UNRAID_CONNECT_HOST = "192-168-20-21.68d348e016dd91382cd87993289f845857f74c1e.myunraid.net"
UNRAID_PORT = 443  # Standard HTTPS port
UNRAID_API_KEY = "d19cc212ffe54c88397398237f87791e75e8161e9d78c41509910ceb8f07e688"

def test_sync():
    """Test synchronous client."""
    logger.info("Starting synchronous tests...")
    
    try:
        # Initialize client with HTTPS protocol and Unraid Connect hostname
        client = UnraidClient(
            host=UNRAID_CONNECT_HOST,
            port=UNRAID_PORT,
            use_ssl=True,     # Use HTTPS
            verify_ssl=False  # Skip SSL verification for self-signed cert
        )
        
        # Authenticate with API key
        logger.info("Authenticating with API key...")
        client.connect_sign_in(UNRAID_API_KEY)
        
        # Test system info
        logger.info("Getting system information...")
        system_info = client.info.get_system_info()
        logger.info(f"System name: {system_info.name}")
        logger.info(f"Unraid version: {system_info.version}")
        
        # Test array
        logger.info("Getting array status...")
        array_status = client.array.get_array_status()
        logger.info(f"Array status: {array_status.status}")
        
        # Test disks
        logger.info("Getting disk information...")
        disks = client.disk.get_disks()
        logger.info(f"Found {len(disks)} disks")
        
        logger.info("Synchronous tests completed successfully")
    
    except AuthenticationError as e:
        logger.error(f"Authentication error: {e}")
    except ConnectionError as e:
        logger.error(f"Connection error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

def main():
    """Run tests."""
    # Run synchronous tests only until we fix the async client
    test_sync()
    
    # Commented out until we fix the async client
    # asyncio.run(test_async())

if __name__ == "__main__":
    main() 