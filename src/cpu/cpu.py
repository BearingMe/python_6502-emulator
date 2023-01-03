'''
AVISO:
    Tem várias operações de flag feita sem bitshift, o que significa que tá passando o valor
    inteiro da flag, e não o valor da flag em si. Isso é um problema, mas não é um problema.

    Só faz alguns testes pra ver se funciona direito, e se não funcionar, aí a gente arruma.


    Parece que as flags serem valores unitários é um problema em operações com o status. rever todo o código de flags.
'''

import json

from .cpu_flags import CpuFlags
from .cpu_state import CpuState

with open("./data/instruction_set.json", "r") as f:
    lookup = json.load(f)

class MemoryHandler:
    def __init__(self) -> None:
        self.memory = [0] * 64 * 1024

    def read(self, address: int) -> int:
        return self.memory[address]

    def write(self, address: int, data: int) -> None:
        self.memory[address] = data
        
    def fetch(self) -> int:
        if (lookup[self.cpu_state.opcode]["addressing_mode"] != "IMP"):
            self.cpu_state.fetched = self.read(self.cpu_state.addr_abs)

        return self.cpu_state.fetched


class Cpu(MemoryHandler):
    def __init__(self, cpu_state: CpuState, cpu_flags: CpuFlags):
        super().__init__()

        self.cpu_state = cpu_state
        self.cpu_flags = cpu_flags

    # helper methods
    def _fetch_argument(self) -> int:
        operand = self.read(self.cpu_state.pc) 
        self.cpu_state.pc += 1

        return operand

    def _fetch_instruction(self) -> tuple:
        lo = self._fetch_argument()
        hi = self._fetch_argument()

        return hi, lo

    def _check_page_boundary_cross(self, address: int, hi: int) -> int:        
        return (address >> 8) != hi

    def _join_high_low_bytes(self, high_byte, low_byte) -> int:
        return ((high_byte << 8) | low_byte)

    # execute
    def execute(self, binary) -> None:
        self.reset()

        self.cpu_state.pc = 0x0400

        self.cpu_flags.Z = 1
        self.cpu_flags.I = 1
        self.cpu_flags.B = 1
        self.cpu_flags.U = 1

        self.cpu_state.sp = 0xFF
        self.cpu_state.status = 0x36

        for i in range(len(binary)):
            self.write(i + 0x0000, binary[i])

        while self.cpu_state.pc < 0xFFFF:
            print(f"Program Counter: {hex(self.cpu_state.pc)}") 

            self.cpu_state.opcode = self.read(self.cpu_state.pc)

            opcode = self.cpu_state.opcode
            addressing_mode = lookup[self.cpu_state.opcode]["addressing_mode"]
            operation = lookup[self.cpu_state.opcode]["operation"]

            self.cpu_state.pc += 1

            print(f"Operation: {operation}")
            print(f"Addressing Mode: {addressing_mode}")

            if addressing_mode != None:
                getattr(self, addressing_mode)()

            if operation != None:
                getattr(self, operation)()

            print(f"Opcode: {hex(self.cpu_state.opcode)}")
            print(f"Accumulator: {hex(self.cpu_state.a)}")

            print(f"Absolute Address: {hex(self.cpu_state.addr_abs)}")
            print(f"X Register: {hex(self.cpu_state.x)}")
            print(f"Y Register: {hex(self.cpu_state.y)}")
            print(self.cpu_flags)
            print(f"Stack Pointer: {hex(self.cpu_state.sp)}")

            print("\n")

            if self.cpu_state.pc == 0x674:
                from time import sleep
                sleep(1)
            
            if opcode == 0x00:
                break

        return self.memory

    # reset
    def reset(self) -> None:
        # reset internal registers
        self.cpu_state.a = 0
        self.cpu_state.x = 0
        self.cpu_state.y = 0
        self.cpu_state.sp = 0xFD
        self.cpu_state.status = 0x00 | self.cpu_flags.U

        lo = self.read(self.cpu_state.addr_abs)
        hi = self.read(self.cpu_state.addr_abs + 1)
        self.cpu_state.pc = self._join_high_low_bytes(hi, lo)

        # clear internal helpers
        self.cpu_state.addr_abs = 0x0000
        self.cpu_state.addr_rel = 0x0000
        self.cpu_state.fetched = 0x00

        self.cpu_state.cycles = 8
    
    # interrupt
    def irq(self) -> None:
        if not self.cpu_flags.I:
            self.write(0x0100 + self.cpu_state.sp, (self.cpu_state.pc >> 8) & 0x00FF)
            self.cpu_state.sp -= 1
            self.write(0x0100 + self.cpu_state.sp, self.cpu_state.pc & 0x00FF)
            self.cpu_state.sp -= 1

            self.cpu_flags.B = 0
            self.cpu_flags.U = 1
            self.cpu_flags.I = 1
            self.write(0x0100 + self.cpu_state.sp, self.cpu_state.status)
            self.cpu_state.sp -= 1

            self.cpu_state.addr_abs = 0xFFFE
            lo = self.read(self.cpu_state.addr_abs)
            hi = self.read(self.cpu_state.addr_abs + 1)
            self.cpu_state.pc = self._join_high_low_bytes(hi, lo)

            self.cpu_state.cycles = 7

    # non maskable interrupt
    def nmi(self) -> None:
        self.write(0x0100 + self.cpu_state.sp, (self.cpu_state.pc >> 8) & 0x00FF)
        self.cpu_state.sp -= 1
        self.write(0x0100 + self.cpu_state.sp, self.cpu_state.pc & 0x00FF)
        self.cpu_state.sp -= 1

        self.cpu_flags.B = 0
        self.cpu_flags.U = 1
        self.cpu_flags.I = 1
        self.write(0x0100 + self.cpu_state.sp, self.cpu_state.status)
        self.cpu_state.sp -= 1

        self.cpu_state.addr_abs = 0xFFFA
        lo = self.read(self.cpu_state.addr_abs)
        hi = self.read(self.cpu_state.addr_abs + 1)
        self.cpu_state.pc = self._join_high_low_bytes(hi, lo)

        self.cpu_state.cycles = 7

    # addressing modes
    def ABS(self) -> int:
        hi, lo = self._fetch_instruction()
        self.cpu_state.addr_abs = self._join_high_low_bytes(hi, lo)

        return 0

    def ABX(self) -> int:
        hi, lo = self._fetch_instruction()
        self.cpu_state.addr_abs = self._join_high_low_bytes(hi, lo) + self.cpu_state.x

        return self._check_page_boundary_cross(self.cpu_state.addr_abs, hi)

    def ABY(self) -> int:
        hi, lo = self._fetch_instruction()
        self.cpu_state.addr_abs = self._join_high_low_bytes(hi, lo) + self.cpu_state.y

        return self._check_page_boundary_cross(self.cpu_state.addr_abs, hi)

    def IMM(self) -> int:
        self.cpu_state.addr_abs = self.cpu_state.pc
        self.cpu_state.pc += 1

        return 0

    def IMP(self) -> int:
        self.cpu_state.fetched = self.cpu_state.a

        return 0

    def IND(self) -> int:
        hi, lo = self._fetch_instruction()

        ptr = self._join_high_low_bytes(hi, lo)

        self.cpu_state.addr_abs = self._join_high_low_bytes(self.read(ptr + 1), self.read(ptr))
        
        if lo == 0x00FF:
            self.cpu_state.addr_abs = self._join_high_low_bytes(self.read(ptr), self.read(ptr))
        
        return 0

    def IZX(self) -> int:
        t = self._fetch_argument()

        hi = self.read((t + self.cpu_state.x + 1) & 0x00FF)
        lo = self.read((t + self.cpu_state.x) & 0x00FF)

        self.cpu_state.addr_abs = self._join_high_low_bytes(hi, lo)

        return 0

    def IZY(self) -> int:
        t = self._fetch_argument()

        hi = self.read((t + 1) & 0x00FF)
        lo = self.read(t & 0x00FF)

        self.cpu_state.addr_abs = self._join_high_low_bytes(hi, lo) + self.cpu_state.y

        return self._check_page_boundary_cross(self.cpu_state.addr_abs, hi)

    def REL(self) -> int:
        self.addr_rel = self.read(self.cpu_state.pc)
        self.cpu_state.pc += 1

        if (self.addr_rel & 0x80): self.addr_rel |= 0xFF00

        return 0

    def ZP0(self) -> int:
        self.cpu_state.addr_abs = self._fetch_argument()
        self.cpu_state.addr_abs &= 0x00FF

        return 0

    def ZPX(self) -> int:
        self.cpu_state.addr_abs = self._fetch_argument() + self.cpu_state.x
        self.cpu_state.addr_abs &= 0x00FF

        return 0

    def ZPY(self) -> int:
        self.cpu_state.addr_abs = self._fetch_argument() + self.cpu_state.y
        self.cpu_state.addr_abs &= 0x00FF

        return 0

    # instructions
    def ADC(self) -> int:
        self.fetch()
        temp = self.cpu_state.a + self.cpu_state.fetched + self.cpu_flags.C
        self.cpu_flags.C = (temp > 255)
        self.cpu_flags.Z = ((temp & 0x00FF) == 0)
        self.cpu_flags.N = (temp & 0x80)
        self.cpu_flags.V = ((~(self.cpu_state.a ^ self.cpu_state.fetched) & (self.cpu_state.a ^ temp)) & 0x0080)

        self.cpu_state.a = temp & 0x00FF

        return 1

    def AND(self) -> int:
        self.fetch()
        self.cpu_state.a &= self.cpu_state.fetched
        self.cpu_flags.Z = (self.cpu_state.a == 0x00)
        self.cpu_flags.N = (self.cpu_state.a & 0x80)

        return 1

    def ASL(self) -> int:
        self.fetch()
        temp = self.cpu_state.fetched << 1
        self.cpu_flags.C = (temp & 0xFF00) > 0
        self.cpu_flags.Z = (temp & 0x00FF) == 0
        self.cpu_flags.N = (temp & 0x80)

        if self.cpu_state.lookup[self.cpu_state.opcode]["addressing_mode"] == "IMP":
            self.cpu_state.a = temp & 0x00FF
        else:
            self.write(self.cpu_state.addr_abs, temp & 0x00FF)

        return 0

    def BCC(self) -> int:
        if not self.cpu_flags.C:
            self.cpu_state.cycles += 1
            self.cpu_state.addr_abs = (self.cpu_state.pc + self.addr_rel) & 0xFFFF

            if (self.cpu_state.addr_abs & 0xFF00) != (self.cpu_state.pc & 0xFF00):
                self.cpu_state.cycles += 1

            self.cpu_state.pc = self.cpu_state.addr_abs

        return 0

    def BCS(self) -> int:
        if self.cpu_flags.C:
            self.cpu_state.cycles += 1
            self.cpu_state.addr_abs = (self.cpu_state.pc + self.addr_rel) & 0xFFFF

            if (self.cpu_state.addr_abs & 0xFF00) != (self.cpu_state.pc & 0xFF00):
                self.cpu_state.cycles += 1

            self.cpu_state.pc = self.cpu_state.addr_abs

        return 0

    def BEQ(self) -> int:
        if self.cpu_flags.Z:
            self.cpu_state.cycles += 1
            self.cpu_state.addr_abs = ((self.cpu_state.pc + self.addr_rel) & 0xFFFF)

            if (self.cpu_state.addr_abs & 0xFF00) != (self.cpu_state.pc & 0xFF00):
                self.cpu_state.cycles += 1

            self.cpu_state.pc = self.cpu_state.addr_abs

        return 0

    def BIT(self) -> int:
        self.fetch()
        temp = self.cpu_state.a & self.cpu_state.fetched
        self.cpu_flags.Z = (temp & 0x00FF) == 0x00
        self.cpu_flags.N = self.cpu_state.fetched & (1 << 7)
        self.cpu_flags.V = self.cpu_state.fetched & (1 << 6)

        return 0

    def BMI(self) -> int:
        if self.cpu_flags.N:
            self.cpu_state.cycles += 1
            self.cpu_state.addr_abs = (self.cpu_state.pc + self.addr_rel) & 0xFFFF

            if (self.cpu_state.addr_abs & 0xFF00) != (self.cpu_state.pc & 0xFF00):
                self.cpu_state.cycles += 1

            self.cpu_state.pc = self.cpu_state.addr_abs

        return 0

    def BNE(self) -> int:
        if not self.cpu_flags.Z:
            self.cpu_state.cycles += 1
            self.cpu_state.addr_abs = (self.cpu_state.pc + self.addr_rel) & 0xFFFF

            if (self.cpu_state.addr_abs & 0xFF00) != (self.cpu_state.pc & 0xFF00):
                self.cpu_state.cycles += 1

            self.cpu_state.pc = self.cpu_state.addr_abs

        return 0

    def BPL(self) -> int:
        if not self.cpu_flags.N:
            self.cpu_state.cycles += 1
            self.cpu_state.addr_abs = (self.cpu_state.pc + self.addr_rel) & 0xFFFF

            if (self.cpu_state.addr_abs & 0xFF00) != (self.cpu_state.pc & 0xFF00):
                self.cpu_state.cycles += 1

            self.cpu_state.pc = self.cpu_state.addr_abs

        return 0

    def BRK(self) -> int:
        self.cpu_state.pc += 1

        self.cpu_flags.I = 1

        self.write(0x0100 + self.cpu_state.sp, (self.cpu_state.pc >> 8) & 0x00FF)
        self.cpu_state.sp -= 1
        self.write(0x0100 + self.cpu_state.sp, self.cpu_state.pc & 0x00FF)
        self.cpu_state.sp -= 1

        self.cpu_flags.B = 1
        
        self.write(0x0100 + self.cpu_state.sp, self.cpu_state.status)
        self.cpu_state.sp -= 1
        self.cpu_flags.B = 0

        self.cpu_state.pc = self.read(0xFFFE) | (self.read(0xFFFF) << 8)
        
        return 0

    def BVC(self) -> int:
        if not self.cpu_flags.V:
            self.cpu_state.cycles += 1
            self.cpu_state.addr_abs = (self.cpu_state.pc + self.addr_rel) & 0xFFFF

            if (self.cpu_state.addr_abs & 0xFF00) != (self.cpu_state.pc & 0xFF00):
                self.cpu_state.cycles += 1

            self.cpu_state.pc = self.cpu_state.addr_abs

        return 0

    def BVS(self) -> int:
        if self.cpu_flags.V:
            self.cpu_state.cycles += 1
            self.cpu_state.addr_abs = (self.cpu_state.pc + self.addr_rel) & 0xFFFF

            if (self.cpu_state.addr_abs & 0xFF00) != (self.cpu_state.pc & 0xFF00):
                self.cpu_state.cycles += 1

            self.cpu_state.pc = self.cpu_state.addr_abs

        return 0

    def CLC(self) -> int:
        self.cpu_flags.C = 0
        return 0

    def CLD(self) -> int:
        self.cpu_flags.D = 0
        return 0

    def CLI(self) -> int:
        self.cpu_flags.I = 0
        return 0

    def CLV(self) -> int:
        self.cpu_flags.V = 0
        return 0

    def CMP(self) -> int:
        self.fetch()
        temp = self.cpu_state.a - self.cpu_state.fetched
        self.cpu_flags.C = self.cpu_state.a >= self.cpu_state.fetched
        self.cpu_flags.Z = (temp & 0x00FF) == 0x0000
        self.cpu_flags.N = temp & 0x0080
        return 1

    def CPX(self) -> int:
        self.fetch()
        temp = self.cpu_state.x - self.cpu_state.fetched
        self.cpu_flags.C = self.cpu_state.x >= self.cpu_state.fetched
        self.cpu_flags.Z = (temp & 0x00FF) == 0x0000
        self.cpu_flags.N = temp & 0x0080
        return 0

    def CPY(self) -> int:
        self.fetch()
        temp = self.cpu_state.y - self.cpu_state.fetched
        self.cpu_flags.C = self.cpu_state.y >= self.cpu_state.fetched
        self.cpu_flags.Z = (temp & 0x00FF) == 0x0000
        self.cpu_flags.N = temp & 0x0080
        return 0

    def DEC(self) -> int:
        self.fetch()
        temp = self.cpu_state.fetched - 1
        self.write(self.cpu_state.addr_abs, temp & 0x00FF)
        self.cpu_flags.Z = (temp & 0x00FF) == 0x0000
        self.cpu_flags.N = temp & 0x0080
        return 0

    def DEX(self) -> int:
        self.cpu_state.x -= 1
        self.cpu_flags.Z = self.cpu_state.x == 0x00
        self.cpu_flags.N = self.cpu_state.x & 0x80
        return 0

    def DEY(self) -> int:
        self.cpu_state.y -= 1
        self.cpu_flags.Z = self.cpu_state.y == 0x00
        self.cpu_flags.N = self.cpu_state.y & 0x80
        return 0

    def EOR(self) -> int:
        self.fetch()
        self.cpu_state.a ^= self.cpu_state.fetched
        self.cpu_flags.Z = self.cpu_state.a == 0x00
        self.cpu_flags.N = self.cpu_state.a & 0x80
        return 1

    def INC(self) -> int:
        self.fetch()
        temp = self.cpu_state.fetched + 1
        self.write(self.cpu_state.addr_abs, temp & 0x00FF)
        self.cpu_flags.Z = (temp & 0x00FF) == 0x0000
        self.cpu_flags.N = temp & 0x0080
        return 0

    def INX(self) -> int:
        self.cpu_state.x += 1
        self.cpu_flags.Z = self.cpu_state.x == 0x00
        self.cpu_flags.N = self.cpu_state.x & 0x80
        return 0

    def INY(self) -> int:
        self.cpu_state.y += 1
        self.cpu_flags.Z = self.cpu_state.y == 0x00
        self.cpu_flags.N = self.cpu_state.y & 0x80
        return 0

    def JMP(self) -> int:
        self.cpu_state.pc = self.cpu_state.addr_abs
        return 0

    def JSR(self) -> int:
        self.cpu_state.pc -= 1

        self.write(0x0100 + self.cpu_state.sp, (self.cpu_state.pc >> 8) & 0x00FF)
        self.cpu_state.sp -= 1
        self.write(0x0100 + self.cpu_state.sp, self.cpu_state.pc & 0x00FF)
        self.cpu_state.sp -= 1
        
        self.cpu_state.pc = self.cpu_state.addr_abs
        
        return 0

    def LDA(self) -> int:
        self.fetch()
        
        self.cpu_state.a = self.cpu_state.fetched
        self.cpu_flags.Z = self.cpu_state.a == 0x00
        self.cpu_flags.N = self.cpu_state.a & 0x80
        
        return 1

    def LDX(self) -> int:
        self.fetch()
        
        self.cpu_state.x = self.cpu_state.fetched
        print(self.cpu_state.x == 0x00)

        self.cpu_flags.Z = int(self.cpu_state.x == 0x00)
        self.cpu_flags.N = self.cpu_state.x & 0x80
        
        return 1

    def LDY(self) -> int:
        self.fetch()
        
        self.cpu_state.y = self.cpu_state.fetched
        self.cpu_flags.Z = self.cpu_state.y == 0x00
        self.cpu_flags.N = self.cpu_state.y & 0x80
        
        return 1

    def LSR(self) -> int:
        self.fetch()

        self.cpu_flags.C = self.cpu_state.fetched & 0x0001
        temp = self.cpu_state.fetched >> 1

        self.cpu_flags.Z = (temp & 0x00FF) == 0x0000
        self.cpu_flags.N = temp & 0x0080

        if self.cpu_state.lookup[self.cpu_state.opcode]["addressing_mode"] == 'IMP':
            self.cpu_state.a = temp & 0x00FF
        else:
            self.write(self.cpu_state.addr_abs, temp & 0x00FF)
        return 0

    def NOP(self) -> int:
        if self.cpu_state.opcode == (0x80 | 0x82 | 0x89 | 0xC2 | 0xE2):
            return 1

        return 0

    def ORA(self) -> int:
        self.fetch()
        self.cpu_state.a |= self.cpu_state.fetched
        self.cpu_flags.Z = self.cpu_state.a == 0x00
        self.cpu_flags.N = self.cpu_state.a & 0x80
        return 1

    def PHA(self) -> int:
        self.write(0x0100 + self.cpu_state.sp, self.cpu_state.a)
        self.cpu_state.sp -= 1
        return 0

    def PHP(self) -> int:
        self.cpu_flags.B = 1
        self.cpu_flags.U = 1

        self.write(0x0100 + self.cpu_state.sp, self.cpu_state.status | self.cpu_flags.B << 4 | self.cpu_flags.U << 5)
        self.cpu_flags.B = 0 # check if the
        self.cpu_flags.U = 0
        self.cpu_state.sp -= 1
        return 0

    def PLA(self) -> int:
        self.cpu_state.sp += 1
        self.cpu_state.a = self.read(0x0100 + self.cpu_state.sp)
        self.cpu_flags.Z = self.cpu_state.a == 0x00
        self.cpu_flags.N = self.cpu_state.a & 0x80
        return 0

    def PLP(self) -> int:
        self.cpu_state.sp += 1
        self.cpu_state.status = self.read(0x0100 + self.cpu_state.sp)

        self.cpu_flags.C = (self.cpu_state.status & 0b00000001) >> 0
        self.cpu_flags.Z = (self.cpu_state.status & 0b00000010) >> 1
        self.cpu_flags.I = (self.cpu_state.status & 0b00000100) >> 2
        self.cpu_flags.D = (self.cpu_state.status & 0b00001000) >> 3
        self.cpu_flags.V = (self.cpu_state.status & 0b01000000) >> 6
        self.cpu_flags.N = (self.cpu_state.status & 0b10000000) >> 7
        self.cpu_flags.U = 1

        return 0

    def ROL(self) -> int:
        self.fetch()
        temp = (self.cpu_state.fetched << 1) | self.cpu_flags.C
        self.cpu_flags.C = temp & 0xFF00
        self.cpu_flags.Z = (temp & 0x00FF) == 0x0000
        self.cpu_flags.N = temp & 0x0080

        if self.cpu_state.lookup[self.cpu_state.opcode]["addressing_mode"] == 'IMP':
            self.cpu_state.a = temp & 0x00FF
        else:
            self.write(self.cpu_state.addr_abs, temp & 0x00FF)
        return 0

    def ROR(self) -> int:
        self.fetch()
        temp = (self.cpu_state.fetched >> 1) | (self.cpu_flags.C << 7)
        self.cpu_flags.C = self.cpu_state.fetched & 0x0001
        self.cpu_flags.Z = (temp & 0x00FF) == 0x0000
        self.cpu_flags.N = temp & 0x0080

        if self.cpu_state.lookup[self.cpu_state.opcode]["addressing_mode"] == 'IMP':
            self.cpu_state.a = temp & 0x00FF
        else:
            self.write(self.cpu_state.addr_abs, temp & 0x00FF)
        return 0

    def RTI(self) -> int:
        self.cpu_state.sp += 1
        self.cpu_state.status = self.read(0x0100 + self.cpu_state.sp)
        self.cpu_state.status &= self.cpu_flags.B
        self.cpu_state.status &= self.cpu_flags.U

        self.cpu_state.sp += 1
        self.cpu_state.pc = self.read(0x0100 + self.cpu_state.sp)
        self.cpu_state.sp += 1
        self.cpu_state.pc |= self.read(0x0100 + self.cpu_state.sp) << 8

        return 0

    def RTS(self) -> int:
        self.cpu_state.sp += 1
        self.cpu_state.pc = self.read(0x0100 + self.cpu_state.sp)
        self.cpu_state.sp += 1
        self.cpu_state.pc |= self.read(0x0100 + self.cpu_state.sp) << 8

        self.cpu_state.pc += 1
        return 0

    def SEC(self) -> int:
        self.cpu_flags.C = 1
        return 0

    def SED(self) -> int:
        self.cpu_flags.D = 1
        return 0

    def SEI(self) -> int:
        self.cpu_flags.I = 1
        return 0

    def STA(self) -> int:
        self.write(self.cpu_state.addr_abs, self.cpu_state.a)
        return 0

    def STX(self) -> int:
        self.write(self.cpu_state.addr_abs, self.cpu_state.x)
        return 0

    def STY(self) -> int:
        self.write(self.cpu_state.addr_abs, self.cpu_state.y)
        return 0

    def SBC(self) -> int:
        self.fetch()
        value = self.cpu_state.fetched ^ 0x00FF

        temp = self.cpu_state.a + value + self.cpu_flags.C
        self.cpu_flags.C = (temp > 0xFF)
        self.cpu_flags.Z = ((temp & 0x00FF) == 0x0000)
        self.cpu_flags.N = (temp & 0x80)
        self.cpu_flags.V = ((self.cpu_state.a ^ temp) & (value ^ temp) & 0x0080) #TODO: Check this
        self.cpu_state.a = temp & 0x00FF
        
        return 1

    def TAX(self) -> int:
        self.cpu_state.x = self.cpu_state.a
        self.cpu_flags.Z = self.cpu_state.x == 0x00
        self.cpu_flags.N = self.cpu_state.x & 0x80
        return 0

    def TAY(self) -> int:
        self.cpu_state.y = self.cpu_state.a
        self.cpu_flags.Z = self.cpu_state.y == 0x00
        self.cpu_flags.N = self.cpu_state.y & 0x80
        return 0

    def TSX(self) -> int:
        self.cpu_state.x = self.cpu_state.sp
        self.cpu_flags.Z = self.cpu_state.x == 0x00
        self.cpu_flags.N = self.cpu_state.x & 0x80
        return 0

    def TXA(self) -> int:
        self.cpu_state.a = self.cpu_state.x
        self.cpu_flags.Z = self.cpu_state.a == 0x00
        self.cpu_flags.N = self.cpu_state.a & 0x80
        return 0

    def TXS(self) -> int:
        self.cpu_state.sp = self.cpu_state.x
        return 0

    def TYA(self) -> int:
        self.cpu_state.a = self.cpu_state.y
        self.cpu_flags.Z = self.cpu_state.a == 0x00
        self.cpu_flags.N = self.cpu_state.a & 0x80
        return 0
    
    def XXX(self) -> int:
        return 0