from typing import Dict

class CpuFlags:
    # Dictionary that stores the values of the flags
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

    def get_bit(self, flag_key: str) -> bool:
        """
        Returns the value of the flag with the specified key.
        """
        if flag_key not in self._flag_data:
            raise ValueError("Invalid key")

        return self._flag_data[flag_key]

    def set_bit(self, flag_key: str, flag_value: bool) -> bool:
        """
        Sets the value of the flag with the specified key.
        Returns the new value of the flag.
        """
        if flag_key not in self._flag_data:
            raise ValueError("Invalid key")
        
        self._flag_data[flag_key] = flag_value
        return self.get_bit(flag_key)

    def get_byte(self) -> int:
        """
        Returns the 8-bit integer representation of the flags.
        """
        accumulator = 0x00

        for index, value in enumerate(self._flag_data.values()):
            accumulator |= (value << index)

        return accumulator

    def set_byte(self, value: int) -> int:
        """
        Sets the flags to the values specified by the given 8-bit integer.
        Returns the new 8-bit integer representation of the flags.
        """
        if not (0 <= value < 256):
            raise ValueError("Value must be 8 bit long")

        for index, key in enumerate(self._flag_data.keys()):
            self._flag_data[key] = bool(value >> index & 1)

        return self.get_byte()

    def reset_flags(self) -> int:
        """
        Resets all flags to False.
        Returns the new 8-bit integer representation of the flags.
        """
        for key in self._flag_data.keys():
            self._flag_data[key] = False

        return self.get_byte()
