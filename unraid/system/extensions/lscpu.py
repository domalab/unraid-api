import json
from typing import Dict
from ...unraid import Unraid
from ...exceptions import ExecutionError, ParseError

class LscpuExtension:
    def __init__(self, instance: Unraid):
        self.instance = instance

    async def lscpu(self) -> Dict[str, str]:
        result = await self.instance.execute('lscpu -J')
        if result['code'] != 0:
            raise ExecutionError("Failed to execute lscpu command")
        
        try:
            data = json.loads(result['stdout'][0])
            return {item['field'].replace(' ', ''): item['data'] for item in data['lscpu']}
        except (json.JSONDecodeError, KeyError):
            raise ParseError("Failed to parse lscpu JSON output")