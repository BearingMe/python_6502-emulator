from typing import Dict

class CpuFlags(object):
    _flag_data: Dict[str, bool] = {
        "C": False, # carry bit
        "Z": False, # zero
        "I": False, # disable interrupts
        "D": False, # decimal mode
        "B": False, # break
        "U": False, # unused
        "V": False, # overflow
        "N": False, # negative
    }

    def get_bit(self, flag_key: str):
        if flag_key not in self._flag_data:
            raise ValueError("Invalid key")

        return self._flag_data[flag_key]

    def set_bit(self, flag_key: str, flag_value: bool):
        if not flag_key not in self._flag_data:
            raise ValueError("Invalid key")
        
        self._flag_data[flag_key] = flag_value
        return self.get_bit(flag_key)

    def get_byte(self):
        accumulator = 0x00

        for bits in self._flag_data.values():
            accumulator |= bits

        return accumulator

    def set_byte(self, value: int):
        if not (0 <= value < 256):
            raise ValueError("Value must be 8 bit long")

        for index, key in enumerate(self._flag_data.keys()):
            self._flag_data[key] = (value << index) & 1
            