from cpu import cpu, cpu_flags, cpu_state

cpu_state = cpu_state.CpuState()
cpu_flags = cpu_flags.CpuFlags()

with open("test.bin", "rb") as f:
    binary = list(f.read())


cpu = cpu.Cpu(cpu_state=cpu_state, cpu_flags=cpu_flags)

print([chr(c) for c in cpu.execute(binary)[:11]])