import unittest

from src.cpu.old_cpu_flags import CpuFlags

class TestCpuFlags(unittest.TestCase):
    def setUp(self):
        """
        Set up the test case by creating a new CpuFlags object.
        """
        self.flags = CpuFlags()

    def test_reset_flags(self):
        """
        Test the reset_flags() method to ensure that it sets all flags to False.
        """
        # Set all flags to True
        self.flags._flag_data["C"] = True
        self.flags._flag_data["D"] = True
        self.flags._flag_data["N"] = True

        # Call the reset_flags() method and assert that it returns 0x00000000
        self.assertEqual(self.flags.reset_flags(), 0x00000000)

        # Assert that all flags are now False
        self.assertEqual(any(self.flags._flag_data.values()), False)

    def test_get_bit(self):
        """
        Test the get_bit() method to ensure that it returns the correct value for each flag.
        """
        # Assert that the C, I, and B flags are initially False
        self.assertEqual(self.flags.get_bit('C'), False)
        self.assertEqual(self.flags.get_bit('I'), False)
        self.assertEqual(self.flags.get_bit('B'), False)

    def test_set_bit(self):
        """
        Test the set_bit() method to ensure that it sets the value of the specified flag correctly.
        """
        # Assert that the C and N flags can be set to True
        self.assertEqual(self.flags.set_bit('C', True), True)
        self.assertEqual(self.flags.set_bit('N', True), True)

        # Assert that the C and Z flags can be set to False
        self.assertEqual(self.flags.set_bit('C', False), False)
        self.assertEqual(self.flags.set_bit('Z', False), False)


    def test_get_byte(self):
        """
        Test the get_byte() method to ensure that it returns the correct byte representation of the flags.
        """
        # Assert that the initial value of the flags is 0b00000000
        self.assertEqual(self.flags.get_byte(), 0b00000000)

        # Set the C flag to True and assert that the value of the flags is now 0b00000001
        self.flags.set_bit("C", True)
        self.assertEqual(self.flags.get_byte(), 0b00000001)

        # Set the D flag to True and assert that the value of the flags is now 0b00001001
        self.flags.set_bit("D", True)
        self.assertEqual(self.flags.get_byte(), 0b00001001)

        # Set the C flag to False and assert that the value of the flags is now 0b0001000
        self.flags.set_bit("C", False)
        self.assertEqual(self.flags.get_byte(), 0b0001000)
        
    def test_set_byte(self):
        """
        Test the set_byte() method to ensure that it sets the flags to the correct values.
        """
        # Set the flags to 0b11011100 and assert that the method returns that value
        self.assertEqual(self.flags.set_byte(0b11011100), 0b11011100)