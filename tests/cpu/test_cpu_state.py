import unittest

from src.cpu.cpu_state import CpuState

class TestCpuState(unittest.TestCase):
    def setUp(self):
        """
        Set up the test case by creating a new CpuState object.
        """
        self.cpu_state = CpuState()

    def test_getters(self):
        """
        Test the getters for the registers.
        """
        self.assertEqual(self.cpu_state.a, 0x00)
        self.assertEqual(self.cpu_state.x, 0x00)
        self.assertEqual(self.cpu_state.y, 0x00)
        self.assertEqual(self.cpu_state.sp, 0x00)
        self.assertEqual(self.cpu_state.status, 0x00)
        self.assertEqual(self.cpu_state.pc, 0x0000)

    def test_setters(self):
        """
        Test the setters for the registers.
        """
        self.cpu_state.a = 0x01
        self.cpu_state.x = 0x02
        self.cpu_state.y = 0x03
        self.cpu_state.sp = 0x04
        self.cpu_state.status = 0x05
        self.cpu_state.pc = 0x1234

        self.assertEqual(self.cpu_state.a, 0x01)
        self.assertEqual(self.cpu_state.x, 0x02)
        self.assertEqual(self.cpu_state.y, 0x03)
        self.assertEqual(self.cpu_state.sp, 0x04)
        self.assertEqual(self.cpu_state.status, 0x05)
        self.assertEqual(self.cpu_state.pc, 0x1234)

    def test_setters_invalid_value(self):
        """
        Test the setters for the registers with invalid values.
        """
        with self.assertRaises(ValueError):
            self.cpu_state.a = 0x100
        with self.assertRaises(ValueError):
            self.cpu_state.x = 0x100
        with self.assertRaises(ValueError):
            self.cpu_state.y = 0x100
        with self.assertRaises(ValueError):
            self.cpu_state.sp = 0x100
        with self.assertRaises(ValueError):
            self.cpu_state.status = 0x100
        with self.assertRaises(ValueError):
            self.cpu_state.pc = 0x10000