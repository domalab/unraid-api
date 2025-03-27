#!/usr/bin/env python3
"""Test script for PyUnraid."""

import os
import time
import logging
import urllib3
import httpx
import json
import asyncio

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

# GraphQL endpoint
GRAPHQL_URL = f"https://{UNRAID_CONNECT_HOST}/graphql"

# Headers with API key
HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": UNRAID_API_KEY,
    "Accept": "application/json"
}

def test_direct_query():
    """Test a direct GraphQL query to the Unraid API."""
    logger.info("Testing direct GraphQL query...")
    
    # Simple system info query
    query = """
    query {
      info {
        os {
          platform
          distro
          release
          uptime
        }
        cpu {
          manufacturer
          brand
          cores
          threads
        }
        memory {
          total
          free
          used
          active
          available
        }
      }
    }
    """
    
    try:
        # Send the query
        logger.info(f"Sending query to {GRAPHQL_URL}")
        response = httpx.post(
            GRAPHQL_URL, 
            json={"query": query},
            headers=HEADERS,
            verify=False,  # Skip SSL verification
            timeout=10.0
        )
        
        # Check the response
        logger.info(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            logger.info("Query successful!")
            data = response.json()
            logger.info(f"Response data: {json.dumps(data, indent=2)}")
            return True
        else:
            logger.error(f"Query failed: {response.text}")
            return False
    
    except Exception as e:
        logger.error(f"Error during query: {e}")
        return False

def main():
    """Run tests."""
    # Test direct GraphQL query
    test_direct_query()

if __name__ == "__main__":
    main() 