from abc import ABC, abstractmethod

from .abstract_cpu_state_handler import AbstractStateHandler
from .abstract_cpu_addressing_modes import AbstractCpuAddressingModes
from .abstract_cpu_instructions import AbstractCpuInstructions

class AbstractCpu(ABC):
    def __init__(self):
        self.state_handler: AbstractStateHandler
        self.instructions: AbstractCpuInstructions
        self.addressing_modes: AbstractCpuAddressingModes

    @abstractmethod
    def run(self) -> None:
        pass
