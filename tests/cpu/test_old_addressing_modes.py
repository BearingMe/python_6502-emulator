import unittest

from src.cpu.old_addressing_modes import AddressingModes

class TestCpuFlags(unittest.TestCase):
    def setUp(self):
        """
        Set up the test case by creating a new AddressinMode object.
        """
        self.addressing_modes = AddressingModes()

    def test_ABS(self):
        # Set up some test values
        self.addressing_modes.pc = 0x0001
        self.addressing_modes.read = lambda address: 0x01 if address == 0x0001 else 0x02

        # Call the ABS method and check the result
        result = self.addressing_modes.ABS()
        self.assertEqual(result, 0)
        self.assertEqual(self.addressing_modes.addr_abs, 0x0201)
        self.assertEqual(self.addressing_modes.pc, 0x0003)

    def test_ABX_no_boundary_cross(self):
        # Set up some test values
        self.addressing_modes.x = 0x01
        self.addressing_modes.pc = 0x0001
        self.addressing_modes.read = lambda address: 0x01 if address == 0x0001 else 0x02

        # Call the ABX method and check the result
        result = self.addressing_modes.ABX()
        self.assertEqual(result, 0)
        self.assertEqual(self.addressing_modes.addr_abs, 0x0202)
        self.assertEqual(self.addressing_modes.pc, 0x0003)

    def test_ABX_boundary_cross(self):
        # Set up some test values
        self.addressing_modes.x = 0x01
        self.addressing_modes.pc = 0x0001
        self.addressing_modes.read = lambda address: 0xFF if address == 0x0001 else 0x02

        # Call the ABX method and check the result
        result = self.addressing_modes.ABX()
        self.assertEqual(result, 1)
        self.assertEqual(self.addressing_modes.addr_abs, 0x0300)
        self.assertEqual(self.addressing_modes.pc, 0x0003)

    def test_ABY_no_boundary_cross(self):
        # Set up some test values
        self.addressing_modes.y = 0x01
        self.addressing_modes.pc = 0x0001
        self.addressing_modes.read = lambda address: 0x01 if address == 0x0001 else 0x02

        # Call the ABY method and check the result
        result = self.addressing_modes.ABY()
        self.assertEqual(result, 0)
        self.assertEqual(self.addressing_modes.addr_abs, 0x0202)
        self.assertEqual(self.addressing_modes.pc, 0x0003)

    def test_ABY_boundary_cross(self):
        # Set up some test values
        self.addressing_modes.y = 0x01
        self.addressing_modes.pc = 0x0001
        self.addressing_modes.read = lambda address: 0xFF if address == 0x0001 else 0x02

        # Call the ABY method and check the result
        result = self.addressing_modes.ABY()
        self.assertEqual(result, 1)
        self.assertEqual(self.addressing_modes.addr_abs, 0x0300)
        self.assertEqual(self.addressing_modes.pc, 0x0003)

    def test_IMM(self):
        # Set up some test values
        self.addressing_modes.pc = 0x0001

        # Call the IMM method and check the result
        result = self.addressing_modes.IMM()
        self.assertEqual(result, 0)
        self.assertEqual(self.addressing_modes.addr_abs, 0x0001)
        self.assertEqual(self.addressing_modes.pc, 0x0002)

    def test_IMP(self):
        # Set up some test values
        self.addressing_modes.a = 0x01

        # Call the IMP method and check the result
        result = self.addressing_modes.IMP()
        self.assertEqual(result, 0)
        self.assertEqual(self.addressing_modes.fetched, 0x01)

    def test_IND(self):
        # Set up some test values
        self.addressing_modes.pc = 0x0001
        self.addressing_modes.read = lambda address: 0xFF if address == 0x0001 else 0x02

        # Call the IND method and check the result
        result = self.addressing_modes.IND()
        self.assertEqual(result, 0)
        self.assertEqual(self.addressing_modes.addr_abs, 0x0202)
        self.assertEqual(self.addressing_modes.pc, 0x0003)

    def test_IZX(self):
        # Set up some test values
        self.addressing_modes.x = 0x01
        self.addressing_modes.pc = 0x0001
        self.addressing_modes.read = lambda address: 0x01 if address == 0x0001 else 0x02

        # Call the IZX method and check the result
        result = self.addressing_modes.IZX()
        self.assertEqual(result, 0)
        self.assertEqual(self.addressing_modes.addr_abs, 0x0202)
        self.assertEqual(self.addressing_modes.pc, 0x0002)

    def test_IZY_no_boundary_cross(self):
        # Set up some test values
        self.addressing_modes.y = 0x01
        self.addressing_modes.pc = 0x0001
        self.addressing_modes.read = lambda address: 0x01 if address == 0x0001 else 0x02

        # Call the IZY method and check the result
        result = self.addressing_modes.IZY()
        self.assertEqual(result, 0)
        self.assertEqual(self.addressing_modes.addr_abs, 0x0202)
        self.assertEqual(self.addressing_modes.pc, 0x0002)

    def test_IZY_boundary_cross(self):
        # Set up some test values
        self.addressing_modes.y = 0xFF
        self.addressing_modes.pc = 0x0001
        self.addressing_modes.read = lambda address: 0xFF if address == 0x0001 else 0x02

        # Call the IZY method and check the result
        result = self.addressing_modes.IZY()
        self.assertEqual(result, 1)
        self.assertEqual(self.addressing_modes.addr_abs, 0x0301)
        self.assertEqual(self.addressing_modes.pc, 0x0002)

    def test_REL(self):
    # Set up some test values
        self.addressing_modes.pc = 0x0001
        self.addressing_modes.read = lambda address: 0x80 if address == 0x0001 else 0x00

        # Call the REL method and check the result
        result = self.addressing_modes.REL()
        self.assertEqual(result, 0)
        self.assertEqual(self.addressing_modes.addr_rel, 0xFF80)
        self.assertEqual(self.addressing_modes.pc, 0x0002)

    def test_ZP0(self):
        # Set up some test values
        self.addressing_modes.pc = 0x0001
        self.addressing_modes.read = lambda address: 0x01

        # Call the ZP0 method and check the result
        result = self.addressing_modes.ZP0()
        self.assertEqual(result, 0)
        self.assertEqual(self.addressing_modes.addr_abs, 0x0001)
        self.assertEqual(self.addressing_modes.pc, 0x0002)

    def test_ZPX(self):
        # Set up some test values
        self.addressing_modes.x = 0x01
        self.addressing_modes.pc = 0x0001
        self.addressing_modes.read = lambda address: 0x01

        # Call the ZPX method and check the result
        result = self.addressing_modes.ZPX()
        self.assertEqual(result, 0)
        self.assertEqual(self.addressing_modes.addr_abs, 0x0002)
        self.assertEqual(self.addressing_modes.pc, 0x0002)

    def test_ZPY(self):
        # Set up some test values
        self.addressing_modes.y = 0x01
        self.addressing_modes.pc = 0x0001
        self.addressing_modes.read = lambda address: 0x01

        # Call the ZPY method and check the result
        result = self.addressing_modes.ZPY()
        self.assertEqual(result, 0)
        self.assertEqual(self.addressing_modes.addr_abs, 0x0002)
        self.assertEqual(self.addressing_modes.pc, 0x0002)