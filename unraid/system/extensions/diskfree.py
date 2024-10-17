from typing import List, Dict
from ...unraid import Unraid
from ...exceptions import ExecutionError

class DiskFreeReturn(Dict):
    fs: str
    blocks: int
    used: int
    available: int
    mounted: str

class DiskfreeExtension:
    def __init__(self, instance: Unraid):
        self.instance = instance

    async def diskfree(self) -> List[DiskFreeReturn]:
        result = await self.instance.execute('df')
        if result['code'] != 0:
            raise ExecutionError("Failed to run df command")

        return self._parse_df_output(result['stdout'][1:])  # Skip header

    def _parse_df_output(self, lines: List[str]) -> List[DiskFreeReturn]:
        return [
            DiskFreeReturn(
                fs=parts[0],
                blocks=int(parts[1]),
                used=int(parts[2]),
                available=int(parts[3]),
                mounted=parts[5]
            )
            for line in lines
            for parts in [line.split()]
            if len(parts) >= 6
        ]