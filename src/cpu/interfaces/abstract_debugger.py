from abc import ABC, abstractmethod

class AbstractDebugger(ABC):
    @abstractmethod
    def log(self) -> None:
        pass
