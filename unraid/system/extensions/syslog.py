from typing import List
from ...unraid import Unraid
from ...exceptions import ExecutionError

class SyslogExtension:
    def __init__(self, instance: Unraid):
        self.instance = instance

    async def syslog(self, lines: int = None) -> List[str]:
        command = f"tail {'--lines ' + str(lines) if lines else ''} /var/log/syslog"
        result = await self.instance.execute(command)
        if result['code'] != 0:
            raise ExecutionError("Failed to read syslog")
        return result['stdout']

    async def on_syslog(self, listener):
        command = "tail -f -n 0 /var/log/syslog"
        event, future = await self.instance.execute_stream(command)
        
        async def reader():
            while True:
                await event.wait()
                line = await self.instance.read_stream_output()
                await listener(line)
                event.clear()

        return future