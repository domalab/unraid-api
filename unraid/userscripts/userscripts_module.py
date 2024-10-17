from typing import List
import json
from ..unraid import Unraid
from .user_script import UserScript, UserScriptJSON
from ..exceptions import ExecutionError, ParseError

class UserScriptsModule:
    """
    Module for managing user scripts on an Unraid server.
    """

    def __init__(self, instance: Unraid):
        """
        Initialize the UserScripts module.

        Args:
            instance: The Unraid instance to use for executing commands.
        """
        self.instance = instance

    async def has_user_scripts_installed(self) -> bool:
        """
        Check if the User Scripts plugin is installed on the Unraid server.

        Returns:
            True if the User Scripts plugin is installed, False otherwise.
        """
        result = await self.instance.execute('test -f /boot/config/plugins/user.scripts.plg')
        return result['code'] == 0

    async def get_user_scripts(self) -> List[UserScript]:
        """
        Get all user scripts on the Unraid server.

        Returns:
            A list of UserScript objects representing the user scripts on the server.

        Raises:
            ExecutionError: If the command to list user scripts fails.
            ParseError: If the user script data cannot be parsed.
        """
        result = await self.instance.execute(self._list_userscripts_command())
        if result['code'] != 0:
            raise ExecutionError("Got non-zero exit code while reading userscripts")

        try:
            parsed_scripts: List[UserScriptJSON] = json.loads(result['stdout'][0])
        except json.JSONDecodeError:
            raise ParseError("Failed to parse user scripts JSON output")

        return [UserScript(self.instance, script_info) for script_info in parsed_scripts]

    def _list_userscripts_command(self) -> str:
        """
        Generate the command to list all user scripts.

        Returns:
            A string containing the bash command to list user scripts.
        """
        return """
        SECOND_ITERATION=""
        SCHEDULE_JSON=$(cat /boot/config/plugins/user.scripts/schedule.json)
        printf "%s" "["
        for script in $(ls /boot/config/plugins/user.scripts/scripts)
        do
            COMBINED_PATH=/boot/config/plugins/user.scripts/scripts/${script%/}/
            SCRIPT_LOCATION=$(printf "%s%s" $COMBINED_PATH script)
            NAME_LOCATION=$(printf "%s%s" $COMBINED_PATH name)
            DESCRIPTION_LOCATION=$(printf "%s%s" $COMBINED_PATH description)
            PID_LOCATION="/tmp/user.scripts/running/${script%/}"
            NAME=""
            DESCRIPTION=""
            SCRIPT=""
            OUTPUT=""
            RUNNING=""
            PID=""
            SCHEDULE=""
            if [[ -d "$COMBINED_PATH" ]]; then
                if [[ -f "$SCRIPT_LOCATION" ]]; then
                    if [[ -f "$NAME_LOCATION" ]]; then
                        NAME=$(cat $NAME_LOCATION)
                    fi
                    if [[ -f "$DESCRIPTION_LOCATION" ]]; then
                        DESCRIPTION=$(cat $DESCRIPTION_LOCATION)
                    fi
                    SCRIPT=$(cat $SCRIPT_LOCATION)
                    if [[ -z "$NAME" ]]; then
                        NAME=${script%/}
                    fi
                    if [[ -f "$PID_LOCATION" ]]; then
                        PID=$(cat $PID_LOCATION)
                        ps --pid $PID > /dev/null
                        if [ "$?" -eq 0 ]; then
                            RUNNING=true
                        else
                            RUNNING=false
                        fi
                    else
                        RUNNING=false
                    fi
                    SCHEDULE=$(echo "$SCHEDULE_JSON" | jq -r --arg script "$SCRIPT_LOCATION" '.[$script]')
                    if [[ -z "$DESCRIPTION" ]]; then
                        OUTPUT=$(jq -n --arg name "$NAME" --arg dirName "${script%/}" --argjson running "$RUNNING" --arg script "$SCRIPT" --argjson schedule "$SCHEDULE" '$ARGS.named')
                    else
                        OUTPUT=$(jq -n --arg name "$NAME" --arg dirName "${script%/}" --argjson running "$RUNNING" --arg script "$SCRIPT" --arg description "$DESCRIPTION" --argjson schedule "$SCHEDULE" '$ARGS.named')
                    fi
                    if [[ -z "$SECOND_ITERATION" ]]; then
                        printf "%s" "$OUTPUT"
                        SECOND_ITERATION=true
                    else
                        printf ",%s" "$OUTPUT"
                    fi
                fi 
            fi
        done
        printf "%s" "]"
        """

    async def create_user_script(self, name: str, script_content: str, description: str = "") -> UserScript:
        """
        Create a new user script.

        Args:
            name: The name of the new script.
            script_content: The content of the script.
            description: An optional description for the script.

        Returns:
            A UserScript object representing the newly created script.

        Raises:
            ExecutionError: If the command to create the user script fails.
        """
        script_dir = f"/boot/config/plugins/user.scripts/scripts/{name}"
        
        commands = [
            f'mkdir -p "{script_dir}"',
            f'echo "{name}" > "{script_dir}/name"',
            f'echo "{description}" > "{script_dir}/description"',
            f'cat > "{script_dir}/script" << EOL\n{script_content}\nEOL',
            f'chmod +x "{script_dir}/script"'
        ]
        
        for cmd in commands:
            result = await self.instance.execute(cmd)
            if result['code'] != 0:
                raise ExecutionError(f"Failed to create user script: {result['stderr']}")
        
        return UserScript(self.instance, UserScriptJSON(
            name=name,
            dirName=name,
            running=False,
            script=script_content,
            description=description,
            schedule=None
        ))

    async def delete_user_script(self, name: str) -> None:
        """
        Delete a user script.

        Args:
            name: The name of the script to delete.

        Raises:
            ExecutionError: If the command to delete the user script fails.
        """
        result = await self.instance.execute(f'rm -rf "/boot/config/plugins/user.scripts/scripts/{name}"')
        if result['code'] != 0:
            raise ExecutionError(f"Failed to delete user script: {result['stderr']}")