# Unraid API

> **IMPORTANT NOTICE:** The Unraid API is currently under active development. It may contain bugs or incomplete features. Use at your own risk and please report any issues you encounter.

Unraid API is a Python library for interacting with and managing Unraid servers. It provides a comprehensive set of tools to handle various aspects of Unraid server management, including system information, Docker containers, virtual machines, user scripts, and more.

## Features

- **System Information**: Retrieve detailed system stats, CPU usage, disk information, and more.
- **Docker Management**: List, start, stop, and manage Docker containers.
- **Virtual Machine Control**: Manage VMs, including starting, stopping, and querying status.
- **User Scripts**: Execute and manage user scripts on the Unraid server.
- **Notifications**: Access and manage Unraid system notifications.
- **Configuration**: View and modify Unraid server configurations.

## Installation

You can install the Unraid API using pip:

```bash
pip install unraid-api
```
## Quick Start
Here's a simple example to get you started:
```python
import asyncio
from unraid_api import Unraid, SSHExecutor

async def main():
    unraid = Unraid(SSHExecutor, {
        'host': 'your_unraid_server_ip',
        'username': 'root',
        'password': 'your_password',
        'port': 22
    })
    
    await unraid.connect()

    # Get system information
    hostname = await unraid.system.get_hostname()
    print(f"Hostname: {hostname}")

    # List Docker containers
    containers = await unraid.docker.list()
    for container in containers:
        print(f"Container: {container.name}, State: {container.state}")

    # List VMs
    vms = await unraid.vm.list()
    for vm in vms:
        print(f"VM: {vm.name}, State: {vm.state}")

    await unraid.disconnect()

asyncio.run(main())
```
## Documentation

For detailed documentation on all available methods and classes, please refer to the inline docstrings in the source code. You can generate HTML documentation using a tool like Sphinx.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Testing

To run the tests, execute:
```bash
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This project is not officially associated with Unraid. Use at your own risk.

## Support This Project

If you find this project useful or it has helped you in any way, please consider supporting its development. Your contributions help maintain and improve the project and allow me to dedicate more time to make it even better.

You can support by:

- Giving a ⭐ if you like it!
- [![Donate with PayPal](https://www.paypalobjects.com/webstatic/en_US/i/buttons/PP_logo_h_150x38.png)](https://www.paypal.com/donate?hosted_button_id=H8QX7K47EXPB4)

Thank you for your support and for helping keep this project going!


