from typing import Dict, List
from pydantic import BaseModel
from ..unraid import Unraid
from ..exceptions import ExecutionError, ParseError

class IdentConfig(BaseModel):
    name: str
    timezone: str
    comment: str
    security: str
    workgroup: str
    domain: str
    domain_short: str
    hide_dot_files: str
    local_master: str
    enable_fruit: str
    use_netbios: str
    use_wsd: str
    wsd_opt: str
    use_ntp: str
    ntp_server1: str
    ntp_server2: str
    ntp_server3: str
    ntp_server4: str
    domain_login: str
    domain_passwd: str
    sys_model: str
    sys_array_slots: str
    use_ssl: str
    port: str
    port_ssl: str
    local_tld: str
    bind_mgt: str
    use_telnet: str
    port_telnet: str
    use_ssh: str
    port_ssh: str
    use_upnp: str
    start_page: str

class UnraidModule:
    """
    Module for managing Unraid-specific configurations.
    """

    def __init__(self, instance: Unraid):
        """
        Initialize the Unraid module.

        Args:
            instance: The Unraid instance to use for executing commands.
        """
        self.instance = instance

    async def get_case_model(self) -> str:
        """
        Get the case model of the Unraid server.

        Returns:
            The case model as a string.

        Raises:
            ExecutionError: If the command to get the case model fails.
        """
        result = await self.instance.execute('cat /boot/config/plugins/dynamix/case-model.cfg')
        if result['code'] != 0:
            raise ExecutionError("Failed to get case model")
        return result['stdout'][0]

    async def set_case_model(self, case_model: str):
        """
        Set the case model of the Unraid server.

        Args:
            case_model: The case model to set.

        Raises:
            ExecutionError: If the command to set the case model fails.
        """
        result = await self.instance.execute(f'echo {case_model} > /boot/config/plugins/dynamix/case-model.cfg')
        if result['code'] != 0:
            raise ExecutionError("Failed to set case model")

    async def get_ident_config(self) -> IdentConfig:
        """
        Get the ident configuration of the Unraid server.

        Returns:
            An IdentConfig object containing the ident configuration.

        Raises:
            ExecutionError: If the command to get the ident config fails.
            ParseError: If parsing the ident config fails.
        """
        result = await self.instance.execute('cat /boot/config/ident.cfg')
        if result['code'] != 0:
            raise ExecutionError("Failed to get ident config")
        return self._parse_ident_config(result['stdout'])

    def _parse_ident_config(self, lines: List[str]) -> IdentConfig:
        """
        Parse the ident configuration from raw config lines.

        Args:
            lines: The raw lines from the ident.cfg file.

        Returns:
            An IdentConfig object containing the parsed configuration.

        Raises:
            ParseError: If parsing the config fails.
        """
        config = {}
        try:
            for line in lines:
                if line.startswith('#'):
                    continue
                key, value = line.split('=', 1)
                config[self._snake_to_camel(key.lower())] = value.strip().strip('"')
            return IdentConfig(**config)
        except ValueError as e:
            raise ParseError(f"Failed to parse ident config: {str(e)}")

    def _snake_to_camel(self, snake_str: str) -> str:
        """
        Convert a snake_case string to camelCase.

        Args:
            snake_str: The snake_case string to convert.

        Returns:
            The camelCase version of the input string.
        """
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    async def set_ident_config(self, config: Dict[str, str]):
        """
        Set the ident configuration of the Unraid server.

        Args:
            config: A dictionary containing the configuration key-value pairs to set.

        Raises:
            ExecutionError: If the command to set the ident config fails.
        """
        current_config = await self.get_ident_config()
        updated_config = current_config.dict()
        updated_config.update(config)

        config_lines = [f'{key.upper()}="{value}"' for key, value in updated_config.items()]
        config_content = '\n'.join(config_lines)

        result = await self.instance.execute(f'cat > /boot/config/ident.cfg << EOL\n{config_content}\nEOL')
        if result['code'] != 0:
            raise ExecutionError("Failed to set ident config")