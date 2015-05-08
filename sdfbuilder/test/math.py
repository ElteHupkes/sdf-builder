"""
Math tests, this clearly needs more stuff.
"""
import unittest
from sdfbuilder.math import Quaternion


class TestMath(unittest.TestCase):
    """
    Tests the math components
    """
    def test_euler_angles(self):
        """

        :return:
        """
        q = Quaternion(-0.5, 0.5, 0.5, 0.5)
        print(q.get_rpy())


if __name__ == '__main__':
    unittest.main()