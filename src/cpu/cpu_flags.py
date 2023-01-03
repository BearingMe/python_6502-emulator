from typing import Dict

class CpuFlags:
    def __init__(self):      
        self._flags: Dict[str, bool] = {
            "C": 0, # carry bit
            "Z": 0, # zero
            "I": 0, # disable interrupts
            "D": 0, # decimal mode
            "B": 0, # break
            "U": 0, # unused
            "V": 0, # overflow
            "N": 0, # negative
        }

    def __repr__(self) -> str:
        return f"N:{self.N}, " +\
               f"V:{self.V}, " +\
               f"D:{self.D}, " +\
               f"I:{self.I}, " +\
               f"Z:{self.Z}, " +\
               f"C:{self.C}"

    @property
    def C(self) -> int:
        return int(self._flags.get("C"))

    @property
    def Z(self) -> int:
        return int(self._flags.get("Z"))
    
    @property
    def I(self) -> int:
        return int(self._flags.get("I"))

    @property
    def D(self) -> int:
        return int(self._flags.get("D"))

    @property
    def B(self) -> int:
        return int(self._flags.get("B"))

    @property
    def U(self) -> int:
        return int(self._flags.get("U"))

    @property
    def V(self) -> int:
        return int(self._flags.get("V"))

    @property
    def N(self) -> int:
        return int(self._flags.get("N"))

    @property
    def byte(self) -> int:
        accumulator = 0x00

        for index, value in enumerate(self._flags.values()):
            accumulator |= (value << index)

        return accumulator

    @C.setter
    def C(self, value: int) -> int:
        self._set_flag_value("C", value)

        return self.C

    @Z.setter
    def Z(self, value: int) -> int:
        self._set_flag_value("Z", value)

        return self.Z

    @I.setter
    def I(self, value: int) -> int:
        self._set_flag_value("I", value)

        return self.I
    
    @D.setter
    def D(self, value: int) -> int:
        self._set_flag_value("D", value)

        return self.D

    @B.setter
    def B(self, value: int) -> int:
        self._set_flag_value("B", value)

        return self.B

    @U.setter
    def U(self, value: int) -> int:
        self._set_flag_value("U", value)

        return self.U

    @V.setter
    def V(self, value: int) -> int: 
        self._set_flag_value("V", value)

        return self.V

    @N.setter
    def N(self, value: int) -> int:
        self._set_flag_value("N", value)

        return self.N

    @byte.setter
    def byte(self, value: int) -> int:
        self._check_value_size(value, bits=8)

        for index, key in enumerate(self._flags.keys()):
            self._flags[key] = bool(value >> index & 1)

        return self.byte

    def _check_value_size(self, value, bits=1):
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")

        if not (0 <= value < 2**bits):
            raise ValueError(f"{value} is not a {bits}-bit value")

    def _set_flag_value(self, flag, value): 
        self._flags[flag] = bool(value)