from .interfaces.abstract_cpu import AbstractCpu
from .interfaces.abstract_cpu_bus import AbstractCpuBus
from .interfaces.abstract_cpu_state_handler import AbstractCpuStateHandler
from .interfaces.abstract_cpu_instructions import AbstractCpuInstructions
from .interfaces.abstract_cpu_addressing_modes import AbstractCpuAddressingModes

from .cpu_addressing_modes import CpuAddressingModes
from .cpu_instructions import CpuInstructions
from .cpu_state_handler import CpuStateHandler

import json

with open("./data/instruction_set.json", "r") as f:
    lookup = json.load(f)

class CpuBus(AbstractCpuBus):
    def __init__(self, cpu: AbstractCpu):
        self.cpu = cpu
        self.ram = [0] * 64 * 1024

    def read(self, address: int, read_only: bool = False) -> int:
        return self.ram[address]

    def write(self, address: int, data: int) -> None:
        if address > len(self.ram) - 1:
            raise IndexError(f'Address out of range: {address} > {len(self.ram) - 1}')
        
        self.ram[address] = data

    def load(self, program: bytearray) -> None:
        for i, byte in enumerate(program):
            self.write(i, byte)

# TODO: Implement interrupts
class Cpu(AbstractCpu):
    def __init__(self):
        self.state: AbstractCpuStateHandler = CpuStateHandler()
        self.bus: AbstractCpuBus = CpuBus(self)
        self.addr_modes: AbstractCpuAddressingModes = CpuAddressingModes(self)
        self.instructions: AbstractCpuInstructions = CpuInstructions(self)

    # TODO: Organize this better
    # TODO: Implement cycle counter
    def run(self, binary) -> None:
        self.bus.load(binary)

        self.state.register_PC = 0x0400

        self.state.flag_Z = bool(1)
        self.state.flag_I = bool(1)

        print(f"Status: {self.state.register_SR:08b}")

        while True:
            print(f"PC: {self.state.register_PC:04x}")

            self.state.opcode = self.bus.read(self.state.register_PC)
            self.state.register_PC += 1

            print(f"OPCODE: {self.state.opcode:02x}")

            self.state.current_addressing_mode = lookup[self.state.opcode]["addressing_mode"]
            self.state.current_instruction = lookup[self.state.opcode]["operation"]

            print(f"INSTRUCTION: {self.state.current_instruction}")
            print(f"ADDRESSING MODE: {self.state.current_addressing_mode}")

            getattr(self.addr_modes, self.state.current_addressing_mode)()
            getattr(self.instructions, self.state.current_instruction)()

            print(f"A: 0x{self.state.register_A:02x},", end=" ")
            print(f"X: 0x{self.state.register_X:02x},", end=" ")
            print(f"Y: 0x{self.state.register_Y:02x},", end=" ")
            print(f"SP: 0x{self.state.register_SP:02x}")

            print(f"N: {int(self.state.flag_N)},", end=" ")
            print(f"V: {int(self.state.flag_V)},", end=" ")
            print(f"U: {int(self.state.flag_U)},", end=" ")
            print(f"B: {int(self.state.flag_B)},", end=" ")
            print(f"D: {int(self.state.flag_D)},", end=" ")
            print(f"I: {int(self.state.flag_I)},", end=" ")
            print(f"Z: {int(self.state.flag_Z)},", end=" ")
            print(f"C: {int(self.state.flag_C)}")

            print("\n")

            if self.state.register_PC == 0x0435:
                from time import sleep
                sleep(1)

            if self.state.current_instruction == "BRK":
                break

    def fetch(self) -> int:
        if self.state.addr_abs != "IMP":
            self.state.fetched = self.bus.read(self.state.addr_abs)

        return self.state.fetched

    def reset(self) -> None:
        """
        Work in progress
        """
        pass
