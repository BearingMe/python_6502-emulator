from abc import ABC, abstractmethod
from typing import Dict

class AbstractCpuStateHandler(ABC):
    def __init__(self):
        self._flags: Dict[str, int]
        self._helpers: Dict[str, int]
        self._registers: Dict[str, int]

    # Flags
    @property
    @abstractmethod
    def flag_C(self) -> int:
        pass

    @property
    @abstractmethod
    def flag_Z(self) -> int:
        pass

    @property
    @abstractmethod
    def flag_I(self) -> int:
        pass

    @property
    @abstractmethod
    def flag_D(self) -> int:
        pass

    @property
    @abstractmethod
    def flag_B(self) -> int:
        pass

    @property
    @abstractmethod
    def flag_U(self) -> int:
        pass

    @property
    @abstractmethod
    def flag_V(self) -> int:
        pass

    @property
    @abstractmethod
    def flag_N(self) -> int:
        pass

    @flag_C.setter
    @abstractmethod
    def flag_C(self, value: int) -> None:
        pass

    @flag_Z.setter
    @abstractmethod
    def flag_Z(self, value: int) -> None:
        pass

    @flag_I.setter
    @abstractmethod
    def flag_I(self, value: int) -> None:
        pass

    @flag_D.setter
    @abstractmethod
    def flag_D(self, value: int) -> None:
        pass

    @flag_B.setter
    @abstractmethod
    def flag_B(self, value: int) -> None:
        pass

    @flag_U.setter
    @abstractmethod
    def flag_U(self, value: int) -> None:
        pass

    @flag_V.setter
    @abstractmethod
    def flag_V(self, value: int) -> None:
        pass

    @flag_N.setter
    @abstractmethod
    def flag_N(self, value: int) -> None:
        pass

    # Helpers
    @property
    @abstractmethod
    def helper_addr_abs(self) -> int:
        pass

    @property
    @abstractmethod
    def helper_addr_rel(self) -> int:
        pass

    @property
    @abstractmethod
    def helper_fetched(self) -> int:
        pass

    @property
    @abstractmethod
    def helper_cycles(self) -> int:
        pass

    @property
    @abstractmethod
    def helper_opcode(self) -> int:
        pass
    
    @helper_addr_abs.setter
    @abstractmethod
    def helper_addr_abs(self, value: int) -> None:
        pass

    @helper_addr_rel.setter
    @abstractmethod
    def helper_addr_rel(self, value: int) -> None:
        pass

    @helper_fetched.setter
    @abstractmethod
    def helper_fetched(self, value: int) -> None:
        pass

    @helper_cycles.setter
    @abstractmethod
    def helper_cycles(self, value: int) -> None:
        pass

    @helper_opcode.setter
    @abstractmethod
    def helper_opcode(self, value: int) -> None:
        pass

    # Registers
    @property
    @abstractmethod
    def register_A(self) -> int:
        pass

    @property
    @abstractmethod
    def register_X(self) -> int:
        pass

    @property
    @abstractmethod
    def register_Y(self) -> int:
        pass

    @property
    @abstractmethod
    def register_PC(self) -> int:
        pass

    @property
    @abstractmethod
    def register_SP(self) -> int:
        pass

    @property
    @abstractmethod
    def register_SR(self) -> int:
        pass

    @register_A.setter
    @abstractmethod
    def register_A(self, value: int) -> None:
        pass

    @register_X.setter
    @abstractmethod
    def register_X(self, value: int) -> None:
        pass

    @register_Y.setter
    @abstractmethod
    def register_Y(self, value: int) -> None:
        pass

    @register_PC.setter
    @abstractmethod
    def register_PC(self, value: int) -> None:
        pass

    @register_SP.setter
    @abstractmethod
    def register_SP(self, value: int) -> None:
        pass

    @register_SR.setter
    @abstractmethod
    def register_SR(self, value: int) -> None:
        pass
