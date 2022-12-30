class AddressingModes:
    def _fetch_argument(self):
        operand = self.read(self.pc)
        self.pc += 1

        return operand

    def _fetch_instruction(self):
        lo = self._fetch_argument()
        hi = self._fetch_argument()

        return hi, lo

    def _check_page_boundary_cross(self, address: int, hi: int) -> int:
        if (address & 0xFF00) != (hi << 8):
            return 1
        
        return 0

    def _join_high_low_bytes(self, high_byte, low_byte):
        return ((high_byte << 8) | low_byte)

    def ABS(self) -> int:
        hi, lo = self._fetch_instruction()

        self.addr_abs = self._join_high_low_bytes(hi, lo)

        return 0

    def ABX(self) -> int:
        hi, lo = self._fetch_instruction()

        self.addr_abs = self._join_high_low_bytes(hi, lo) + self.x

        return self._check_page_boundary_cross(self.addr_abs, hi)

    def ABY(self) -> int:
        hi, lo = self._fetch_instruction()

        self.addr_abs = self._join_high_low_bytes(hi, lo) + self.y

        return self._check_page_boundary_cross(self.addr_abs, hi)

    def IMM(self) -> int:
        self.addr_abs = self.pc
        self.pc += 1

        return 0

    def IMP(self) -> int:
        self.fetched = self.a

        return 0

    def IND(self) -> int:
        hi, lo = self._fetch_instruction()

        ptr = self._join_high_low_bytes(hi, lo)

        self.addr_abs = self._join_high_low_bytes(self.read(ptr + 1), self.read(ptr))
        
        if lo == 0x00FF:
            self.addr_abs = self._join_high_low_bytes(self.read(ptr), self.read(ptr))
        
        return 0

    def IZX(self) -> int:
        t = self._fetch_argument()

        hi = self.read((t + self.x + 1) & 0x00FF)
        lo = self.read((t + self.x) & 0x00FF)

        self.addr_abs = self._join_high_low_bytes(hi, lo)

        return 0

    def IZY(self) -> int:
        t = self._fetch_argument()

        hi = self.read((t + 1) & 0x00FF)
        lo = self.read(t & 0x00FF)

        self.addr_abs = self._join_high_low_bytes(hi, lo) + self.y

        return self._check_page_boundary_cross(self.addr_abs, hi)

    def REL(self) -> int:
        self.addr_rel = self.read(self.pc)
        self.pc += 1

        if (self.addr_rel & 0x80):
            self.addr_rel |= 0xFF00

        return 0

    def ZP0(self) -> int:
        self.addr_abs = self._fetch_argument()
        self.addr_abs &= 0x00FF

        return 0

    def ZPX(self) -> int:
        self.addr_abs = self._fetch_argument() + self.x
        self.addr_abs &= 0x00FF

        return 0

    def ZPY(self) -> int:
        self.addr_abs = self._fetch_argument() + self.y
        self.addr_abs &= 0x00FF

        return 0
