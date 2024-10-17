import re
from typing import List, Dict
from ...unraid import Unraid
from ...exceptions import ExecutionError, ParseError

class UsersExtension:
    def __init__(self, instance: Unraid):
        self.instance = instance

    async def users(self) -> List[Dict[str, str]]:
        result = await self.instance.execute('cat /etc/passwd')
        if result['code'] != 0:
            raise ExecutionError("Failed to read user information")
        
        return self._parse_passwd_file(result['stdout'])

    def _parse_passwd_file(self, lines: List[str]) -> List[Dict[str, str]]:
        users = []
        for line in lines:
            parts = line.split(':')
            if len(parts) == 7:
                users.append({
                    'username': parts[0],
                    'password': parts[1],
                    'uid': parts[2],
                    'gid': parts[3],
                    'full_name': parts[4],
                    'home': parts[5],
                    'shell': parts[6]
                })
            else:
                raise ParseError(f"Invalid format in /etc/passwd line: {line}")
        return users