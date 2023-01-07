from .interfaces import AbstractCpuStateHandler

from typing import Any

class CpuStateHandler(AbstractCpuStateHandler):
    def __init__(self):
        self._aux_vars = {
            "addr_abs": 0x0000,              # Absolute address
            "addr_rel": 0x0000,              # Relative address
            "cycles": 0,                     # Cycles
            "fetched": 0x0000,               # Fetched data
            "opcode": 0x00,                  # Opcode
            "current_addressing_mode": None, # Current addressing mode
            "current_instruction": None,     # Current instruction
        }

        self._flags = {
            "C": (1 << 0), # Carry
            "Z": (1 << 1), # Zero
            "I": (1 << 2), # Interrupt
            "D": (1 << 3), # Decimal
            "B": (1 << 4), # Break
            "U": (1 << 5), # Unused
            "V": (1 << 6), # Overflow
            "N": (1 << 7), # Negative
        }

        self._registers = {
            "A": 0x00,    # 8-bit Accumulator
            "X": 0x00,    # 8-bit X register
            "Y": 0x00,    # 8-bit Y register
            "SP": 0x00,   # 8-bit Stack pointer
            "SR": 0x00,   # 8-bit Status register
            "PC": 0x0000, # 16-bit Program counter
        }

    # Methods
    def _check_value_size(self, value: int, bits: int = 8):
        if not (0 <= value < 2**bits):
            raise ValueError(f"{value} is not a {bits} bits unsigned integer")

    def _check_value_type(self, value: Any, expected_type: str):
        if not isinstance(value, expected_type):
            raise TypeError(f"{value} is not a {expected_type}")

    def _set_flag(self, flag: str, value: int):
        if (value):
            self.register_SR |= self._flags[flag]
        else:
            self.register_SR &= ~self._flags[flag]

    def _get_flag(self, flag: str) -> int:
        flag_value = self.register_SR & self._flags[flag]

        return bool(flag_value)


    @property
    def addr_abs(self) -> int:
        return self._aux_vars.get("addr_abs")

    @property
    def addr_rel(self) -> int:
        return self._aux_vars.get("addr_rel")

    @property
    def fetched(self) -> int:
        return self._aux_vars.get("fetched")

    @property
    def cycles(self) -> int:
        return self._aux_vars.get("cycles")

    @property
    def opcode(self) -> int:
        return self._aux_vars.get("opcode")

    @property
    def current_addressing_mode(self) -> str:
        return self._aux_vars.get("current_addressing_mode")

    @property
    def current_instruction(self) -> str:
        return self._aux_vars.get("current_instruction")

    @addr_abs.setter
    def addr_abs(self, value: int):
        self._check_value_size(value, 16)
        self._aux_vars["addr_abs"] = value

    @addr_rel.setter
    def addr_rel(self, value: int):
        self._check_value_size(value, 16)
        self._aux_vars["addr_rel"] = value

    @fetched.setter
    def fetched(self, value: int):
        self._check_value_size(value, 16)
        self._aux_vars["fetched"] = value

    @cycles.setter
    def cycles(self, value: int):
        self._check_value_size(value, 64)
        self._aux_vars["cycles"] = value

    @opcode.setter
    def opcode(self, value: int):
        self._check_value_size(value)
        self._aux_vars["opcode"] = value

    # TODO: add enum, tests and typechecking
    @current_addressing_mode.setter
    def current_addressing_mode(self, value):
        self._check_value_type(value, str)
        self._aux_vars["current_addressing_mode"] = value
    
    @current_instruction.setter
    def current_instruction(self, value):
        self._check_value_type(value, str)
        self._aux_vars["current_instruction"] = value

    @property
    def flag_C(self) -> int:
        return self._get_flag("C")

    @property
    def flag_Z(self) -> int:
        return self._get_flag("Z")

    @property
    def flag_I(self) -> int:
        return self._get_flag("I")

    @property
    def flag_D(self) -> int:
        return self._get_flag("D")

    @property
    def flag_B(self) -> int:
        return self._get_flag("B")

    @property
    def flag_U(self) -> int:
        return self._get_flag("U")

    @property
    def flag_V(self) -> int:
        return self._get_flag("V")

    @property
    def flag_N(self) -> int:
        return self._get_flag("N")

    # TODO: add tests
    @flag_C.setter
    def flag_C(self, value: int):
        self._check_value_size(value)
        self._check_value_type(value, bool)

        self._set_flag("C", value)

    @flag_Z.setter
    def flag_Z(self, value: int):
        self._check_value_size(value)
        self._check_value_type(value, bool)

        self._set_flag("Z", value)

    @flag_I.setter
    def flag_I(self, value: int):
        self._check_value_size(value)
        self._check_value_type(value, bool)

        self._set_flag("I", value)

    @flag_D.setter
    def flag_D(self, value: int):
        self._check_value_size(value)
        self._check_value_type(value, bool)

        self._set_flag("D", value)

    @flag_B.setter
    def flag_B(self, value: int):
        self._check_value_size(value)
        self._check_value_type(value, bool)

        self._set_flag("B", value)

    @flag_U.setter
    def flag_U(self, value: int):
        self._check_value_size(value)
        self._check_value_type(value, bool)

        self._set_flag("U", value)

    @flag_V.setter
    def flag_V(self, value: int):
        self._check_value_size(value)   
        self._check_value_type(value, bool)

        self._set_flag("V", value)

    @flag_N.setter
    def flag_N(self, value: int):
        self._check_value_size(value)
        self._check_value_type(value, bool)

        self._set_flag("N", value)

    # Registers Getters and Setters
    @property
    def register_A(self) -> int:
        return self._registers.get("A")

    @property
    def register_X(self) -> int:
        return self._registers.get("X")

    @property
    def register_Y(self) -> int:
        return self._registers.get("Y")

    @property
    def register_PC(self) -> int:
        return self._registers.get("PC")

    @property
    def register_SP(self) -> int:
        return self._registers.get("SP")

    @property
    def register_SR(self) -> int:
        return self._registers.get("SR")

    @register_A.setter
    def register_A(self, value: int):
        self._check_value_size(value)
        self._registers["A"] = value

    @register_X.setter
    def register_X(self, value: int):
        self._check_value_size(value)
        self._registers["X"] = value

    @register_Y.setter
    def register_Y(self, value: int):
        self._check_value_size(value)
        self._registers["Y"] = value

    @register_PC.setter
    def register_PC(self, value: int):
        self._check_value_size(value, 16)
        self._registers["PC"] = value

    @register_SP.setter
    def register_SP(self, value: int):
        # self._check_value_size(value)
        self._registers["SP"] = value

    @register_SR.setter
    def register_SR(self, value: int):
        self._check_value_size(value)
        self._registers["SR"] = value
