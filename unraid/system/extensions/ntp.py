from typing import List
from ...unraid import Unraid
from ...exceptions import ExecutionError

class NtpExtension:
    def __init__(self, instance: Unraid):
        self.instance = instance

    async def ntp(self) -> List[str]:
        result = await self.instance.execute('cat /etc/ntp.conf | grep server')
        if result['code'] != 0:
            raise ExecutionError("Failed to read NTP configuration")
        
        servers = []
        for line in result['stdout']:
            if line.startswith('server') and not line.startswith('server 127.127.1.0'):
                servers.append(line.split()[1])
        
        return servers