import unittest

from src.cpu.cpu_state_handler import CpuStateHandler

class TestCpuFlags(unittest.TestCase):
    def setUp(self):
        """
        Set up the test case by creating a new CpuFlags object.
        """
        self.state_handler = CpuStateHandler()

        self.flag_c_shift = 0
        self.flag_z_shift = 1
        self.flag_i_shift = 2
        self.flag_d_shift = 3
        self.flag_b_shift = 4
        self.flag_u_shift = 5
        self.flag_v_shift = 6
        self.flag_n_shift = 7

    def test_flags_getters(self):
        """
        Test the getters to ensure that they return the correct value for each flag.
        """
        # Assert that the C, I, and B flags are initially zero
        self.assertEqual(self.state_handler.flag_C, 0)
        self.assertEqual(self.state_handler.flag_I, 0)
        self.assertEqual(self.state_handler.flag_B, 0)

    def test_flags_setters(self):
        """
        Test the setters to ensure that they set the value of the specified flag correctly.
        """
        # Assert that the C and N flags can be set to zero
        self.assertEqual(self.state_handler.flag_C, 0)
        self.assertEqual(self.state_handler.flag_N, 0)

        # Set the C and N flags to 1
        self.state_handler.flag_C = 1 << self.flag_c_shift
        self.state_handler.flag_N = 1 << self.flag_n_shift

        self.assertEqual(self.state_handler.flag_C, 1 << self.flag_c_shift)
        self.assertEqual(self.state_handler.flag_N, 1 << self.flag_n_shift)

        # Assert that the C and Z flags can be set to False
        self.state_handler.flag_C = 0
        self.state_handler.flag_Z = 0

        self.assertEqual(self.state_handler.flag_C, 0)
        self.assertEqual(self.state_handler.flag_Z, 0)

    def test_setters_with_invalid_values(self):
        """
        Test the setters to ensure that they raise an exception when given an invalid value.
        """
        # Assert that the setters raise an exception when given an invalid value
        with self.assertRaises(TypeError):
            self.state_handler.flag_C = "True"

        with self.assertRaises(TypeError):
            self.state_handler.flag_N = "False"

        with self.assertRaises(ValueError):
            self.state_handler.flag_Z = 1

    def test_helpers(self):
        # Set the helper address absolute value and check the result
        self.state_handler.addr_abs = 0xF0F0
        self.assertEqual(self.state_handler.addr_abs, 0xF0F0)

        # Set the helper address relative value and check the result
        self.state_handler.addr_rel = 0x0F0F
        self.assertEqual(self.state_handler.addr_rel, 0x0F0F)

        # Set the helper fetched value and check the result
        self.state_handler.fetched = 0xF0F0
        self.assertEqual(self.state_handler.fetched, 0xF0F0)

        # Set the helper cycles value and check the result
        self.state_handler.cycles = 2 ** 64 - 1
        self.assertEqual(self.state_handler.cycles, 2 ** 64 - 1)

        # Set the helper opcode value and check the result
        self.state_handler.opcode = 0xF0
        self.assertEqual(self.state_handler.opcode, 0xF0)

    def test_helpers_with_invalid_value(self):
        # Try to set an invalid helper address absolute value
        with self.assertRaises(ValueError):
            self.state_handler.addr_abs = 0xFFFF + 1

        with self.assertRaises(ValueError):
            self.state_handler.addr_abs = -327

        # Try to set an invalid helper address relative value
        with self.assertRaises(ValueError):
            self.state_handler.addr_rel = 0xFFFF + 1

        with self.assertRaises(ValueError):
            self.state_handler.addr_rel = -523

        # Try to set an invalid helper fetched value
        with self.assertRaises(ValueError):
            self.state_handler.fetched = 0xFFFF + 1

        with self.assertRaises(ValueError):
            self.state_handler.fetched = -879

        # Try to set an invalid helper cycles value
        with self.assertRaises(ValueError):
            self.state_handler.cycles = 0xFFFFFFFFFFFFFFFF + 1
        
        with self.assertRaises(ValueError):
            self.state_handler.cycles = -455

        # Try to set an invalid helper opcode value
        with self.assertRaises(ValueError):
            self.state_handler.opcode = 0xFF + 1

        with self.assertRaises(ValueError):
            self.state_handler.opcode = -654

    def test_register_getters(self):
        """
        Test the getters for the registers.
        """
        self.assertEqual(self.state_handler.register_A, 0x00)
        self.assertEqual(self.state_handler.register_X, 0x00)
        self.assertEqual(self.state_handler.register_Y, 0x00)
        self.assertEqual(self.state_handler.register_SP, 0x00)
        self.assertEqual(self.state_handler.register_SR, 0x00)
        self.assertEqual(self.state_handler.register_PC, 0x0000)

    def test_register_setters(self):
        """
        Test the setters for the registers.
        """
        self.state_handler.register_A = 0x01
        self.state_handler.register_X = 0x02
        self.state_handler.register_Y = 0x03
        self.state_handler.register_SP = 0x04
        self.state_handler.register_SR = 0x05
        self.state_handler.register_PC = 0x1234

        self.assertEqual(self.state_handler.register_A, 0x01)
        self.assertEqual(self.state_handler.register_X, 0x02)
        self.assertEqual(self.state_handler.register_Y, 0x03)
        self.assertEqual(self.state_handler.register_SP, 0x04)
        self.assertEqual(self.state_handler.register_SR, 0x05)
        self.assertEqual(self.state_handler.register_PC, 0x1234)

    def test_register_with_invalid_value(self):
        """
        Test the setters for the registers with invalid values.
        """
        with self.assertRaises(ValueError):
            self.state_handler.register_A = 0x100
        with self.assertRaises(ValueError):
            self.state_handler.register_X = 0x100
        with self.assertRaises(ValueError):
            self.state_handler.register_Y = 0x100
        with self.assertRaises(ValueError):
            self.state_handler.register_SP = 0x100
        with self.assertRaises(ValueError):
            self.state_handler.register_SR = 0x100
        with self.assertRaises(ValueError):
            self.state_handler.register_PC = 0x10000

    def test_check_value_size(self):
        # Test valid input
        self.state_handler._check_value_size(0)
        self.state_handler._check_value_size(255)
        self.state_handler._check_value_size(127, 7)
        self.state_handler._check_value_size(2**15-1, 16)
        

    def test_check_value_size_with_invalid_value(self):
        # Test invalid input
        with self.assertRaises(ValueError):
            self.state_handler._check_value_size(-1)

        with self.assertRaises(ValueError):
            self.state_handler._check_value_size(256)

        with self.assertRaises(ValueError):
            self.state_handler._check_value_size(128, 7)

        with self.assertRaises(ValueError):
            self.state_handler._check_value_size(2**16, 16)
