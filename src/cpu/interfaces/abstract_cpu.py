from abc import ABC, abstractmethod

from .abstract_addressing_modes import AbstractAddressingModes
from .abstract_bus import AbstractBus
from .abstract_instructions import AbstractInstructions
from .abstract_state_handler import AbstractStateHandler

class AbstractCpu(ABC):
    def __init__(self):
        self.addr_modes: AbstractAddressingModes
        self.bus: AbstractBus
        self.instructions: AbstractInstructions
        self.state: AbstractStateHandler

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def fetch(self) -> int:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass
