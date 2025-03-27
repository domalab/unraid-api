#!/usr/bin/env python3
"""
Direct Testing Script for Unraid GraphQL API

This script performs direct GraphQL queries against the Unraid API
to verify which endpoints and queries are working correctly.
"""

import os
import sys
import logging
import json
import httpx
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Configuration
UNRAID_HOST = "192-168-20-21.68d348e016dd91382cd87993289f845857f74c1e.myunraid.net"
UNRAID_PORT = 443
UNRAID_API_KEY = "d19cc212ffe54c88397398237f87791e75e8161e9d78c41509910ceb8f07e688"
USE_SSL = True

def execute_query(query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Execute a GraphQL query against the Unraid API."""
    url = f"{'https' if USE_SSL else 'http'}://{UNRAID_HOST}:{UNRAID_PORT}/graphql"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": UNRAID_API_KEY
    }
    
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    
    try:
        with httpx.Client(verify=False) as client:
            response = client.post(
                url,
                json=payload,
                headers=headers,
                timeout=15
            )
            
            logger.info(f"Query: {query.strip()}")
            logger.info(f"Response status: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"Error response: {response.text}")
                return {"error": response.text}
            
            return response.json()
    except Exception as e:
        logger.error(f"Request error: {e}")
        return {"error": str(e)}

def test_system_info():
    """Test the system info query."""
    query = """
    query {
        info {
            os {
                platform
                distro
                release
                kernel
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
            }
        }
    }
    """
    
    result = execute_query(query)
    
    if "error" in result:
        logger.error("System info query failed")
        return False
    
    logger.info(f"System info result: {json.dumps(result, indent=2)}")
    return True

def test_simple_info():
    """Test a simplified system info query."""
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
    
    result = execute_query(query)
    
    if "error" in result:
        logger.error("Simple info query failed")
        return False
    
    logger.info(f"Simple info result: {json.dumps(result, indent=2)}")
    return True

def test_array_status():
    """Test the array status query."""
    query = """
    query {
        array {
            name
            started
            size
            used
            free
        }
    }
    """
    
    result = execute_query(query)
    
    if "error" in result:
        logger.error("Array status query failed")
        return False
    
    logger.info(f"Array status result: {json.dumps(result, indent=2)}")
    return True

def test_disks():
    """Test the disks query."""
    query = """
    query {
        disks {
            id
            name
            size
        }
    }
    """
    
    result = execute_query(query)
    
    if "error" in result:
        logger.error("Disks query failed")
        return False
    
    logger.info(f"Disks result: {json.dumps(result, indent=2)}")
    return True

def test_docker_containers():
    """Test the docker containers query."""
    query = """
    query {
        dockerContainers {
            id
            names
            image
            state
        }
    }
    """
    
    result = execute_query(query)
    
    if "error" in result:
        logger.error("Docker containers query failed")
        return False
    
    logger.info(f"Docker containers result: {json.dumps(result, indent=2)}")
    return True

def test_notifications():
    """Test the notifications query."""
    query = """
    query {
        notifications {
            overview {
                unread {
                    total
                }
            }
        }
    }
    """
    
    result = execute_query(query)
    
    if "error" in result:
        logger.error("Notifications query failed")
        return False
    
    logger.info(f"Notifications result: {json.dumps(result, indent=2)}")
    return True

def test_vms():
    """Test the VMs query."""
    query = """
    query {
        vms {
            domain {
                uuid
                name
                state
            }
        }
    }
    """
    
    result = execute_query(query)
    
    if "error" in result:
        logger.error("VMs query failed")
        return False
    
    logger.info(f"VMs result: {json.dumps(result, indent=2)}")
    return True

def test_schema():
    """Test the schema introspection query."""
    query = """
    query {
        __schema {
            queryType {
                name
                fields {
                    name
                }
            }
        }
    }
    """
    
    result = execute_query(query)
    
    if "error" in result:
        logger.error("Schema introspection query failed")
        return False
    
    logger.info(f"Schema introspection result: {json.dumps(result, indent=2)}")
    return True

def main():
    """Run all test queries."""
    logger.info("Starting direct GraphQL query tests")
    logger.info(f"Testing against Unraid server: {UNRAID_HOST}:{UNRAID_PORT}")
    
    # First, try a schema introspection query to understand the API structure
    logger.info("\n===== Testing schema introspection =====")
    test_schema()
    
    # Then test specific queries
    logger.info("\n===== Testing simple info query =====")
    test_simple_info()
    
    logger.info("\n===== Testing system info query =====")
    test_system_info()
    
    logger.info("\n===== Testing array status query =====")
    test_array_status()
    
    logger.info("\n===== Testing disks query =====")
    test_disks()
    
    logger.info("\n===== Testing docker containers query =====")
    test_docker_containers()
    
    logger.info("\n===== Testing VMs query =====")
    test_vms()
    
    logger.info("\n===== Testing notifications query =====")
    test_notifications()
    
    logger.info("\nAll tests completed")

if __name__ == "__main__":
    main() 