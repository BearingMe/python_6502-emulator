from typing import Dict

class CpuState:
    _registers: Dict[str, int] = {
        "A": 0x00, # 8-bit accumulator
        "X": 0x00, # 8-bit x register
        "Y": 0x00, # 8-bit y register
        "SP": 0x00, # 8-bit stack pointer
        "Status": 0x00, # 8-bit processor status
        "PC": 0x0000 # 16-bit processor counter
    }

    cycles = 0
    fetched = 0x00
    addr_abs = 0x0000
    addr_rel = 0x0000
    opcode = 0x00

    def _check_value_size(self, value, bits):
        if value >= 2**bits or value < 0:
            raise ValueError(f"{value} is not a {bits}-bit value")

    def _set_register_value(self, register, value, bits):
        self._registers[register] = value & 2**bits - 1

    @property
    def a(self):
        return self._registers.get("A") 

    @property
    def x(self):
        return self._registers.get("X")
    
    @property
    def y(self):
        return self._registers.get("Y")

    @property
    def sp(self):
        return self._registers.get("SP")

    @property
    def status(self):
        return self._registers.get("Status")

    @property
    def pc(self):
        return self._registers.get("PC")

    @a.setter
    def a(self, value):
        self._check_value_size(value, bits=8)
        self._set_register_value("A", value, bits=8)

        return self._registers["A"]

    @x.setter
    def x(self, value):
        self._check_value_size(value, bits=8)
        self._set_register_value("X", value, bits=8)

        return self._registers["X"]

    @y.setter
    def y(self, value):
        self._check_value_size(value, bits=8)
        self._set_register_value("Y", value, bits=8)

        return self._registers["Y"]

    @sp.setter
    def sp(self, value):
        self._check_value_size(value, bits=8)
        self._set_register_value("SP", value, bits=8)

        return self._registers["SP"]

    @status.setter
    def status(self, value):
        self._check_value_size(value, bits=8)
        self._set_register_value("Status", value, bits=8)

        return self._registers["Status"]
      
    @pc.setter
    def pc(self, value):
        self._check_value_size(value, bits=16)
        self._set_register_value("PC", value, bits=16)

        return self._registers["PC"]
