import json
from typing import Dict, Any
from ...unraid import Unraid
from ...exceptions import ExecutionError, ParseError

class LsblkExtension:
    def __init__(self, instance: Unraid):
        self.instance = instance

    async def lsblk(self, all: bool = False) -> Dict[str, Any]:
        command = f"lsblk -J {'--all' if all else ''}"
        result = await self.instance.execute(command)
        if result['code'] != 0:
            raise ExecutionError("Failed to execute lsblk command")
        
        try:
            return json.loads(result['stdout'][0])
        except json.JSONDecodeError:
            raise ParseError("Failed to parse lsblk JSON output")