from ...unraid import Unraid
from ...exceptions import ExecutionError

class HostnameExtension:
    def __init__(self, instance: Unraid):
        self.instance = instance

    async def get_hostname(self) -> str:
        result = await self.instance.execute('hostname')
        if result['code'] != 0:
            raise ExecutionError("Failed to get hostname")
        return result['stdout'][0]