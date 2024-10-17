import json
from typing import Dict, Any
from ...unraid import Unraid
from ...exceptions import ExecutionError, ParseError

class SmartctlExtension:
    def __init__(self, instance: Unraid):
        self.instance = instance

    async def smartctl(self, device_name: str, all: bool = False) -> Dict[str, Any]:
        command = f"smartctl -j {'--all --xall' if all else ''} {device_name}"
        result = await self.instance.execute(command)
        
        # Note: smartctl may return non-zero exit codes for various reasons,
        # so we don't check the exit code here.
        
        try:
            return json.loads(result['stdout'][0])
        except json.JSONDecodeError:
            raise ParseError(f"Failed to parse smartctl JSON output for device {device_name}")