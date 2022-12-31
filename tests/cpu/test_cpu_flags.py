import unittest

from src.cpu.cpu_flags import CpuFlags

class TestCpuFlags(unittest.TestCase):
    def setUp(self):
        """
        Set up the test case by creating a new CpuFlags object.
        """
        self.flags = CpuFlags()

    def test_getters(self):
        """
        Test the getters to ensure that they return the correct value for each flag.
        """
        # Assert that the C, I, and B flags are initially False
        self.assertEqual(self.flags.C, False)
        self.assertEqual(self.flags.I, False)
        self.assertEqual(self.flags.B, False)

    def test_setters(self):
        """
        Test the setters to ensure that they set the value of the specified flag correctly.
        """
        # Assert that the C and N flags can be set to True
        self.assertEqual(self.flags.C, False)
        self.assertEqual(self.flags.N, False)
        self.flags.C = True
        self.flags.N = True
        self.assertEqual(self.flags.C, True)
        self.assertEqual(self.flags.N, True)

        # Assert that the C and Z flags can be set to False
        self.flags.C = False
        self.flags.Z = False
        self.assertEqual(self.flags.C, False)
        self.assertEqual(self.flags.Z, False)

    def test_setters_with_invalid_values(self):
        """
        Test the setters to ensure that they raise an exception when given an invalid value.
        """
        # Assert that the setters raise an exception when given an invalid value
        with self.assertRaises(TypeError):
            self.flags.C = "True"
        with self.assertRaises(TypeError):
            self.flags.N = "False"
        with self.assertRaises(ValueError):
            self.flags.Z = 2
    
    def test_byte_getter(self):
        """
        Test the byte getter to ensure that it returns the correct byte representation of the flags.
        """
        # Assert that the initial value of the flags is 0b00000000
        self.assertEqual(self.flags.byte, 0b00000000)

        # Set the C flag to True and assert that the value of the flags is now 0b00000001
        self.flags.C = True
        self.assertEqual(self.flags.byte, 0b00000001)

        # Set the D flag to True and assert that the value of the flags is now 0b00001001
        self.flags.D = True
        self.assertEqual(self.flags.byte, 0b00001001)

    def test_byte_setter(self):
        """
        Test the byte setter to ensure that it sets the value of the flags correctly.
        """
        # Set the byte to 0b00000001 and assert that the C flag is now True
        self.flags.byte = 0b10000000
        self.assertEqual(self.flags.N, True)

        # Set the byte to 0b00001001 and assert that the C and D flags are now True
        self.flags.byte = 0b00001001
        self.assertEqual(self.flags.C, True)
        self.assertEqual(self.flags.D, True)

    def test_byte_setter_with_invalid_values(self):
        """
        Test the byte setter to ensure that it raises an exception when given an invalid value.
        """
        # Assert that the byte setter raises an exception when given an invalid value
        with self.assertRaises(TypeError):
            self.flags.byte = "0b00000001"
        with self.assertRaises(ValueError):
            self.flags.byte = 0b100000010
