from datetime import datetime
from ...unraid import Unraid
from ...exceptions import ExecutionError

class DateExtension:
    def __init__(self, instance: Unraid):
        self.instance = instance

    async def date(self, parsed: bool = False) -> str | datetime:
        result = await self.instance.execute(f"date{' -R' if parsed else ''}")
        if result['code'] != 0:
            raise ExecutionError("Failed to get date")
        if parsed:
            return datetime.strptime(result['stdout'][0], "%a, %d %b %Y %H:%M:%S %z")
        return result['stdout'][0]