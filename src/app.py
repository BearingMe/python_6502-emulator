from cpu.cpu import Cpu


with open("test.bin", "rb") as f:
    binary = f.read()

    cpu = Cpu()
    cpu.run(binary)
