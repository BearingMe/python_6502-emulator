from abc import ABC, abstractmethod

class AbstractCpuDebugger(ABC):
    @abstractmethod
    def log(self) -> None:
        pass
