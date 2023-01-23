from unittest import TestCase
from unittest.mock import Mock

from ..addressing_modes import AddressingModes

class TestAddressingModes(TestCase):
    def setUp(self):
        """
        Set up the test case by creating a new AddressingMode object.
        """
        self.cpu = Mock()
        
        # Set up some test values
        self.cpu.bus.read = lambda address: 0x01 if address == 0x0001 else 0x02
        self.cpu.state.addr_abs = 0x0000
        self.cpu.state.addr_rel = 0x0000
        self.cpu.state.fetched = 0x00
        self.cpu.state.register_PC = 0x0001
        self.cpu.state.register_A = 0x01
        self.cpu.state.register_X = 0x0001
        self.cpu.state.register_Y = 0x0001

        self.addressing_modes = AddressingModes(self.cpu)

    def test_read_byte(self):
        # Call the _read_byte method and check the result
        result = self.addressing_modes._read_byte(0x0001)
        
        self.assertEqual(result, 0x01)
        self.assertEqual(self.cpu.state.register_PC, 0x0002)

    def test_read_word(self):
        # Call the _read_word method and check the result
        result = self.addressing_modes._read_word(0x0001)

        self.assertEqual(result, (0x01, 0x02))
        self.assertEqual(self.cpu.state.register_PC, 0x0003)

    def test_check_page_boundary(self):
        # Call the _check_page_boundary method and check the result
        result = self.addressing_modes._check_page_boundary(0x0000, 0x0000)
        self.assertEqual(result, False)

        result = self.addressing_modes._check_page_boundary(0x0100, 0x0000)
        self.assertEqual(result, True)

    def test_ABS(self):
        # Call the ABS method and check the result
        result = self.addressing_modes.ABS()
        
        self.assertEqual(result, 0)
        self.assertEqual(self.addressing_modes.cpu.state.addr_abs, 0x0201)
        self.assertEqual(self.addressing_modes.cpu.state.register_PC, 0x0003)

    def test_ABX_no_boundary_cross(self):
        # Call the ABX method and check the result
        result = self.addressing_modes.ABX()

        self.assertEqual(result, 0)
        self.assertEqual(self.addressing_modes.cpu.state.addr_abs, 0x0202)
        self.assertEqual(self.addressing_modes.cpu.state.register_PC, 0x0003)
        
    def test_ABX_boundary_cross(self):
        # Set up some test values
        self.cpu.bus.read = lambda address: 0xFF if address == 0x0001 else 0x02

        # Call the ABX method and check the result
        result = self.addressing_modes.ABX()
        self.assertEqual(result, 1)
        self.assertEqual(self.addressing_modes.cpu.state.addr_abs, 0x0300)
        self.assertEqual(self.addressing_modes.cpu.state.register_PC, 0x0003)
    
    def test_ABY_no_boundary_cross(self):
        # Call the ABY method and check the result
        result = self.addressing_modes.ABX()

        self.assertEqual(result, 0)
        self.assertEqual(self.addressing_modes.cpu.state.addr_abs, 0x202)
        self.assertEqual(self.addressing_modes.cpu.state.register_PC, 0x0003)

    def test_ABY_boundary_cross(self):
        # Set up some test values
        self.cpu.bus.read = lambda address: 0xFF if address == 0x0001 else 0x02

        # Call the ABY method and check the result
        result = self.addressing_modes.ABY()

        self.assertEqual(result, 1)
        self.assertEqual(self.cpu.state.addr_abs, 0x0300)
        self.assertEqual(self.cpu.state.register_PC, 0x0003)

    def test_IMM(self):
        # Call the IMM method and check the result
        result = self.addressing_modes.IMM()

        self.assertEqual(result, 0)
        self.assertEqual(self.cpu.state.addr_abs, 0x0001)
        self.assertEqual(self.cpu.state.register_PC, 0x0002)

    def test_IMP(self):
        # Call the IMP method and check the result
        result = self.addressing_modes.IMP()

        self.assertEqual(result, 0)
        self.assertEqual(self.cpu.state.fetched, 0x01)
        self.assertEqual(self.cpu.state.register_PC, 0x0001)

    # TODO: also test the case where the address is on a page boundary
    def test_IND(self):
        self.cpu.bus.read = lambda address: [0x00, 0x03, 0x00, 0x10, 0x00][address]

        # Call the IND method and check the result
        result = self.addressing_modes.IND()
        self.assertEqual(result, 0)
        self.assertEqual(self.cpu.state.addr_abs, 0x0010)
        self.assertEqual(self.cpu.state.register_PC, 0x0003)

    def test_IZX(self):
        # Set up some test values
        self.cpu.bus.read = lambda address: [0x00, 0x03, 0x00, 0x00, 0x01, 0x00][address]

        # Call the IZX method and check the result
        result = self.addressing_modes.IZX()
        
        self.assertEqual(result, 0)
        self.assertEqual(self.cpu.state.addr_abs, 0x0001)
        self.assertEqual(self.cpu.state.register_PC, 0x0002)

    def test_IZY(self):
        # Set up some test values
        self.cpu.bus.read = lambda address: [0x00, 0x03, 0x00, 0x10, 0x00][address]

        # Call the IZY method and check the result
        result = self.addressing_modes.IZY()

        self.assertEqual(result, 0)
        self.assertEqual(self.cpu.state.addr_abs, 0x0011)
        self.assertEqual(self.cpu.state.register_PC, 0x0002)


    def test_REL(self):
        # Set up some test values
        self.cpu.bus.read = lambda address: 0x80 if address == 0x0001 else 0x00
        
        # Call the REL method and check the result
        result = self.addressing_modes.REL()
        
        self.assertEqual(result, 0)
        self.assertEqual(self.cpu.state.addr_rel, 0xFF80)
        self.assertEqual(self.cpu.state.register_PC, 0x0002)

    def test_ZP0(self):
        # Call the ZP0 method and check the result
        result = self.addressing_modes.ZP0()

        self.assertEqual(result, 0)
        self.assertEqual(self.cpu.state.addr_abs, 0x0001)
        self.assertEqual(self.cpu.state.register_PC, 0x0002)

    def test_ZPX(self):
        # Call the ZPX method and check the result
        result = self.addressing_modes.ZPX()

        self.assertEqual(result, 0)
        self.assertEqual(self.cpu.state.addr_abs, 0x0002)
        self.assertEqual(self.cpu.state.register_PC, 0x0002)

    def test_ZPY(self):
        # Call the ZPY method and check the result
        result = self.addressing_modes.ZPY()

        self.assertEqual(result, 0)
        self.assertEqual(self.cpu.state.addr_abs, 0x0002)
        self.assertEqual(self.cpu.state.register_PC, 0x0002)
