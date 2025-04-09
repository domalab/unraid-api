---
layout: default
title: Authentication
parent: Getting Started
nav_order: 2
---

# Authentication

Before you can use the Unraid API library, you need to enable the GraphQL API on your Unraid server and generate an API key for authentication.

## Enabling the GraphQL API

The GraphQL API is not enabled by default on Unraid servers. To enable it:

1. SSH into your Unraid server or access the terminal from the web UI
2. Run the following command to enable developer mode:
   ```bash
   unraid-api developer
   ```
3. Follow the prompts to enable the GraphQL sandbox
4. Once enabled, you can access the GraphQL playground at:
   ```
   http://YOUR_SERVER_IP/graphql
   ```

## Generating an API Key

API keys are used for authentication with the Unraid GraphQL API. To generate an API key:

1. SSH into your Unraid server or access the terminal from the web UI
2. Run the following command:
   ```bash
   unraid-api apikey --create
   ```
3. Follow the prompts to set:
   - Name (a descriptive name for the API key)
   - Description (optional)
   - Roles (the permissions the API key will have)
   - Permissions (specific permissions for the API key)
4. The command will output an API key. **Save this key securely** as it will not be shown again.

## API Key Security

API keys provide access to your Unraid server, so it's important to keep them secure:

- Store API keys securely and never expose them in public repositories or client-side code
- Use different API keys for different applications or services
- Limit the permissions of each API key to only what is needed
- Rotate API keys periodically
- Revoke API keys that are no longer needed

## Using API Keys with the Unraid API Library

Once you have an API key, you can use it to authenticate with the Unraid API library:

```python
from unraid_api import UnraidClient

# Connect to Unraid server with API key
client = UnraidClient("192.168.1.10", api_key="your-api-key")

# Test the connection
system_info = client.info.get_system_info()
print(f"Connected to Unraid version: {system_info.get('os', {}).get('release')}")
```

## Handling Redirects

Unraid servers often redirect to myunraid.net domains. The Unraid API library automatically handles these redirects, so you don't need to worry about them.

For example, if your server redirects from `http://192.168.1.10/graphql` to `https://192-168-1-10.myunraid.net/graphql`, the library will follow the redirect and use the new URL for all subsequent requests.

## Next Steps

Now that you have enabled the GraphQL API and generated an API key, you can:

1. [Connect to your Unraid server](basic-usage)
2. [Handle errors](error-handling)
3. [Explore the API reference]({{ site.baseurl }}/content/api/overview)
