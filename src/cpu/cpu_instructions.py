from .interfaces.abstract_cpu_instructions import AbstractCpuInstructions
from .interfaces.abstract_cpu import AbstractCpu

# TODO: Implement interrupts and refactor
class CpuInstructions(AbstractCpuInstructions):
    def __init__(self, cpu: AbstractCpu):
        self.cpu: AbstractCpu = cpu

    def irq(self) -> None:
        """
        Handles the Interrupt Request (IRQ) instruction.
        
        This instruction allows other devices to request attention from the CPU. If interrupts are enabled,
        this instruction saves the current program counter and status register on the stack, sets the 
        interrupt disable flag, and transfers control to the interrupt vector at address $FFFE/$FFFF.
        
        :return: None
        """
        # if interrupts are enabled
        if not self.cpu.state.flag_I:
            # push the current program counter onto the stack
            self.cpu.bus.write(0x0100 + self.cpu.state.register_SP, (self.cpu.state.register_PC >> 8) & 0x00FF)
            self.cpu.state.register_SP -= 1

            self.cpu.bus.write(0x0100 + self.cpu.state.register_SP, self.cpu.state.register_PC & 0x00FF)
            self.cpu.state.register_SP -= 1

            # clear the break flag, set the unused flag, and set the interrupt disable flag
            self.cpu.state.flag_B = bool(0)
            self.cpu.state.flag_U = bool(1)
            self.cpu.state.flag_I = bool(1)
            
            # push the current status register onto the stack
            self.cpu.bus.write(0x0100 + self.cpu.state.register_SP, self.cpu.state.register_SR) 
            self.cpu.state.register_SP -= 1

            # load the interrupt vector into the program counter
            self.cpu.state.register_PC = self.cpu.bus.read(0xFFFE) | (self.cpu.bus.read(0xFFFF) << 8)

            # update the cycle count
            self.cpu.state.cycles = 7

    def nmi(self) -> None:
        """
        Handles the Non-Maskable Interrupt (NMI) instruction.
        
        This instruction allows devices with a higher priority to request attention from the CPU. This 
        instruction saves the current program counter and status register on the stack, sets the interrupt 
        disable flag, and transfers control to the interrupt vector at address $FFFA/$FFFB.
        
        :return: None
        """
        # push the current program counter onto the stack
        self.cpu.bus.write(0x0100 + self.cpu.state.register_SP, (self.cpu.state.register_PC >> 8) & 0x00FF)
        self.cpu.state.register_SP -= 1

        self.cpu.bus.write(0x0100 + self.cpu.state.register_SP, self.cpu.state.register_PC & 0x00FF)
        self.cpu.state.register_SP -= 1

        # clear the break flag, set the unused flag, and set the interrupt disable flag
        self.cpu.state.flag_B = bool(0)
        self.cpu.state.flag_U = bool(1)
        self.cpu.state.flag_I = bool(1)

        # push the current status register onto the stack
        self.cpu.bus.write(0x0100 + self.cpu.state.register_SP, self.cpu.state.register_SR)
        self.cpu.state.register_SP -= 1

        # load the interrupt vector into the program counter
        self.cpu.state.register_PC = self.cpu.bus.read(0xFFFA) | (self.cpu.bus.read(0xFFFB) << 8)

        self.cpu.state.cycles = 8
    
    def ADC(self) -> int:
        """
        Handles the Add with Carry (ADC) instruction.
        
        This instruction adds the value of a memory location to the value of the accumulator, along with the
        carry flag. The result is stored in the accumulator.
        
        :return: The number of cycles taken to execute the instruction.
        """
        # fetch the value to be added
        self.cpu.fetch()

        # create a temporary variable to hold the result of the addition
        temp = self.cpu.state.register_A + self.cpu.state.fetched + self.cpu.state.flag_C

        # set the carry flag if the result is greater than 255
        self.cpu.state.flag_C = bool(temp > 255)

        # set the zero flag if the result is zero
        self.cpu.state.flag_Z = bool((temp & 0x00FF) == 0)

        # set the negative flag if the result is negative
        self.cpu.state.flag_N = bool(temp & 0x80)

        # set the overflow flag if the result is greater than 127 or less than -128
        self.cpu.state.flag_V = bool((~(self.cpu.state.register_A ^ self.cpu.state.fetched) & (self.cpu.state.register_A ^ temp)) & 0x0080)

        # store the result in the accumulator
        self.cpu.state.register_A = temp & 0x00FF

        return 1

    def AND(self) -> int:
        """
        Handles the AND (bitwise AND) instruction.
        
        This instruction performs a bitwise AND operation between the value of a memory location and the 
        value of the accumulator, and stores the result in the accumulator.
        
        :return: The number of cycles taken to execute the instruction.
        """
        # fetch the value to be ANDed
        self.cpu.fetch()

        # AND the value with the accumulator
        self.cpu.state.register_A &= self.cpu.state.fetched

        # set the zero flag if the result is zero
        self.cpu.state.flag_Z = bool(self.cpu.state.register_A == 0x00)

        # set the negative flag if the result is negative
        self.cpu.state.flag_N = bool(self.cpu.state.register_A & 0x80)

        return 1

    def ASL(self) -> int:
        """
        Handles the Arithmetic Shift Left (ASL) instruction.
        
        This instruction shifts the value of a memory location or the accumulator one bit to the left, 
        setting the carry flag to the value of the high bit and clearing the low bit.
        
        :return: The number of cycles taken to execute the instruction.
        """
        # fetch the value to be shifted
        self.cpu.fetch()

        # shift the value one bit to the left
        temp = self.cpu.state.fetched << 1

        # set the carry flag if the result is greater than 255
        self.cpu.state.flag_C = bool((temp & 0xFF00) > 0)

        # set the zero flag if the result is zero
        self.cpu.state.flag_Z = bool((temp & 0x00FF) == 0)

        # set the negative flag if the result is negative
        self.cpu.state.flag_N = bool(temp & 0x80)

        # if the operation is being performed on the accumulator, store the result in the accumulator
        if self.cpu.state.current_addressing_mode == "IMP":
            self.cpu.state.register_A = temp & 0x00FF
        else:
            self.cpu.bus.write(self.cpu.state.addr_abs, temp & 0x00FF)

        return 0

    def BIT(self) -> int:
        """
        Handles the BIT (bit test) instruction.
        
        This instruction performs a bitwise AND operation between the value of a memory location and the 
        value of the accumulator, setting the zero flag if the result is zero and the negative and 
        overflow flags to the values of bits 6 and 7 of the memory location, respectively.
        
        :return: The number of cycles taken to execute the instruction.
        """
        # fetch the value to be ANDed with the accumulator
        self.cpu.fetch()

        # AND the value with the accumulator, also storing the result in a temporary variable
        temp = self.cpu.state.register_A & self.cpu.state.fetched

        # set the zero flag if the result is zero
        self.cpu.state.flag_Z = bool((temp & 0x00FF) == 0x00)

        # set the negative and overflow flags to the values of bits 6 and 7 of the memory location
        self.cpu.state.flag_N = bool(self.cpu.state.fetched & (1 << 7))
        self.cpu.state.flag_V = bool(self.cpu.state.fetched & (1 << 6))

        return 0

    def BCC(self) -> int:
        """
        Handles the Branch on Carry Clear (BCC) instruction.
        
        This instruction branches to a new location if the carry flag is clear.
        
        :return: The number of cycles taken to execute the instruction.
        """
        if not self.cpu.state.flag_C:
            self.cpu.state.cycles += 1
            self.cpu.state.addr_abs = (self.cpu.state.register_PC + self.cpu.state.addr_rel) & 0xFFFF

            if (self.cpu.state.addr_abs & 0xFF00) != (self.cpu.state.register_PC & 0xFF00):
                self.cpu.state.cycles += 1

            self.cpu.state.register_PC = self.cpu.state.addr_abs

        return 0

    def BCS(self) -> int:
        """
        Handles the Branch on Carry Set (BCS) instruction.
        
        This instruction branches to a new location if the carry flag is set.
        
        :return: The number of cycles taken to execute the instruction.
        """
        if self.cpu.state.flag_C:
            self.cpu.state.cycles += 1
            self.cpu.state.addr_abs = (self.cpu.state.register_PC + self.cpu.state.addr_rel) & 0xFFFF

            if (self.cpu.state.addr_abs & 0xFF00) != (self.cpu.state.register_PC & 0xFF00):
                self.cpu.state.cycles += 1

            self.cpu.state.register_PC = self.cpu.state.addr_abs

        return 0

    def BEQ(self) -> int:
        """
        Handles the Branch on Equal (BEQ) instruction.
        
        This instruction branches to a new location if the zero flag is set.
        
        :return: The number of cycles taken to execute the instruction.
        """
        if self.cpu.state.flag_Z:
            self.cpu.state.cycles += 1
            self.cpu.state.addr_abs = ((self.cpu.state.register_PC + self.cpu.state.addr_rel) & 0xFFFF)

            if (self.cpu.state.addr_abs & 0xFF00) != (self.cpu.state.register_PC & 0xFF00):
                self.cpu.state.cycles += 1

            self.cpu.state.register_PC = self.cpu.state.addr_abs

        return 0

    def BMI(self) -> int:
        """
        Handles the Branch on Minus (BMI) instruction.
        
        This instruction branches to a new location if the negative flag is set.
        
        :return: The number of cycles taken to execute the instruction.
        """
        if self.cpu.state.flag_N:
            self.cpu.state.cycles += 1
            self.cpu.state.addr_abs = (self.cpu.state.register_PC + self.cpu.state.addr_rel) & 0xFFFF

            if (self.cpu.state.addr_abs & 0xFF00) != (self.cpu.state.register_PC & 0xFF00):
                self.cpu.state.cycles += 1

            self.cpu.state.register_PC = self.cpu.state.addr_abs

        return 0

    def BNE(self) -> int:
        """
        Handles the Branch on Not Equal (BNE) instruction.
        
        This instruction branches to a new location if the zero flag is clear.
        
        :return: The number of cycles taken to execute the instruction.
        """
        if not self.cpu.state.flag_Z:
            self.cpu.state.cycles += 1
            self.cpu.state.addr_abs = (self.cpu.state.register_PC + self.cpu.state.addr_rel) & 0xFFFF

            if (self.cpu.state.addr_abs & 0xFF00) != (self.cpu.state.register_PC & 0xFF00):
                self.cpu.state.cycles += 1

            self.cpu.state.register_PC = self.cpu.state.addr_abs

        return 0

    def BPL(self) -> int:
        """
        Handles the Branch on Plus (BPL) instruction.
        
        This instruction branches to a new location if the negative flag is clear.
        
        :return: The number of cycles taken to execute the instruction.
        """
        # if the negative flag is clear, branch to the new location
        if not self.cpu.state.flag_N:
            self.cpu.state.cycles += 1
            self.cpu.state.addr_abs = (self.cpu.state.register_PC + self.cpu.state.addr_rel) & 0xFFFF

            if (self.cpu.state.addr_abs & 0xFF00) != (self.cpu.state.register_PC & 0xFF00):
                self.cpu.state.cycles += 1

            self.cpu.state.register_PC = self.cpu.state.addr_abs

        return 0

    def BRK(self) -> int:
        """
        Handles the BRK (break) instruction.
        
        This instruction causes a non-maskable interrupt and increments the program counter by 1.

        :return: The number of cycles taken to execute the instruction.
        """
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
        """
        Handles the Branch on oVerflow Clear (BVC) instruction.
        
        This instruction branches to a new location if the overflow flag is clear.
        
        :return: The number of cycles taken to execute the instruction.
        """
        if not self.cpu.state.flag_V:
            self.cpu.state.cycles += 1
            self.cpu.state.addr_abs = (self.cpu.state.register_PC + self.cpu.state.addr_rel) & 0xFFFF

            if (self.cpu.state.addr_abs & 0xFF00) != (self.cpu.state.register_PC & 0xFF00):
                self.cpu.state.cycles += 1

            self.cpu.state.register_PC = self.cpu.state.addr_abs

        return 0

    def BVS(self) -> int:
        """
        Handles the Branch on oVerflow Set (BVS) instruction.
        
        This instruction branches to a new location if the overflow flag is set.
        
        :return: The number of cycles taken to execute the instruction.
        """
        if self.cpu.state.flag_V:
            self.cpu.state.cycles += 1
            self.cpu.state.addr_abs = (self.cpu.state.register_PC + self.cpu.state.addr_rel) & 0xFFFF

            if (self.cpu.state.addr_abs & 0xFF00) != (self.cpu.state.register_PC & 0xFF00):
                self.cpu.state.cycles += 1

            self.cpu.state.register_PC = self.cpu.state.addr_abs

        return 0

    def CLC(self) -> int:
        """
        Handles the CLear Carry (CLC) instruction.
        
        This instruction clears the carry flag.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.state.flag_C = bool(0)
        return 0

    def CLD(self) -> int:
        """
        Handles the CLear Decimal (CLD) instruction.
        
        This instruction clears the decimal mode flag.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.state.flag_D = bool(0)
        return 0

    def CLI(self) -> int:
        """
        Handles the CLear Interrupt (CLI) instruction.
        
        This instruction clears the interrupt disable flag.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.state.flag_I = bool(0)
        return 0

    def CLV(self) -> int:
        """
        Handles the CLear oVerflow (CLV) instruction.
        
        This instruction clears the overflow flag.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.state.flag_V = bool(0)
        return 0

    def CMP(self) -> int:
        """
        Handles the CoMPare (CMP) instruction.
        
        This instruction compares the accumulator to a value from memory and sets the zero, negative, and carry 
        flags based on the result.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.fetch()
        temp = self.cpu.state.register_A - self.cpu.state.fetched
        self.cpu.state.flag_C = bool(self.cpu.state.register_A >= self.cpu.state.fetched)
        self.cpu.state.flag_Z = bool((temp & 0x00FF) == 0x0000)
        self.cpu.state.flag_N = bool(temp & 0x0080)
        return 1

    def CPX(self) -> int:
        """
        Handles the ComPare X register (CPX) instruction.
        
        This instruction compares the X register to a value from
        memory and sets the zero, negative, and carry flags based on the result.

        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.fetch()
        temp = self.cpu.state.register_X - self.cpu.state.fetched
        self.cpu.state.flag_C = bool(self.cpu.state.register_X >= self.cpu.state.fetched)
        self.cpu.state.flag_Z = bool((temp & 0x00FF) == 0x0000)
        self.cpu.state.flag_N = bool(temp & 0x0080)
        return 0

    def CPY(self) -> int:
        """
        Handles the ComPare Y register (CPY) instruction.
        
        This instruction compares the Y register to a value from memory and sets the zero, negative, and carry 
        flags based on the result.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.fetch()
        temp = self.cpu.state.register_Y - self.cpu.state.fetched
        self.cpu.state.flag_C = bool(self.cpu.state.register_Y >= self.cpu.state.fetched)
        self.cpu.state.flag_Z = bool((temp & 0x00FF) == 0x0000)
        self.cpu.state.flag_N = bool(temp & 0x0080)
        return 0

    def DEC(self) -> int:
        """
        Handles the DECrement (DEC) instruction.
        
        This instruction decrements a value in memory and sets the zero and negative flags based on the result.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.fetch()
        temp = self.cpu.state.fetched - 1
        self.cpu.bus.write(self.cpu.state.addr_abs, temp & 0x00FF)
        self.cpu.state.flag_Z = bool((temp & 0x00FF) == 0x0000)
        self.cpu.state.flag_N = bool(temp & 0x0080)
        return 0

    def DEX(self) -> int:
        """
        Handles the DEcrement X register (DEX) instruction.
        
        This instruction decrements the X register and sets the zero and negative flags based on the result.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.state.register_X -= 1
        self.cpu.state.flag_Z = bool(self.cpu.state.register_X == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_X & 0x80)
        return 0

    def DEY(self) -> int:
        """
        Handles the DEcrement Y register (DEY) instruction.
        
        This instruction decrements the Y register and sets the zero and negative flags based on the result.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.state.register_Y -= 1
        self.cpu.state.flag_Z = bool(self.cpu.state.register_Y == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_Y & 0x80)
        return 0

    def EOR(self) -> int:
        """
        Handles the Exclusive OR (EOR) instruction.
        
        This instruction performs an exclusive OR operation between the accumulator and a value from memory, and stores
        the result in the accumulator. The zero and negative flags are set based on the result.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.fetch()
        self.cpu.state.register_A ^= self.cpu.state.fetched
        self.cpu.state.flag_Z = bool(self.cpu.state.register_A == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_A & 0x80)
        return 1

    def INC(self) -> int:
        """
        Handles the INCrement (INC) instruction.
        
        This instruction increments a value in memory and sets the zero and negative flags based on the result.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.fetch()
        temp = self.cpu.state.fetched + 1
        self.cpu.bus.write(self.cpu.state.addr_abs, temp & 0x00FF)
        self.cpu.state.flag_Z = bool((temp & 0x00FF) == 0x0000)
        self.cpu.state.flag_N = bool(temp & 0x0080)
        return 0

    def INX(self) -> int:
        """
        Handles the INcrement X register (INX) instruction.
        
        This instruction increments the X register and sets the zero and negative flags based on the result.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.state.register_X += 1
        self.cpu.state.flag_Z = bool(self.cpu.state.register_X == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_X & 0x80)
        return 0

    def INY(self) -> int:
        """
        Handles the INcrement Y register (INY) instruction.

        This instruction increments the Y register and sets the zero and negative flags based on the result.

        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.state.register_Y += 1
        self.cpu.state.flag_Z = bool(self.cpu.state.register_Y == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_Y & 0x80)
        return 0

    def JMP(self) -> int:
        """
        Handles the JuMP (JMP) instruction.
        
        This instruction sets the program counter to a new address.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.state.register_PC = self.cpu.state.addr_abs
        return 0

    def JSR(self) -> int:
        """
        Handles the Jump to SubRoutine (JSR) instruction.
        
        This instruction pushes the current program counter to the stack and sets the program counter to a new address.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.state.register_PC -= 1

        self.cpu.bus.write(0x0100 + self.cpu.state.register_SP, (self.cpu.state.register_PC >> 8) & 0x00FF)
        self.cpu.state.register_SP -= 1
        self.cpu.bus.write(0x0100 + self.cpu.state.register_SP, self.cpu.state.register_PC & 0x00FF)
        self.cpu.state.register_SP -= 1
        
        self.cpu.state.register_PC = self.cpu.state.addr_abs
        
        return 0

    def LDA(self) -> int:
        """
        Handles the LoaD Accumulator (LDA) instruction.

        This instruction loads a value into the accumulator and sets the zero and negative flags based on the result.

        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.fetch()
        
        self.cpu.state.register_A = self.cpu.state.fetched
        self.cpu.state.flag_Z = bool(self.cpu.state.register_A == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_A & 0x80)
        
        return 1

    def LDX(self) -> int:
        """
        Handles the LoaD X register (LDX) instruction.
        
        This instruction loads a value into the X register and sets the zero and negative flags based on the result.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.fetch()
        
        self.cpu.state.register_X = self.cpu.state.fetched

        self.cpu.state.flag_Z = bool(int(self.cpu.state.register_X == 0x00))
        self.cpu.state.flag_N = bool(self.cpu.state.register_X & 0x80)
        
        return 1

    def LDY(self) -> int:
        """
        Handles the LoaD Y register (LDY) instruction.
        
        This instruction loads a value into the Y register and sets the zero and negative flags based on the result.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.fetch()
        
        self.cpu.state.register_Y = self.cpu.state.fetched
        self.cpu.state.flag_Z = bool(self.cpu.state.register_Y == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_Y & 0x80)
        
        return 1

    def LSR(self) -> int:
        """
        Handles the Logical Shift Right (LSR) instruction.
        
        This instruction performs a logical shift right on a value in memory, and stores the result in the value. The zero
        and carry flags are set based on the result.
        
        :return: The number of cycles taken to execute the instruction.
        """
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
        """
        Handles the NO-OPeration (NOP) instruction.
        
        This instruction does nothing.
        
        :return: The number of cycles taken to execute the instruction.
        """
        if self.cpu.state.opcode == (0x80 | 0x82 | 0x89 | 0xC2 | 0xE2):
            return 1

        return 0

    def ORA(self) -> int:
        """
        Handles the bitwise OR with A (ORA) instruction.
        
        This instruction performs a bitwise OR operation on the accumulator with a value in memory and stores the result in
        the accumulator. The zero and negative flags are set based on the result.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.fetch()
        self.cpu.state.register_A |= self.cpu.state.fetched
        self.cpu.state.flag_Z = bool(self.cpu.state.register_A == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_A & 0x80)
        return 1

    def PHA(self) -> int:
        """
        Handles the PusH Accumulator (PHA) instruction.
        
        This instruction pushes the accumulator to the stack.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.bus.write(0x0100 + self.cpu.state.register_SP, self.cpu.state.register_A)
        self.cpu.state.register_SP -= 1
        return 0

    def PHP(self) -> int:
        """
        Handles the PusH Processor status (PHP) instruction.

        This instruction pushes the processor status to the stack.

        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.state.flag_B = bool(1)
        self.cpu.state.flag_U = bool(1)

        self.cpu.bus.write(0x0100 + self.cpu.state.register_SP, self.cpu.state.register_SR | self.cpu.state.flag_B << 4 | self.cpu.state.flag_U << 5)
        self.cpu.state.flag_B = bool(0) # check if the
        self.cpu.state.flag_U = bool(0)
        self.cpu.state.register_SP -= 1
        return 0

    def PLA(self) -> int:
        """
        Handles the PuLL Accumulator (PLA) instruction.
        
        This instruction pulls the top value from the stack into the accumulator and sets the zero and negative flags based
        on the result.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.state.register_SP += 1
        self.cpu.state.register_A = self.cpu.bus.read(0x0100 + self.cpu.state.register_SP)
        self.cpu.state.flag_Z = bool(self.cpu.state.register_A == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_A & 0x80)
        return 0

    def PLP(self) -> int:
        """
        Handles the PuLL Processor status (PLP) instruction.

        This instruction pulls the top value from the stack into the processor status and sets the zero and negative flags

        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.state.register_SP += 1
        self.cpu.state.register_SR = self.cpu.bus.read(0x0100 + self.cpu.state.register_SP)

        self.cpu.state.flag_U = bool(1)

        return 0

    def ROL(self) -> int:
        """
        Handles the ROtate Left (ROL) instruction.
        
        This instruction performs a rotate left on a value in memory, and stores the result in the value. The zero and carry
        flags are set based on the result.
        
        :return: The number of cycles taken to execute the instruction.
        """
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
        """
        Handles the ROtate Right (ROR) instruction.
        
        This instruction performs a rotate right on a value in memory, and stores the result in the value. The zero and carry
        flags are set based on the result.
        
        :return: The number of cycles taken to execute the instruction.
        """
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
        """
        Handles the ReTurn from Interrupt (RTI) instruction.
        
        This instruction is used to return from an interrupt handler. It pulls the processor status
        register and the program counter from the stack, restoring the processor to the state it was
        in before the interrupt occurred.
        
        :return: The number of cycles taken to execute the instruction.
        """
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
        """
        Handles the ReTurn from Subroutine (RTS) instruction.
        
        This instruction pulls the program counter from the stack and returns from a subroutine.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.state.register_SP += 1
        self.cpu.state.register_PC = self.cpu.bus.read(0x0100 + self.cpu.state.register_SP)
        self.cpu.state.register_SP += 1
        self.cpu.state.register_PC |= self.cpu.bus.read(0x0100 + self.cpu.state.register_SP) << 8

        self.cpu.state.register_PC += 1
        return 0

    def SEC(self) -> int:
        """
        Handles the SEt Carry (SEC) instruction.
        
        This instruction sets the carry flag in the processor status register to 1.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.state.flag_C = bool(1)

        return 0

    def SED(self) -> int:
        """
        Handles the SEt Decimal (SED) instruction.
        
        This instruction sets the decimal flag in the processor status register to 1.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.state.flag_D = bool(1)

        return 0

    def SEI(self) -> int:
        """
        Handles the SEt Interrupt (SEI) instruction.
        
        This instruction sets the interrupt disable flag in the processor status register to 1.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.state.flag_I = bool(1)

        return 0

    def STA(self) -> int:
        """
        Handles the STore Accumulator (STA) instruction.
        
        This instruction stores the value in the accumulator register in memory at the specified
        address.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.bus.write(self.cpu.state.addr_abs, self.cpu.state.register_A)
        return 0

    def STX(self) -> int:
        """
        Handles the STore X register (STX) instruction.
        
        This instruction stores the value in the X register in memory at the specified address.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.bus.write(self.cpu.state.addr_abs, self.cpu.state.register_X)
        return 0

    def STY(self) -> int:
        """
        Handles the STore Y register (STY) instruction.
        
        This instruction stores the value in the Y register in memory at the specified address.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.bus.write(self.cpu.state.addr_abs, self.cpu.state.register_Y)
        return 0

    def SBC(self) -> int:
        """
        Handles the SuBtract with Carry (SBC) instruction.
        
        This instruction subtracts the value at the specified memory address from the accumulator
        register, along with the value of the carry flag. The result is stored in the accumulator.
        
        :return: The number of cycles taken to execute the instruction.
        """
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
        """
        Handles the Transfer Accumulator to X (TAX) instruction.
        
        This instruction transfers the value in the accumulator register to the X register.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.state.register_X = self.cpu.state.register_A
        self.cpu.state.flag_Z = bool(self.cpu.state.register_X == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_X & 0x80)
        return 0

    def TAY(self) -> int:
        """
        Handles the Transfer Accumulator to Y (TAY) instruction.
        
        This instruction transfers the value in the accumulator register to the Y register.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.state.register_Y = self.cpu.state.register_A
        self.cpu.state.flag_Z = bool(self.cpu.state.register_Y == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_Y & 0x80)
        return 0

    def TSX(self) -> int:
        """
        Handles the Transfer Stack Pointer to X (TSX) instruction.
        
        This instruction transfers the value in the stack pointer register to the X register.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.state.register_X = self.cpu.state.register_SP
        self.cpu.state.flag_Z = bool(self.cpu.state.register_X == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_X & 0x80)
        return 0

    def TXA(self) -> int:
        """
        Handles the Transfer X to Accumulator (TXA) instruction.
        
        This instruction transfers the value in the X register to the accumulator.
        
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.state.register_A = self.cpu.state.register_X
        self.cpu.state.flag_Z = bool(self.cpu.state.register_A == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_A & 0x80)
        return 0

    def TXS(self) -> int:
        """
        Handles the Transfer X to Stack Pointer (TXS) instruction.

        This instruction transfers the value in the X register to the stack pointer.

        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.state.register_SP = self.cpu.state.register_X
        return 0

    def TYA(self) -> int:
        """
        Handles the Transfer Y to Accumulator (TYA) instruction.
    
        This instruction transfers the value in the Y register to the accumulator.
    
        :return: The number of cycles taken to execute the instruction.
        """
        self.cpu.state.register_A = self.cpu.state.register_Y
        self.cpu.state.flag_Z = bool(self.cpu.state.register_A == 0x00)
        self.cpu.state.flag_N = bool(self.cpu.state.register_A & 0x80)
        return 0
    
    def XXX(self) -> int:
        """
        Handles invalid instructions.

        :return: The number of cycles taken to execute the instruction.
        """
        return 0
