from abc import ABC, abstractmethod

class AbstractCpuBus(ABC):
    @abstractmethod
    def read(self, address: int) -> int:
        pass

    @abstractmethod
    def write(self, address: int, value: int) -> None:
        pass

    @abstractmethod
    def load(self, program: bytearray) -> None:
        pass