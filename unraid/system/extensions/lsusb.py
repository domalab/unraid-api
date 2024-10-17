import re
from typing import List, Dict
from ...unraid import Unraid
from ...exceptions import ExecutionError, ParseError

class LsusbExtension:
    def __init__(self, instance: Unraid):
        self.instance = instance

    async def lsusb(self) -> List[Dict[str, str]]:
        result = await self.instance.execute('lsusb')
        if result['code'] != 0:
            raise ExecutionError("Failed to execute lsusb command")
        
        return self._parse_lsusb_output(result['stdout'])

    def _parse_lsusb_output(self, lines: List[str]) -> List[Dict[str, str]]:
        regex = re.compile(r'Bus (\d+) Device (\d+): ID (\w+):(\w+) (.+)')
        devices = []

        for line in lines:
            match = regex.match(line)
            if match:
                devices.append({
                    'bus': match.group(1),
                    'device': match.group(2),
                    'id': f"{match.group(3)}:{match.group(4)}",
                    'name': match.group(5)
                })
            else:
                raise ParseError(f"Failed to parse lsusb line: {line}")

        return devices