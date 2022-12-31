import unittest

from src.cpu.instructions import Instructions

class TestInstructions(unittest.TestCase):
    def setUp(self):
        self.instructions = Instructions()

    def test_instruction_set(self):
        # Test if instruction_set is provided
        self.assertIsNotNone(self.instructions.lookup)


    def test_fetch(self):
        # Test the case where the addrmode is not IMP
        self.instructions.opcode = "BRK"
        self.instructions.addr_abs = 0x1234
        self.instructions.read = lambda x: 0xAB
        self.assertEqual(self.instructions.fetch(), 0xAB)

        # Test the case where the addrmode is IMP
        self.instructions.opcode = "RTI"
        self.assertEqual(self.instructions.fetch(), 0)
