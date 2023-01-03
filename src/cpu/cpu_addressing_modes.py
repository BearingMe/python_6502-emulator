from .interfaces.abstract_cpu_addressing_modes import AbstractCpuAddressingModes
from .interfaces.abstract_cpu import AbstractCpu

class CpuAddressingModes(AbstractCpuAddressingModes):
    def __init__(self, cpu):
        self.cpu: AbstractCpu = cpu

    def _read_byte(self, address: int, increment: bool = True) -> int:
        """
        Reads a single byte value from the address pointed to by program counter
        Increments program counter by 1
        """
        operand = self.cpu.bus.read(address)
        self.cpu.state.register_PC += (1 if increment else 0)

        return operand

    def _read_word(self, address: int, increment: bool = True) -> tuple:
        """
        Reads a word value from the address pointed to by program counter
        Increments program counter by 2
        """
        low_byte = self._read_byte(address, increment)
        high_byte = self._read_byte(address + 1, increment)

        return low_byte, high_byte

    def _check_page_boundary(self, address: int, high_byte: int) -> bool:
        """
        Checks if the high byte of the address is in the same page as a given address
        """
        return (address >> 8) != (high_byte)

    def ABS(self) -> int:
        """
        Absolute addressing mode
        Used to access memory at a specific given address from the program counter
        """
        low_byte, high_byte = self._read_word(self.cpu.state.register_PC)
        self.cpu.state.helper_addr_abs = (high_byte << 8) | low_byte

        return 0

    def ABX(self) -> int:
        """
        Absolute addressing mode with X offset
        Access memory at a specific address read + X register offset
        """
        low_byte, high_byte = self._read_word(self.cpu.state.register_PC)
        self.cpu.state.helper_addr_abs = (high_byte << 8) | low_byte

        self.cpu.state.helper_addr_abs += self.cpu.state.register_X

        has_crossed_boundary = self._check_page_boundary(self.cpu.state.helper_addr_abs, high_byte)

        if has_crossed_boundary:
            return 1

        return 0

    def ABY(self) -> int:
        """
        Absolute addressing mode with Y offset
        Access memory at a specific address read + Y register offset
        """
        low_byte, high_byte = self._read_word(self.cpu.state.register_PC)
        self.cpu.state.helper_addr_abs = (high_byte << 8) | low_byte

        self.cpu.state.helper_addr_abs += self.cpu.state.register_Y

        has_crossed_boundary = self._check_page_boundary(self.cpu.state.helper_addr_abs, high_byte)

        if has_crossed_boundary:
            return 1

        return 0

    def IMM(self) -> int:
        """
        Immediate addressing mode
        Specifies a value to be used in an operation
        """
        self.cpu.state.helper_addr_abs = self.cpu.state.register_PC
        self.cpu.state.register_PC += 1

        return 0

    def IMP(self) -> int:
        """
        Implied addressing mode
        No operand is needed
        """
        self.cpu.state.helper_fetched = self.cpu.state.register_A

        return 0

    def IND(self) -> int:
        """
        Indirect addressing mode
        Used to access memory at a specific address
        """
        pointer_low_byte, pointer_high_byte = self._read_word(self.cpu.state.register_PC)

        # Simulate page boundary bug
        if pointer_low_byte == 0xFF:
            pointer_low_byte = 0x00
            pointer_high_byte += 1

        pointer = (pointer_high_byte << 8) | pointer_low_byte

        low_byte, high_byte = self._read_word(pointer, increment=False)

        self.cpu.state.helper_addr_abs = (high_byte << 8) | low_byte

        return 0

    def IZX(self) -> int:
        """
        Indirect addressing mode with X offset
        Access memory using a pointer + X register offset
        """
        pointer = self._read_byte(self.cpu.state.register_PC)
        pointer += self.cpu.state.register_X
        pointer &= 0x00FF

        low_byte, high_byte = self._read_word(pointer, increment=False)

        self.cpu.state.helper_addr_abs = (high_byte << 8) | low_byte

        return 0

    def IZY(self) -> int:
        """
        Indirect addressing mode with Y offset
        Access memory using a pointer + Y register offset
        """
        pointer = self._read_byte(self.cpu.state.register_PC)
        pointer &= 0x00FF

        low_byte, high_byte = self._read_word(pointer, increment=False)

        self.cpu.state.helper_addr_abs = (high_byte << 8) | low_byte
        self.cpu.state.helper_addr_abs += self.cpu.state.register_Y
        self.cpu.state.helper_addr_abs &= 0xFFFF

        has_crossed_boundary = self._check_page_boundary(self.cpu.state.helper_addr_abs, high_byte)

        if has_crossed_boundary:
            return 1

        return 0


    def REL(self) -> int:
        """
        Relative addressing mode
        Used to specify a branch offset
        """
        self.cpu.state.helper_addr_rel = self._read_byte(self.cpu.state.register_PC)

        if self.cpu.state.helper_addr_rel & 0x80:
            self.cpu.state.helper_addr_rel |= 0xFF00

        return 0

    def ZP0(self) -> int:
        """
        Zero page addressing mode
        Used to access memory at a specific address
        """
        self.cpu.state.helper_addr_abs = self._read_byte(self.cpu.state.register_PC)

        self.cpu.state.helper_addr_abs &= 0x00FF

        return 0


    def ZPX(self) -> int:
        """
        Zero page addressing mode with X offset
        Access memory at a specific address + X register offset
        """
        self.cpu.state.helper_addr_abs = self._read_byte(self.cpu.state.register_PC)
        self.cpu.state.helper_addr_abs += self.cpu.state.register_X

        self.cpu.state.helper_addr_abs &= 0x00FF

        return 0


    def ZPY(self) -> int:
        """
        Zero page addressing mode with Y offset
        Access memory at a specific address + Y register offset
        """
        self.cpu.state.helper_addr_abs = self._read_byte(self.cpu.state.register_PC)
        self.cpu.state.helper_addr_abs += self.cpu.state.register_Y

        self.cpu.state.helper_addr_abs &= 0x00FF

        return 0
    