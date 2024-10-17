from typing import Dict
from ...unraid import Unraid
from ...exceptions import ExecutionError, ParseError

class LoadAverageExtension:
    def __init__(self, instance: Unraid):
        self.instance = instance

    async def load_average(self) -> Dict[str, float | int]:
        result = await self.instance.execute('cat /proc/loadavg')
        if result['code'] != 0:
            raise ExecutionError("Failed to get load average")
        return self._parse_load_average(result['stdout'][0])

    def _parse_load_average(self, input: str) -> Dict[str, float | int]:
        parts = input.split()
        if len(parts) < 5:
            raise ParseError("Invalid load average format")
        
        one, five, fifteen, processes, last_pid = parts
        current, total = processes.split('/')

        return {
            'load_1': float(one),
            'load_5': float(five),
            'load_15': float(fifteen),
            'current_processes': int(current),
            'total_processes': int(total),
            'last_pid': int(last_pid)
        }

    async def on_load_average(self, listener, options=None):
        refresh = options.get('refresh', 1) if options else 1
        command = f"while true; do cat /proc/loadavg; sleep {refresh}; done"
        
        event, future = await self.instance.execute_stream(command)
        
        async def reader():
            while True:
                await event.wait()
                load = self._parse_load_average(await self.instance.read_stream_output())
                await listener(load)
                event.clear()

        return future