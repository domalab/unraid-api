from datetime import datetime, timedelta
from ...unraid import Unraid
from ...exceptions import ExecutionError, ParseError

class UptimeExtension:
    def __init__(self, instance: Unraid):
        self.instance = instance

    async def uptime(self) -> dict:
        result = await self.instance.execute('uptime -s')
        if result['code'] != 0:
            raise ExecutionError("Failed to get uptime")
        
        try:
            up_since = datetime.strptime(result['stdout'][0], "%Y-%m-%d %H:%M:%S")
            current_time = datetime.now()
            uptime_duration = current_time - up_since
            
            return {
                'up_since': up_since,
                'uptime': str(uptime_duration),
                'days': uptime_duration.days,
                'hours': uptime_duration.seconds // 3600,
                'minutes': (uptime_duration.seconds % 3600) // 60,
                'seconds': uptime_duration.seconds % 60
            }
        except ValueError:
            raise ParseError("Failed to parse uptime output")