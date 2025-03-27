#!/usr/bin/env python3
"""Test connections to Unraid server with different URL patterns."""

import asyncio
import logging
import urllib3
import httpx

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Server details
UNRAID_HOST = "192.168.20.21"
UNRAID_API_KEY = "d19cc212ffe54c88397398237f87791e75e8161e9d78c41509910ceb8f07e688"

# Headers
HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": UNRAID_API_KEY,
    "Accept": "application/json",
}

# Test URLs - including the redirect URL we discovered
TEST_URLS = [
    # Original URLs
    f"http://{UNRAID_HOST}/graphql",                     
    f"http://{UNRAID_HOST}:80/graphql",                  
    f"http://{UNRAID_HOST}/api/graphql",                 
    
    # Unraid Connect domain we discovered from the redirect
    "https://192-168-20-21.68d348e016dd91382cd87993289f845857f74c1e.myunraid.net/graphql",
    "https://192-168-20-21.68d348e016dd91382cd87993289f845857f74c1e.myunraid.net/api/graphql",
]

# Simple query
QUERY = """
query {
  info {
    os {
      platform
    }
  }
}
"""

async def test_url(url):
    """Test a URL to see if it responds to GraphQL queries."""
    logger.info(f"Testing URL: {url}")
    
    try:
        async with httpx.AsyncClient(verify=False, follow_redirects=True) as client:
            # First try a GET request to see if the endpoint exists
            logger.debug(f"Sending GET request to: {url}")
            get_response = await client.get(url, headers=HEADERS, timeout=10.0)
            logger.debug(f"GET response status: {get_response.status_code}")
            logger.debug(f"GET response body: {get_response.text[:200]}...")
            
            # Then try a POST request with a GraphQL query
            logger.debug(f"Sending POST request to: {url}")
            post_response = await client.post(
                url, 
                json={"query": QUERY},
                headers=HEADERS,
                timeout=10.0
            )
            logger.debug(f"POST response status: {post_response.status_code}")
            logger.debug(f"POST response body: {post_response.text[:200]}...")
            
            if post_response.status_code == 200:
                logger.info(f"✅ SUCCESS: {url} returned 200 OK!")
                logger.info(f"Response: {post_response.text}")
                return True
    except Exception as e:
        logger.error(f"❌ ERROR testing {url}: {e}")
    
    return False

async def main():
    """Run the tests."""
    logger.info("Starting Unraid GraphQL URL tests...")
    
    # Try each URL
    successful_urls = []
    for url in TEST_URLS:
        success = await test_url(url)
        if success:
            successful_urls.append(url)
    
    # Report results
    logger.info("\n\n=== RESULTS ===")
    if successful_urls:
        logger.info(f"Found {len(successful_urls)} working URLs:")
        for url in successful_urls:
            logger.info(f"  - {url}")
    else:
        logger.info("No working URLs found.")
    
    logger.info("Tests completed.")

if __name__ == "__main__":
    asyncio.run(main()) 