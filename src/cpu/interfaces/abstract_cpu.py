from abc import ABC, abstractmethod

from .abstract_cpu_addressing_modes import AbstractCpuAddressingModes
from .abstract_cpu_bus import AbstractCpuBus
from .abstract_cpu_instructions import AbstractCpuInstructions
from .abstract_cpu_state_handler import AbstractCpuStateHandler

class AbstractCpu(ABC):
    def __init__(self):
        self.addr_modes: AbstractCpuAddressingModes
        self.bus: AbstractCpuBus
        self.instructions: AbstractCpuInstructions
        self.state: AbstractCpuStateHandler

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def fetch(self) -> int:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass