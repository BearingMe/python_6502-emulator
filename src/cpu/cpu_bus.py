from .interfaces import AbstractCpu
from .interfaces import AbstractCpuBus

class CpuBus(AbstractCpuBus):
    def __init__(self, cpu: AbstractCpu):
        self.cpu = cpu
        self.ram = [0] * 64 * 1024
        self.read_only = False

    def _check_address_range(self, address: int) -> None:
        """
        Check if address is in range
        """
        if address > len(self.ram) - 1:
            raise IndexError(f'Address out of range: {address} > {len(self.ram) - 1}')

    def _check_read_only(self) -> None:
        """
        Check if memory is read only
        """
        if self.read_only:
            raise ValueError('Cannot write to read only memory')

    def read(self, address: int, read_only: bool = False) -> int:
        """
        Read a byte from ram memory
        """
        self.read_only = read_only
        self._check_address_range(address)

        return self.ram[address]

    def write(self, address: int, data: int) -> None:
        """
        Write a byte to ram memory
        """
        self._check_address_range(address)
        self._check_read_only()

        self.ram[address] = data

    def load(self, program: bytearray, initial_position: int = 0x0000) -> None:
        """
        Load a program into ram memory
        """
        self._check_address_range(initial_position + len(program) - 1)
        
        for i, byte in enumerate(program):
            self.write(i + initial_position, byte)
