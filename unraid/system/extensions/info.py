from typing import Dict
from ...unraid import Unraid
from ...exceptions import ExecutionError, ParseError

class InfoExtension:
    def __init__(self, instance: Unraid):
        self.instance = instance

    async def info(self) -> Dict[str, str]:
        result = await self.instance.execute("dmidecode | grep -A3 '^System Information'")
        if result['code'] != 0:
            raise ExecutionError("Failed to get system info")
        return self._parse_info_output(result['stdout'])

    def _parse_info_output(self, lines: List[str]) -> Dict[str, str]:
        info = {}
        for line in lines:
            parts = line.split(':', 1)
            if len(parts) == 2:
                key, value = parts
                info[key.strip()] = value.strip()
        
        if not info:
            raise ParseError("Failed to parse system info output")
        
        return {
            'manufacturer': info.get('Manufacturer', ''),
            'product_name': info.get('Product Name', ''),
            'version': info.get('Version', '')
        }