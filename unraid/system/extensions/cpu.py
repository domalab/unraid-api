import re
from typing import List, Dict
from ...unraid import Unraid
from ...exceptions import ExecutionError, ParseError

class CoreUsage(Dict):
    usr: float
    nice: float
    sys: float
    io_wait: float
    idle: float
    hardware_interrupts: float
    software_interrupts: float
    steal: float

class CPUUsage(Dict):
    core_count: int
    all: CoreUsage
    cores: List[CoreUsage]
    raw: List[str]

class CpuExtension:
    def __init__(self, instance: Unraid):
        self.instance = instance

    async def usage(self) -> CPUUsage:
        result = await self.instance.execute(
            "COLUMNS=200 TERM=dumb top -1 -n 1 -b | grep '^%Cpu[[:digit:]+]' | tr '\n' '|'"
        )
        if result['code'] != 0:
            raise ExecutionError("Failed to get CPU usage")
        return self._parse_cpu_usage_output(result['stdout'])

    def _parse_cpu_usage_output(self, input_lines: List[str]) -> CPUUsage:
        cpu_regex = re.compile(
            r'%Cpu(\d+)\s*:\s*(\d+\.\d+)\s*us,\s*(\d+\.\d+)\s*sy,\s*(\d+\.\d+)\s*ni,\s*'
            r'(\d+\.\d+)\s*id,\s*(\d+\.\d+)\s*wa,\s*(\d+\.\d+)\s*hi,\s*(\d+\.\d+)\s*si,\s*(\d+\.\d+)\s*st'
        )
        
        cores = []
        all_usage = CoreUsage(usr=0, nice=0, sys=0, io_wait=0, idle=0,
                              hardware_interrupts=0, software_interrupts=0, steal=0)

        for line in input_lines:
            for cpu_match in cpu_regex.finditer(line):
                core_num, usr, sys, nice, idle, io_wait, hi, si, st = map(float, cpu_match.groups())
                core_usage = CoreUsage(
                    usr=usr, nice=nice, sys=sys, io_wait=io_wait, idle=idle,
                    hardware_interrupts=hi, software_interrupts=si, steal=st
                )
                cores.append(core_usage)
                
                for key in all_usage.keys():
                    all_usage[key] += core_usage[key]

        if not cores:
            raise ParseError("Failed to parse CPU usage output")

        core_count = len(cores)
        for key in all_usage.keys():
            all_usage[key] /= core_count

        return CPUUsage(core_count=core_count, all=all_usage, cores=cores, raw=input_lines)

    async def on_cpu_usage(self, listener, options=None):
        refresh = options.get('refresh', 1) if options else 1
        command = f"while true; do {self.usage.__wrapped__.__func__.__code__.co_consts[1]}; sleep {refresh}; done"
        
        event, future = await self.instance.execute_stream(command)
        
        async def reader():
            while True:
                await event.wait()
                usage = self._parse_cpu_usage_output(await self.instance.read_stream_output())
                await listener(usage)
                event.clear()

        return future