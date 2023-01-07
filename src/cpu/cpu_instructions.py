from .interfaces.abstract_cpu_instructions import AbstractCpuInstructions
from .interfaces.abstract_cpu import AbstractCpu

# TODO: Implement interrupts and refactor
class CpuInstructions(AbstractCpuInstructions):
    def __init__(self, cpu: AbstractCpu):
        self.cpu: AbstractCpu = cpu

    def irq(self) -> None:
        """
        Interrupt request
        """
        # if interrupt are allowed
        if not self.cpu.state.flag_I:
            self.cpu.bus.write(0x0100 + self.cpu.state.register_SP, (self.cpu.state.register_PC >> 8) & 0x00FF)
            self.cpu.state.register_SP -= 1

            self.cpu.bus.write(0x0100 + self.cpu.state.register_SP, self.cpu.state.register_PC & 0x00FF)
            self.cpu.state.register_SP -= 1

            self.cpu.state.flag_B = bool(0)
            self.cpu.state.flag_U = bool(1)
            self.cpu.state.flag_I = bool(1)

            self.cpu.bus.write(0x0100 + self.cpu.state.register_SP, self.cpu.state.register_SR) 
            self.cpu.state.register_SP -= 1

            self.cpu.state.register_PC = self.cpu.bus.read(0xFFFE) | (self.cpu.bus.read(0xFFFF) << 8)

            self.cpu.state.cycles = 7

    def nmi(self) -> None:
        """
        Non-maskable interrupt
        """
        self.cpu.bus.write(0x0100 + self.cpu.state.register_SP, (self.cpu.state.register_PC >> 8) & 0x00FF)
        self.cpu.state.register_SP -= 1

        self.cpu.bus.write(0x0100 + self.cpu.state.register_SP, self.cpu.state.register_PC & 0x00FF)
        self.cpu.state.register_SP -= 1

        self.cpu.state.flag_B = bool(0)
        self.cpu.state.flag_U = bool(1)
        self.cpu.state.flag_I = bool(1)

        self.cpu.bus.write(0x0100 + self.cpu.state.register_SP, self.cpu.state.register_SR)
        self.cpu.state.register_SP -= 1

        self.cpu.state.register_PC = self.cpu.bus.read(0xFFFA) | (self.cpu.bus.read(0xFFFB) << 8)

        self.cpu.state.cycles = 8
    
    def ADC(self) -> int:
        self.cpu.fetch()
        temp = self.cpu.state.register_A + self.cpu.state.fetched + self.cpu.state.flag_C
        self.cpu.state.flag_C = bool(temp > 255)
        self.cpu.state.flag_Z = bool((temp & 0x00FF) == 0)
        self.cpu.state.flag_N = bool(temp & 0x80)
        self.cpu.state.flag_V = bool((~(self.cpu.state.register_A ^ self.cpu.state.fetched) & (self.cpu.state.register_A ^ temp)) & 0x0080)

        self.cpu.state.register_A = temp & 0x00FF

        return 1

    def AND(self) -> int:
        self.cpu.fetch()
        self.cpu.state.register_A &= self.cpu.state.fetched
        self.cpu.state.flag_Z = bool(self.cpu.state.register_A == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_A & 0x80)

        return 1

    def ASL(self) -> int:
        self.cpu.fetch()
        temp = self.cpu.state.fetched << 1
        self.cpu.state.flag_C = bool((temp & 0xFF00) > 0)
        self.cpu.state.flag_Z = bool((temp & 0x00FF) == 0)
        self.cpu.state.flag_N = bool(temp & 0x80)

        if self.cpu.state.current_addressing_mode == "IMP":
            self.cpu.state.register_A = temp & 0x00FF
        else:
            self.cpu.bus.write(self.cpu.state.addr_abs, temp & 0x00FF)

        return 0

    def BCC(self) -> int:
        if not self.cpu.state.flag_C:
            self.cpu.state.cycles += 1
            self.cpu.state.addr_abs = (self.cpu.state.register_PC + self.cpu.state.addr_rel) & 0xFFFF

            if (self.cpu.state.addr_abs & 0xFF00) != (self.cpu.state.register_PC & 0xFF00):
                self.cpu.state.cycles += 1

            self.cpu.state.register_PC = self.cpu.state.addr_abs

        return 0

    def BCS(self) -> int:
        if self.cpu.state.flag_C:
            self.cpu.state.cycles += 1
            self.cpu.state.addr_abs = (self.cpu.state.register_PC + self.cpu.state.addr_rel) & 0xFFFF

            if (self.cpu.state.addr_abs & 0xFF00) != (self.cpu.state.register_PC & 0xFF00):
                self.cpu.state.cycles += 1

            self.cpu.state.register_PC = self.cpu.state.addr_abs

        return 0

    def BEQ(self) -> int:
        if self.cpu.state.flag_Z:
            self.cpu.state.cycles += 1
            self.cpu.state.addr_abs = ((self.cpu.state.register_PC + self.cpu.state.addr_rel) & 0xFFFF)

            if (self.cpu.state.addr_abs & 0xFF00) != (self.cpu.state.register_PC & 0xFF00):
                self.cpu.state.cycles += 1

            self.cpu.state.register_PC = self.cpu.state.addr_abs

        return 0

    def BIT(self) -> int:
        self.cpu.fetch()
        temp = self.cpu.state.register_A & self.cpu.state.fetched
        self.cpu.state.flag_Z = bool((temp & 0x00FF) == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.fetched & (1 << 7))
        self.cpu.state.flag_V = bool(self.cpu.state.fetched & (1 << 6))

        return 0

    def BMI(self) -> int:
        if self.cpu.state.flag_N:
            self.cpu.state.cycles += 1
            self.cpu.state.addr_abs = (self.cpu.state.register_PC + self.cpu.state.addr_rel) & 0xFFFF

            if (self.cpu.state.addr_abs & 0xFF00) != (self.cpu.state.register_PC & 0xFF00):
                self.cpu.state.cycles += 1

            self.cpu.state.register_PC = self.cpu.state.addr_abs

        return 0

    def BNE(self) -> int:
        if not self.cpu.state.flag_Z:
            self.cpu.state.cycles += 1
            self.cpu.state.addr_abs = (self.cpu.state.register_PC + self.cpu.state.addr_rel) & 0xFFFF

            if (self.cpu.state.addr_abs & 0xFF00) != (self.cpu.state.register_PC & 0xFF00):
                self.cpu.state.cycles += 1

            self.cpu.state.register_PC = self.cpu.state.addr_abs

        return 0

    def BPL(self) -> int:
        if not self.cpu.state.flag_N:
            self.cpu.state.cycles += 1
            self.cpu.state.addr_abs = (self.cpu.state.register_PC + self.cpu.state.addr_rel) & 0xFFFF

            if (self.cpu.state.addr_abs & 0xFF00) != (self.cpu.state.register_PC & 0xFF00):
                self.cpu.state.cycles += 1

            self.cpu.state.register_PC = self.cpu.state.addr_abs

        return 0

    def BRK(self) -> int:
        self.cpu.state.register_PC += 1

        self.cpu.state.flag_I = bool(1)

        self.cpu.bus.write(0x0100 + self.cpu.state.register_SP, (self.cpu.state.register_PC >> 8) & 0x00FF)
        self.cpu.state.register_SP -= 1
        self.cpu.bus.write(0x0100 + self.cpu.state.register_SP, self.cpu.state.register_PC & 0x00FF)
        self.cpu.state.register_SP -= 1

        self.cpu.state.flag_B = bool(1)
        
        self.cpu.bus.write(0x0100 + self.cpu.state.register_SP, self.cpu.state.register_SR)
        self.cpu.state.register_SP -= 1
        self.cpu.state.flag_B = bool(0)

        self.cpu.state.register_PC = self.cpu.bus.read(0xFFFE) | (self.cpu.bus.read(0xFFFF) << 8)
        
        return 0

    def BVC(self) -> int:
        if not self.cpu.state.flag_V:
            self.cpu.state.cycles += 1
            self.cpu.state.addr_abs = (self.cpu.state.register_PC + self.cpu.state.addr_rel) & 0xFFFF

            if (self.cpu.state.addr_abs & 0xFF00) != (self.cpu.state.register_PC & 0xFF00):
                self.cpu.state.cycles += 1

            self.cpu.state.register_PC = self.cpu.state.addr_abs

        return 0

    def BVS(self) -> int:
        if self.cpu.state.flag_V:
            self.cpu.state.cycles += 1
            self.cpu.state.addr_abs = (self.cpu.state.register_PC + self.cpu.state.addr_rel) & 0xFFFF

            if (self.cpu.state.addr_abs & 0xFF00) != (self.cpu.state.register_PC & 0xFF00):
                self.cpu.state.cycles += 1

            self.cpu.state.register_PC = self.cpu.state.addr_abs

        return 0

    def CLC(self) -> int:
        self.cpu.state.flag_C = bool(0)
        return 0

    def CLD(self) -> int:
        self.cpu.state.flag_D = bool(0)
        return 0

    def CLI(self) -> int:
        self.cpu.state.flag_I = bool(0)
        return 0

    def CLV(self) -> int:
        self.cpu.state.flag_V = bool(0)
        return 0

    def CMP(self) -> int:
        self.cpu.fetch()
        temp = self.cpu.state.register_A - self.cpu.state.fetched
        self.cpu.state.flag_C = bool(self.cpu.state.register_A >= self.cpu.state.fetched)
        self.cpu.state.flag_Z = bool((temp & 0x00FF) == 0x0000)
        self.cpu.state.flag_N = bool(temp & 0x0080)
        return 1

    def CPX(self) -> int:
        self.cpu.fetch()
        temp = self.cpu.state.register_X - self.cpu.state.fetched
        self.cpu.state.flag_C = bool(self.cpu.state.register_X >= self.cpu.state.fetched)
        self.cpu.state.flag_Z = bool((temp & 0x00FF) == 0x0000)
        self.cpu.state.flag_N = bool(temp & 0x0080)
        return 0

    def CPY(self) -> int:
        self.cpu.fetch()
        temp = self.cpu.state.register_Y - self.cpu.state.fetched
        self.cpu.state.flag_C = bool(self.cpu.state.register_Y >= self.cpu.state.fetched)
        self.cpu.state.flag_Z = bool((temp & 0x00FF) == 0x0000)
        self.cpu.state.flag_N = bool(temp & 0x0080)
        return 0

    def DEC(self) -> int:
        self.cpu.fetch()
        temp = self.cpu.state.fetched - 1
        self.cpu.bus.write(self.cpu.state.addr_abs, temp & 0x00FF)
        self.cpu.state.flag_Z = bool((temp & 0x00FF) == 0x0000)
        self.cpu.state.flag_N = bool(temp & 0x0080)
        return 0

    def DEX(self) -> int:
        self.cpu.state.register_X -= 1
        self.cpu.state.flag_Z = bool(self.cpu.state.register_X == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_X & 0x80)
        return 0

    def DEY(self) -> int:
        self.cpu.state.register_Y -= 1
        self.cpu.state.flag_Z = bool(self.cpu.state.register_Y == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_Y & 0x80)
        return 0

    def EOR(self) -> int:
        self.cpu.fetch()
        self.cpu.state.register_A ^= self.cpu.state.fetched
        self.cpu.state.flag_Z = bool(self.cpu.state.register_A == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_A & 0x80)
        return 1

    def INC(self) -> int:
        self.cpu.fetch()
        temp = self.cpu.state.fetched + 1
        self.cpu.bus.write(self.cpu.state.addr_abs, temp & 0x00FF)
        self.cpu.state.flag_Z = bool((temp & 0x00FF) == 0x0000)
        self.cpu.state.flag_N = bool(temp & 0x0080)
        return 0

    def INX(self) -> int:
        self.cpu.state.register_X += 1
        self.cpu.state.flag_Z = bool(self.cpu.state.register_X == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_X & 0x80)
        return 0

    def INY(self) -> int:
        self.cpu.state.register_Y += 1
        self.cpu.state.flag_Z = bool(self.cpu.state.register_Y == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_Y & 0x80)
        return 0

    def JMP(self) -> int:
        self.cpu.state.register_PC = self.cpu.state.addr_abs
        return 0

    def JSR(self) -> int:
        self.cpu.state.register_PC -= 1

        self.cpu.bus.write(0x0100 + self.cpu.state.register_SP, (self.cpu.state.register_PC >> 8) & 0x00FF)
        self.cpu.state.register_SP -= 1
        self.cpu.bus.write(0x0100 + self.cpu.state.register_SP, self.cpu.state.register_PC & 0x00FF)
        self.cpu.state.register_SP -= 1
        
        self.cpu.state.register_PC = self.cpu.state.addr_abs
        
        return 0

    def LDA(self) -> int:
        self.cpu.fetch()
        
        self.cpu.state.register_A = self.cpu.state.fetched
        self.cpu.state.flag_Z = bool(self.cpu.state.register_A == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_A & 0x80)
        
        return 1

    def LDX(self) -> int:
        self.cpu.fetch()
        
        self.cpu.state.register_X = self.cpu.state.fetched

        self.cpu.state.flag_Z = bool(int(self.cpu.state.register_X == 0x00))
        self.cpu.state.flag_N = bool(self.cpu.state.register_X & 0x80)
        
        return 1

    def LDY(self) -> int:
        self.cpu.fetch()
        
        self.cpu.state.register_Y = self.cpu.state.fetched
        self.cpu.state.flag_Z = bool(self.cpu.state.register_Y == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_Y & 0x80)
        
        return 1

    def LSR(self) -> int:
        self.cpu.fetch()

        self.cpu.state.flag_C = bool(self.cpu.state.fetched & 0x0001)
        temp = self.cpu.state.fetched >> 1

        self.cpu.state.flag_Z = bool((temp & 0x00FF) == 0x0000)
        self.cpu.state.flag_N = bool(temp & 0x0080)

        if self.cpu.state.current_addressing_mode == 'IMP':
            self.cpu.state.register_A = temp & 0x00FF
        else:
            self.cpu.bus.write(self.cpu.state.addr_abs, temp & 0x00FF)
        return 0

    def NOP(self) -> int:
        if self.cpu.state.opcode == (0x80 | 0x82 | 0x89 | 0xC2 | 0xE2):
            return 1

        return 0

    def ORA(self) -> int:
        self.cpu.fetch()
        self.cpu.state.register_A |= self.cpu.state.fetched
        self.cpu.state.flag_Z = bool(self.cpu.state.register_A == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_A & 0x80)
        return 1

    def PHA(self) -> int:
        self.cpu.bus.write(0x0100 + self.cpu.state.register_SP, self.cpu.state.register_A)
        self.cpu.state.register_SP -= 1
        return 0

    def PHP(self) -> int:
        self.cpu.state.flag_B = bool(1)
        self.cpu.state.flag_U = bool(1)

        self.cpu.bus.write(0x0100 + self.cpu.state.register_SP, self.cpu.state.register_SR | self.cpu.state.flag_B << 4 | self.cpu.state.flag_U << 5)
        self.cpu.state.flag_B = bool(0) # check if the
        self.cpu.state.flag_U = bool(0)
        self.cpu.state.register_SP -= 1
        return 0

    def PLA(self) -> int:
        self.cpu.state.register_SP += 1
        self.cpu.state.register_A = self.cpu.bus.read(0x0100 + self.cpu.state.register_SP)
        self.cpu.state.flag_Z = bool(self.cpu.state.register_A == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_A & 0x80)
        return 0

    def PLP(self) -> int:
        self.cpu.state.register_SP += 1
        self.cpu.state.register_SR = self.cpu.bus.read(0x0100 + self.cpu.state.register_SP)

        self.cpu.state.flag_U = bool(1)

        return 0

    def ROL(self) -> int:
        self.cpu.fetch()
        temp = (self.cpu.state.fetched << 1) | self.cpu.state.flag_C
        self.cpu.state.flag_C = bool(temp & 0xFF00)
        self.cpu.state.flag_Z = bool((temp & 0x00FF) == 0x0000)
        self.cpu.state.flag_N = bool(temp & 0x0080)

        if self.cpu.state.current_addressing_mode == 'IMP':
            self.cpu.state.register_A = temp & 0x00FF
        else:
            self.cpu.bus.write(self.cpu.state.addr_abs, temp & 0x00FF)
        return 0

    def ROR(self) -> int:
        self.cpu.fetch()
        temp = (self.cpu.state.fetched >> 1) | (self.cpu.state.flag_C << 7)
        self.cpu.state.flag_C = bool(self.cpu.state.fetched & 0x0001)
        self.cpu.state.flag_Z = bool((temp & 0x00FF) == 0x0000)
        self.cpu.state.flag_N = bool(temp & 0x0080)

        if self.cpu.state.current_addressing_mode == 'IMP':
            self.cpu.state.register_A = temp & 0x00FF
        else:
            self.cpu.bus.write(self.cpu.state.addr_abs, temp & 0x00FF)
        return 0

    def RTI(self) -> int:
        self.cpu.state.register_SP += 1
        self.cpu.state.register_SR = self.cpu.bus.read(0x0100 + self.cpu.state.register_SP)
        
        self.cpu.state.flag_B = bool(0)
        self.cpu.state.flag_U = bool(0)

        self.cpu.state.register_SP += 1
        self.cpu.state.register_PC = self.cpu.bus.read(0x0100 + self.cpu.state.register_SP)
        self.cpu.state.register_SP += 1
        self.cpu.state.register_PC |= self.cpu.bus.read(0x0100 + self.cpu.state.register_SP) << 8

        return 0

    def RTS(self) -> int:
        self.cpu.state.register_SP += 1
        self.cpu.state.register_PC = self.cpu.bus.read(0x0100 + self.cpu.state.register_SP)
        self.cpu.state.register_SP += 1
        self.cpu.state.register_PC |= self.cpu.bus.read(0x0100 + self.cpu.state.register_SP) << 8

        self.cpu.state.register_PC += 1
        return 0

    def SEC(self) -> int:
        self.cpu.state.flag_C = bool(1)

        return 0

    def SED(self) -> int:
        self.cpu.state.flag_D = bool(1)

        return 0

    def SEI(self) -> int:
        self.cpu.state.flag_I = bool(1)

        return 0

    def STA(self) -> int:
        self.cpu.bus.write(self.cpu.state.addr_abs, self.cpu.state.register_A)
        return 0

    def STX(self) -> int:
        self.cpu.bus.write(self.cpu.state.addr_abs, self.cpu.state.register_X)
        return 0

    def STY(self) -> int:
        self.cpu.bus.write(self.cpu.state.addr_abs, self.cpu.state.register_Y)
        return 0

    def SBC(self) -> int:
        self.cpu.fetch()
        value = self.cpu.state.fetched ^ 0x00FF

        temp = self.cpu.state.register_A + value + self.cpu.state.flag_C
        self.cpu.state.flag_C = bool(temp > 0xFF)
        self.cpu.state.flag_Z = bool((temp & 0x00FF) == 0x0000)
        self.cpu.state.flag_N = bool(temp & 0x80)
        self.cpu.state.flag_V = bool((self.cpu.state.register_A ^ temp) & (value ^ temp) & 0x0080) #TODO: Check this
        self.cpu.state.register_A = temp & 0x00FF
        
        return 1

    def TAX(self) -> int:
        self.cpu.state.register_X = self.cpu.state.register_A
        self.cpu.state.flag_Z = bool(self.cpu.state.register_X == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_X & 0x80)
        return 0

    def TAY(self) -> int:
        self.cpu.state.register_Y = self.cpu.state.register_A
        self.cpu.state.flag_Z = bool(self.cpu.state.register_Y == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_Y & 0x80)
        return 0

    def TSX(self) -> int:
        self.cpu.state.register_X = self.cpu.state.register_SP
        self.cpu.state.flag_Z = bool(self.cpu.state.register_X == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_X & 0x80)
        return 0

    def TXA(self) -> int:
        self.cpu.state.register_A = self.cpu.state.register_X
        self.cpu.state.flag_Z = bool(self.cpu.state.register_A == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_A & 0x80)
        return 0

    def TXS(self) -> int:
        self.cpu.state.register_SP = self.cpu.state.register_X
        return 0

    def TYA(self) -> int:
        self.cpu.state.register_A = self.cpu.state.register_Y
        self.cpu.state.flag_Z = bool(self.cpu.state.register_A == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_A & 0x80)
        return 0
    
    def XXX(self) -> int:
        return 0