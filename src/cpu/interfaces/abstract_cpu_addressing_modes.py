from abc import ABC, abstractmethod
from .abstract_cpu import AbstractCpu

class AbstractCpuAddressingModes(ABC):
    def __init__(self, cpu: AbstractCpu):
        self.cpu: AbstractCpu = cpu

    @abstractmethod
    def ABS(self) -> int:
        pass

    @abstractmethod
    def ABX(self) -> int:
        pass

    @abstractmethod
    def ABY(self) -> int:
        pass

    @abstractmethod
    def IMM(self) -> int:
        pass

    @abstractmethod
    def IMP(self) -> int:
        pass

    @abstractmethod
    def IND(self) -> int:
        pass

    @abstractmethod
    def IZX(self) -> int:
        pass

    @abstractmethod
    def IZY(self) -> int:
        pass

    @abstractmethod
    def REL(self) -> int:
        pass

    @abstractmethod
    def ZP0(self) -> int:
        pass

    @abstractmethod
    def ZPX(self) -> int:
        pass

    @abstractmethod
    def ZPY(self) -> int:
        pass
