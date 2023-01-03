from abc import ABC, abstractmethod
from .abstract_cpu import AbstractCpu

class AbstractCpuBus(ABC):
    def __init__(self, cpu: AbstractCpu):
        self.cpu: AbstractCpu = cpu

    @abstractmethod
    def read(self, address: int) -> int:
        pass

    @abstractmethod
    def write(self, address: int, value: int) -> None:
        pass

    @abstractmethod
    def load(self, program: bytearray) -> None:
        pass