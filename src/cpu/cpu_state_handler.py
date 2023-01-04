from .interfaces.abstract_cpu_state_handler import AbstractCpuStateHandler

class CpuStateHandler(AbstractCpuStateHandler):
    def __init__(self):
        self._flags = {
            "C": (0 << 0), # Carry
            "Z": (0 << 1), # Zero
            "I": (0 << 2), # Interrupt
            "D": (0 << 3), # Decimal
            "B": (0 << 4), # Break
            "U": (0 << 5), # Unused
            "V": (0 << 6), # Overflow
            "N": (0 << 7),  # Negative
        }

        self._helpers = {
            "addr_abs": 0x0000, # Absolute address
            "addr_rel": 0x0000, # Relative address
            "cycles": 0,        # Cycles
            "fetched": 0x0000,  # Fetched data
            "opcode": 0x00,      # Opcode

        }
        self._registers = {
            "A": 0x00,    # 8-bit Accumulator
            "X": 0x00,    # 8-bit X register
            "Y": 0x00,    # 8-bit Y register
            "SP": 0x00,   # 8-bit Stack pointer
            "SR": 0x00,   # 8-bit Status register
            "PC": 0x0000, # 16-bit Program counter
        }

    # Flags Getters and Setters
    @property
    def flag_C(self) -> int:
        return self._flags.get("C")

    @property
    def flag_Z(self) -> int:
        return self._flags.get("Z")

    @property
    def flag_I(self) -> int:
        return self._flags.get("I")

    @property
    def flag_D(self) -> int:
        return self._flags.get("D")

    @property
    def flag_B(self) -> int:
        return self._flags.get("B")

    @property
    def flag_U(self) -> int:
        return self._flags.get("U")

    @property
    def flag_V(self) -> int:
        return self._flags.get("V")

    @property
    def flag_N(self) -> int:
        return self._flags.get("N")

    @flag_C.setter
    def flag_C(self, value: int):
        self._check_value_size(value)
        self._ensure_nth_bit(value, bit=0)

        self._flags["C"] = value

    @flag_Z.setter
    def flag_Z(self, value: int):
        self._check_value_size(value)
        self._ensure_nth_bit(value, bit=1)

        self._flags["Z"] = value

    @flag_I.setter
    def flag_I(self, value: int):
        self._check_value_size(value)
        self._ensure_nth_bit(value, bit=2)

        self._flags["I"] = value

    @flag_D.setter
    def flag_D(self, value: int):
        self._check_value_size(value)
        self._ensure_nth_bit(value, bit=3)

        self._flags["D"] = value

    @flag_B.setter
    def flag_B(self, value: int):
        self._check_value_size(value)
        self._ensure_nth_bit(value, bit=4)

        self._flags["B"] = value

    @flag_U.setter
    def flag_U(self, value: int):
        self._check_value_size(value)
        self._ensure_nth_bit(value, bit=5)

        self._flags["U"] = value

    @flag_V.setter
    def flag_V(self, value: int):
        self._check_value_size(value)   
        self._ensure_nth_bit(value, bit=6)

        self._flags["V"] = value

    @flag_N.setter
    def flag_N(self, value: int):
        self._check_value_size(value)
        self._ensure_nth_bit(value, bit=7)

        self._flags["N"] = value

    # Helpers Getters and Setters
    @property
    def helper_addr_abs(self) -> int:
        return self._helpers.get("addr_abs")

    @property
    def helper_addr_rel(self) -> int:
        return self._helpers.get("addr_rel")

    @property
    def helper_fetched(self) -> int:
        return self._helpers.get("fetched")

    @property
    def helper_cycles(self) -> int:
        return self._helpers.get("cycles")

    @property
    def helper_opcode(self) -> int:
        return self._helpers.get("opcode")

    @helper_addr_abs.setter
    def helper_addr_abs(self, value: int):
        self._check_value_size(value, 16)
        self._helpers["addr_abs"] = value

    @helper_addr_rel.setter
    def helper_addr_rel(self, value: int):
        self._check_value_size(value, 16)
        self._helpers["addr_rel"] = value

    @helper_fetched.setter
    def helper_fetched(self, value: int):
        self._check_value_size(value, 16)
        self._helpers["fetched"] = value

    @helper_cycles.setter
    def helper_cycles(self, value: int):
        self._check_value_size(value, 64)
        self._helpers["cycles"] = value

    @helper_opcode.setter
    def helper_opcode(self, value: int):
        self._check_value_size(value)
        self._helpers["opcode"] = value

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
        self._check_value_size(value)
        self._registers["SP"] = value

    @register_SR.setter
    def register_SR(self, value: int):
        self._check_value_size(value)
        self._registers["SR"] = value

    # Methods
    def _check_value_size(self, value: int, bits: int = 8):
        if not (0 <= value < 2**bits):
            raise ValueError(f"{value} is not a {bits} bits unsigned integer")

    def _ensure_nth_bit(self, value: int, bit: int):
        sulfix_map = {
            1: "st", 
            2: "nd", 
            3: "rd",
        }
        
        sulfix = sulfix_map.get(bit, "th")

        bit_exists = (value >> bit) & 1
        
        if not (value == 0 or bit_exists):
            raise ValueError(f"{bit}{sulfix} bit not set")
