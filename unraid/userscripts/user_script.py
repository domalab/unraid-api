from typing import Optional, Callable, Awaitable
import asyncio
from pydantic import BaseModel
from ..unraid import Unraid
from ..exceptions import ExecutionError

class Schedule(BaseModel):
    script: str
    frequency: str
    id: str
    custom: str

class UserScriptJSON(BaseModel):
    name: str
    dirName: str
    running: bool
    script: str
    description: Optional[str]
    schedule: Optional[Schedule]

class UserScript:
    """
    Represents a user script on the Unraid server.
    """

    def __init__(self, instance: Unraid, user_script_json: UserScriptJSON):
        self.instance = instance
        self.name = user_script_json.name
        self.dir_name = user_script_json.dirName
        self.running_cache = user_script_json.running
        self.script = user_script_json.script
        self.description = user_script_json.description
        self.schedule = user_script_json.schedule
        self.foreground_only = False
        self.background_only = False
        self.array_started = False
        self.clear_log = False
        self.no_parity = False
        self.argument_description = None
        self.argument_default = None
        self.interpreter = '/bin/bash'
        
        self._parse_script_header()

    def _parse_script_header(self):
        """Parse the script header for metadata."""
        for line in self.script.split('\n'):
            if line.startswith('#!'):
                self.interpreter = line[2:].strip()
            elif line.startswith('#'):
                parts = line[1:].split('=', 1)
                if len(parts) == 2:
                    key, value = parts
                    key = key.strip().lower()
                    value = value.strip()
                    if key == 'name':
                        self.name = value
                    elif key == 'description':
                        self.description = value
                    elif key == 'argumentdescription':
                        self.argument_description = value
                    elif key == 'argumentdefault':
                        self.argument_default = value
                    elif key == 'foregroundonly':
                        self.foreground_only = value.lower() == 'true'
                    elif key == 'backgroundonly':
                        self.background_only = value.lower() == 'true'
                    elif key == 'arraystarted':
                        self.array_started = value.lower() == 'true'
                    elif key == 'clearlog':
                        self.clear_log = value.lower() == 'true'
                    elif key == 'noparity':
                        self.no_parity = value.lower() == 'true'
            else:
                break

    async def running(self, bypass_cache: bool = False) -> bool:
        """
        Check if the script is currently running.

        Args:
            bypass_cache: If True, check the actual running state instead of using the cached value.

        Returns:
            True if the script is running, False otherwise.

        Raises:
            ExecutionError: If the command to check the script's running state fails.
        """
        if self.foreground_only:
            return False
        if self.running_cache and not bypass_cache:
            return self.running_cache
        
        result = await self.instance.execute(self._is_running_command())
        if result['code'] != 0:
            raise ExecutionError("Failed to check if user script is running")
        
        self.running_cache = 'true' in result['stdout'][0].lower()
        return self.running_cache

    async def start_background(self):
        """
        Start the script in the background.

        Raises:
            ExecutionError: If the script fails to start or if it's not allowed to run in the background.
        """
        if self.foreground_only:
            raise ExecutionError("This script doesn't support background execution")
        
        is_running = await self.running(True)
        if is_running:
            return

        result = await self.instance.execute(self._convert_script_command())
        if result['code'] != 0:
            raise ExecutionError("Failed to convert user script")

        temp_path = result['stdout'][0].strip()
        if not temp_path:
            raise ExecutionError("Failed to get temporary script path")

        result = await self.instance.execute(self._run_converted_script_command(temp_path))
        if result['code'] != 0:
            raise ExecutionError("Failed to run converted user script")

        await self.running(True)

    async def abort(self):
        """
        Abort the running script.

        Raises:
            ExecutionError: If the abort command fails or if the script is not running.
        """
        is_running = await self.running(True)
        if not is_running:
            return

        result = await self.instance.execute(self._abort_script_command())
        if result['code'] != 0:
            raise ExecutionError("Failed to abort user script")

        await self.running(True)

    async def start(self, input_parameter_callback: Optional[Callable[[str, Optional[str]], Awaitable[str]]] = None):
        """
        Start the script in the foreground.

        Args:
            input_parameter_callback: An optional async function that will be called if the script requires input.

        Returns:
            A tuple containing an Event for new output, a Future for the command completion, and a cancel function.

        Raises:
            ExecutionError: If the script fails to start or if it's not allowed to run in the foreground.
        """
        if self.background_only:
            raise ExecutionError("This script doesn't support foreground execution")

        is_running = await self.running(True)
        if is_running:
            raise ExecutionError("Script is already running in the background")

        if self.argument_description and self.argument_default and not input_parameter_callback:
            input_parameter_callback = lambda desc, default: asyncio.to_thread(lambda: default)

        if self.argument_description and not input_parameter_callback:
            raise ExecutionError("Missing input callback for user script")

        argument = ""
        if self.argument_description:
            argument = await input_parameter_callback(self.argument_description, self.argument_default)

        script = f"{self.interpreter} /boot/config/plugins/user.scripts/scripts/{self.dir_name}/script"
        command = f"{script} {argument}" if argument else script

        event, future = await self.instance.execute_stream(self._run_foreground_script_command(command))

        async def cancel():
            await self.abort()

        return event, future, cancel

    def _is_running_command(self) -> str:
        return f"""
        if [[ -f "/tmp/user.scripts/running/{self.dir_name}" ]]; then
            pid=$(cat /tmp/user.scripts/running/{self.dir_name})
            ps --pid $pid > /dev/null
            if [ "$?" -eq 0 ]; then
                echo true
                exit 0
            fi
        fi
        echo false
        """

    def _convert_script_command(self) -> str:
        return f'echo | php -B "$_POST[\'action\'] = \'convertScript\'; $_POST[\'path\'] = \'/boot/config/plugins/user.scripts/scripts/{self.dir_name}/script\';" -F /usr/local/emhttp/plugins/user.scripts/exec.php'

    def _run_converted_script_command(self, tmp_location: str) -> str:
        return f'echo /usr/local/emhttp/plugins/user.scripts/startBackground.php "{tmp_location}" | at NOW -M > /dev/null 2>&1'

    def _abort_script_command(self) -> str:
        return f'echo | php -B "$_POST[\'action\'] = \'abortScript\'; $_POST[\'name\'] = \'{self.dir_name}\';" -F /usr/local/emhttp/plugins/user.scripts/exec.php'

    def _run_foreground_script_command(self, command: str) -> str:
        return f"export HOME=$(grep $(whoami) /etc/passwd | cut -d: -f 6) && source ${{HOME}}/.bashrc && {command}"

    def to_dict(self) -> dict:
        """
        Convert the UserScript object to a dictionary.

        Returns:
            A dictionary representation of the UserScript.
        """
        return {
            'name': self.name,
            'dir_name': self.dir_name,
            'running': self.running_cache,
            'description': self.description,
            'schedule': self.schedule.dict() if self.schedule else None,
            'foreground_only': self.foreground_only,
            'background_only': self.background_only,
            'array_started': self.array_started,
            'clear_log': self.clear_log,
            'no_parity': self.no_parity,
            'argument_description': self.argument_description,
            'argument_default': self.argument_default,
            'interpreter': self.interpreter
        }