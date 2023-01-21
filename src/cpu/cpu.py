import json
from time import sleep

from .cpu_bus import Bus
from .cpu_addressing_modes import AddressingModes
from .cpu_instructions import Instructions
from .cpu_state_handler import StateHandler
from .cpu_debugger import Debugger

from .interfaces import AbstractCpu

class Cpu(AbstractCpu):
    def __init__(self):
        self.state = StateHandler()
        self.bus = Bus(self)
        self.addr_modes = AddressingModes(self)
        self.instructions = Instructions(self)
        self.debugger = Debugger(self)

    def _wait_cycles(self, clock_speed_mhz: float = 1) -> None:
        """
        Wait for a given amount of cycles
        """
        for _ in range(self.state.cycles):
            sleep(1 / (clock_speed_mhz * 10**6))

        self.state.cycles = 0

    def _load_lookup_table(self) -> None:
        """
        Load the instruction lookup table containing all the information
        about the instructions and their addressing modes
        """
        with open("./data/instruction_set.json", "r") as f:
            self.lookup = json.load(f)

    def fetch(self) -> int:
        """
        Fetches the next byte from the bus
        """
        if self.state.addr_abs != "IMP":
            self.state.fetched = self.bus.read(self.state.addr_abs)

        return self.state.fetched
        
    def reset(self) -> None:
        """
        Force the CPU into a known state
        """
        # set program counter to the reset vector
        self.state.register_PC = self.bus.read(0xFFFC) | (self.bus.read(0xFFFD) << 8)

        # reset registers
        self.state.register_A = 0
        self.state.register_X = 0
        self.state.register_Y = 0
        self.state.register_SP = 0xFD
        self.state.register_SR = 0x00

        # set unused flag as 1
        self.state.flag_U = bool(1)

        # clear helper variables
        self.state.addr_rel = 0x0000
        self.state.addr_abs = 0x0000
        self.state.fetched = 0x00

        self.state.cycles = 8
        

    def run(self, binary, cycle_accurate=False) -> None:
        """
        Read the rom and execute the instructions
        """
        self.bus.load(binary)
        self.reset()

        self._load_lookup_table()

        # test binary only
        self.state.register_PC = 0x0400

        while True:
            self.debugger.log()
            
            # fetch opcode
            self.state.opcode = self.bus.read(self.state.register_PC)
            self.state.register_PC += 1
        
            # read data from lookup table
            self.state.cycles = self.lookup[self.state.opcode]["cycles"]
            self.state.current_addressing_mode = self.lookup[self.state.opcode]["addressing_mode"]
            self.state.current_instruction = self.lookup[self.state.opcode]["operation"]
            
            # load function pointers
            address_mode = getattr(self.addr_modes, self.state.current_addressing_mode)
            instruction = getattr(self.instructions, self.state.current_instruction)
            
            # fetch data, perform operation and increment cycle counter
            self.state.cycles += address_mode()
            self.state.cycles += instruction()

            if cycle_accurate:
                self._wait_cycles(1000)

            if self.state.current_instruction == "BRK":
                break

        self.debugger.log()
        