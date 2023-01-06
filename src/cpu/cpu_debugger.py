from .interfaces import AbstractCpu

from rich.console import Console

class CpuDebugger():
    def __init__(self, cpu: AbstractCpu):
        self.console = Console()
        self.cpu = cpu
        self.cprint = self.console.print

    def _log_flags(self) -> None:
        self.cprint("[red bold]>[/red bold]", end=" ")

        print(
            f"N: 0b{int(self.cpu.state.flag_N)}, " +
            f"V: 0b{int(self.cpu.state.flag_V)}, " +
            f"U: 0b{int(self.cpu.state.flag_U)}, " +
            f"B: 0b{int(self.cpu.state.flag_B)}, " +
            f"D: 0b{int(self.cpu.state.flag_D)}, " +
            f"I: 0b{int(self.cpu.state.flag_I)}, " + 
            f"Z: 0b{int(self.cpu.state.flag_Z)}, " +
            f"C: 0b{int(self.cpu.state.flag_C)}"
        )

    def _log_registers(self) -> None:
        self.cprint("[red bold]>[/red bold]", end=" ")

        print(
            "A:", f"0x{self.cpu.state.register_A:02x}, " +
            "X:", f"0x{self.cpu.state.register_X:02x}, " +
            "Y:", f"0x{self.cpu.state.register_Y:02x}, " +
            "SP:", f"0x{self.cpu.state.register_SP:02x}"
        )

    def _log_info(self) -> None:
        opcode_info = f"{self.cpu.state.opcode:02x}".upper()

        self.cprint(
            "[green]•[/green] Opcode:", f"[cyan]{opcode_info}[/cyan]", "\n" +
            "[green]•[/green] Addressing Mode:", f"[cyan]{self.cpu.state.current_addressing_mode}[/cyan]", "\n" +
            "[green]•[/green] Instruction:", f"[cyan]{self.cpu.state.current_instruction}[/cyan]"
        )

    def _log_program_counter(self) -> None:
        print(f"• PC: {self.cpu.state.register_PC - 1:04x}")

    def log(self) -> None:
        self._log_program_counter()
        self._log_info()
        self._log_registers()
        self._log_flags()

        print("\n")