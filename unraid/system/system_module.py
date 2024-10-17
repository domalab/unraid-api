from ..unraid import Unraid
from .extensions import *

class SystemModule:
    """
    Module for retrieving system information from an Unraid server.
    """

    def __init__(self, instance: Unraid):
        """
        Initialize the System module.

        Args:
            instance: The Unraid instance to use for executing commands.
        """
        self.instance = instance
        self.cpu = CpuExtension(instance)
        self.date = DateExtension(instance)
        self.diskfree = DiskfreeExtension(instance)
        self.hostname = HostnameExtension(instance)
        self.info = InfoExtension(instance)
        self.loadaverage = LoadAverageExtension(instance)
        self.lsblk = LsblkExtension(instance)
        self.lscpu = LscpuExtension(instance)
        self.lsusb = LsusbExtension(instance)
        self.ntp = NtpExtension(instance)
        self.smartctl = SmartctlExtension(instance)
        self.syslog = SyslogExtension(instance)
        self.uptime = UptimeExtension(instance)
        self.users = UsersExtension(instance)

    async def usage(self):
        """
        Get CPU usage information.

        Returns:
            CPU usage information as returned by the CpuExtension.

        Raises:
            Any exception raised by the CpuExtension.
        """
        return await self.cpu.usage()

    async def get_hostname(self):
        """
        Get the hostname of the Unraid server.

        Returns:
            The hostname as a string.

        Raises:
            Any exception raised by the HostnameExtension.
        """
        return await self.hostname.get_hostname()

    async def get_system_info(self):
        """
        Get general system information.

        Returns:
            A dictionary containing various system information.

        Raises:
            Any exceptions raised by the individual extensions.
        """
        return {
            'hostname': await self.get_hostname(),
            'uptime': await self.uptime.uptime(),
            'load_average': await self.loadaverage.load_average(),
            'cpu_info': await self.lscpu.lscpu(),
            'disk_usage': await self.diskfree.diskfree(),
        }

    # You can add more convenience methods here as needed