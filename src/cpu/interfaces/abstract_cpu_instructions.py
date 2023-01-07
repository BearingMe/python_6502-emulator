from abc import ABC, abstractmethod

class AbstractCpuInstructions(ABC):
    @abstractmethod
    def irq(self) -> None:
        pass

    @abstractmethod
    def nmi(self) -> None:
        pass

    @abstractmethod
    def ADC(self) -> int:
        pass

    @abstractmethod
    def AND(self) -> int:
        pass

    @abstractmethod
    def ASL(self) -> int:
        pass

    @abstractmethod
    def BCC(self) -> int:
        pass

    @abstractmethod
    def BCS(self) -> int:
        pass

    @abstractmethod
    def BEQ(self) -> int:
        pass

    @abstractmethod
    def BIT(self) -> int:
        pass

    @abstractmethod
    def BMI(self) -> int:
        pass

    @abstractmethod
    def BNE(self) -> int:
        pass

    @abstractmethod
    def BPL(self) -> int:
        pass

    @abstractmethod
    def BRK(self) -> int:
        pass

    @abstractmethod
    def BVC(self) -> int:
        pass

    @abstractmethod
    def BVS(self) -> int:
        pass

    @abstractmethod
    def CLC(self) -> int:
        pass

    @abstractmethod
    def CLD(self) -> int:
        pass

    @abstractmethod
    def CLI(self) -> int:
        pass

    @abstractmethod
    def CLV(self) -> int:
        pass

    @abstractmethod
    def CMP(self) -> int:
        pass

    @abstractmethod
    def CPX(self) -> int:
        pass

    @abstractmethod
    def CPY(self) -> int:
        pass

    @abstractmethod
    def DEC(self) -> int:
        pass

    @abstractmethod
    def DEX(self) -> int:
        pass

    @abstractmethod
    def DEY(self) -> int:
        pass
    
    @abstractmethod
    def EOR(self) -> int:
        pass

    @abstractmethod
    def INC(self) -> int:
        pass

    @abstractmethod
    def INX(self) -> int:
        pass

    @abstractmethod
    def INY(self) -> int:
        pass

    @abstractmethod
    def JMP(self) -> int:
        pass

    @abstractmethod
    def JSR(self) -> int:
        pass

    @abstractmethod
    def LDA(self) -> int:
        pass

    @abstractmethod
    def LDX(self) -> int:
        pass

    @abstractmethod
    def LDY(self) -> int:
        pass

    @abstractmethod
    def LSR(self) -> int:
        pass

    @abstractmethod
    def NOP(self) -> int:
        pass

    @abstractmethod
    def ORA(self) -> int:
        pass

    @abstractmethod
    def PHA(self) -> int:
        pass

    @abstractmethod
    def PHP(self) -> int:
        pass

    @abstractmethod
    def PLA(self) -> int:
        pass

    @abstractmethod
    def PLP(self) -> int:
        pass

    @abstractmethod
    def ROL(self) -> int:
        pass

    @abstractmethod
    def ROR(self) -> int:
        pass

    @abstractmethod
    def RTI(self) -> int:
        pass

    @abstractmethod
    def RTS(self) -> int:
        pass

    @abstractmethod
    def SBC(self) -> int:
        pass

    @abstractmethod
    def SEC(self) -> int:
        pass

    @abstractmethod
    def SED(self) -> int:
        pass

    @abstractmethod
    def SEI(self) -> int:
        pass

    @abstractmethod
    def STA(self) -> int:
        pass

    @abstractmethod
    def STA(self) -> int:
        pass

    @abstractmethod
    def STX(self) -> int:
        pass

    @abstractmethod
    def STY(self) -> int:
        pass

    @abstractmethod
    def TAX(self) -> int:
        pass

    @abstractmethod
    def TAY(self) -> int:
        pass

    @abstractmethod
    def TSX(self) -> int:
        pass

    @abstractmethod
    def TXA(self) -> int:
        pass

    @abstractmethod
    def TXS(self) -> int:
        pass

    @abstractmethod
    def TYA(self) -> int:
        pass
