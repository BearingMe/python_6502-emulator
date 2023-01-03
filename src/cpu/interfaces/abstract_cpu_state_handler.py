from abc import ABC, abstractmethod
from typing import Dict
from .abstract_cpu import AbstractCpu

class AbstractStateHandler(ABC):
    def __init__(self, cpu):
        self.cpu: AbstractCpu = cpu

        self._registers: Dict[str, int]
        self._flags: Dict[str, int]
        self._helpers: Dict[str, int]

    @abstractmethod
    def get_helper(self) -> int:
        pass

    @abstractmethod
    def get_register(self) -> int:
        pass
    
    @abstractmethod
    def get_flag(self) -> int:
        pass

    @abstractmethod
    def set_helper(self, value: int) -> None:
        pass

    @abstractmethod
    def set_register(self, value: int) -> None:
        pass

    @abstractmethod
    def set_flag(self, value: int) -> None:
        pass
