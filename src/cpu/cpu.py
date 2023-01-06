from .interfaces import AbstractCpu
from .interfaces import AbstractCpuBus
from .interfaces import AbstractCpuStateHandler
from .interfaces import AbstractCpuInstructions
from .interfaces import AbstractCpuAddressingModes

from .cpu_bus import CpuBus
from .cpu_addressing_modes import CpuAddressingModes
from .cpu_instructions import CpuInstructions
from .cpu_state_handler import CpuStateHandler
from .cpu_debugger import CpuDebugger

import json

with open("./data/instruction_set.json", "r") as f:
    lookup = json.load(f)


# TODO: Implement interrupts
class Cpu(AbstractCpu):
    def __init__(self):
        self.state: AbstractCpuStateHandler = CpuStateHandler()
        self.bus: AbstractCpuBus = CpuBus(self)
        self.addr_modes: AbstractCpuAddressingModes = CpuAddressingModes(self)
        self.instructions: AbstractCpuInstructions = CpuInstructions(self)
        self.debugger = CpuDebugger(self)

    def fetch(self) -> int:
        if self.state.addr_abs != "IMP":
            self.state.fetched = self.bus.read(self.state.addr_abs)

        return self.state.fetched
        
    def reset(self) -> None:
        """
        Work in progress
        """
        pass

    # TODO: Organize this better
    # TODO: Implement cycle counter
    def run(self, binary) -> None:
        self.bus.load(binary)

        self.state.register_PC = 0x0400

        self.state.flag_Z = bool(1)
        self.state.flag_I = bool(1)

        while True:
            self.state.opcode = self.bus.read(self.state.register_PC)
            self.state.register_PC += 1
            
            self.state.current_addressing_mode = lookup[self.state.opcode]["addressing_mode"]
            self.state.current_instruction = lookup[self.state.opcode]["operation"]

            getattr(self.addr_modes, self.state.current_addressing_mode)()
            getattr(self.instructions, self.state.current_instruction)()
            
            self.debugger.log()

            if self.state.current_instruction == "BRK":
                break
