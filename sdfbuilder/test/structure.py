from __future__ import absolute_import
import unittest
import math
from sdfbuilder.math import Vector3
from sdfbuilder.structure.geometries import Box, CompoundGeometry


class TestGeometry(unittest.TestCase):
    """
    Tests mostly the compound geometry
    """
    def test_box_inertia(self):
        """
        """
        x, y, z = 10, 20, 30
        box = Box(x, y, z)
        mass = 250
        inert = box.get_inertial(mass)

        self.assertAlmostEquals(inert.ixx, mass * (y**2 + z**2) / 12.0)
        self.assertAlmostEquals(inert.iyy, mass * (x**2 + z**2) / 12.0)
        self.assertAlmostEquals(inert.izz, mass * (x**2 + y**2) / 12.0)
        self.assertAlmostEquals(inert.ixy, 0)
        self.assertAlmostEquals(inert.ixz, 0)
        self.assertAlmostEquals(inert.iyz, 0)

    def test_compound_inertia(self):
        """
        Performs a simple compound geometry inertia check
        by comparing two aligned boxes with one big box,
        with the same mass distribution and total mass.
        """
        total_mass = 100
        simple_box = Box(4, 8, 12)
        i1 = simple_box.get_inertial(total_mass)

        # # First the most trivial case - two same size
        # # boxes with half the mass.
        compound = CompoundGeometry()
        sub1 = Box(4, 8, 12)
        sub2 = Box(4, 8, 12)
        compound.add_geometry(sub1, 0.5 * total_mass)
        compound.add_geometry(sub2, 0.5 * total_mass)
        i2 = compound.get_inertial()
        self.assertEqualTensors(i1, i2)

        # Next, we try to boxes positioned on top
        # of each other, with the mass divided over them.
        compound = CompoundGeometry()
        sub1 = Box(4, 8, 5)
        sub2 = Box(4, 8, 7)
        sub1.translate(Vector3(0, 0, 2.5))
        sub2.translate(Vector3(0, 0, -3.5))
        compound.add_geometry(sub1, total_mass * 5.0 / 12)
        compound.add_geometry(sub2, total_mass * 7.0 / 12)
        i2 = compound.get_inertial()
        self.assertEqualTensors(i1, i2)

        # Finally, something involving rotation,
        # and different sizes.
        compound = CompoundGeometry()
        sub1 = Box(4, 8, 4)
        sub2 = Box(8, 8, 4)
        compound.add_geometry(sub1, 4.0 * total_mass / 12)
        compound.add_geometry(sub2, 8.0 * total_mass / 12)

        # Rotate the boxes around the y-axis so the x-axis
        # becomes the z axis.
        sub1.rotate_around(Vector3(0, 1, 0), -0.5 * math.pi)
        sub2.rotate_around(Vector3(0, 1, 0), -0.5 * math.pi)

        # Translate such that the subs connect (but not overlap)
        # at the z axis as before.
        sub1.translate(Vector3(0, 0, -2))
        sub2.translate(Vector3(0, 0, 4))

        i2 = compound.get_inertial()
        self.assertEqualTensors(i1, i2)

    def assertEqualTensors(self, i1, i2):
        self.assertAlmostEquals(i1.ixx, i2.ixx)
        self.assertAlmostEquals(i1.ixy, i2.ixy)
        self.assertAlmostEquals(i1.ixz, i2.ixz)
        self.assertAlmostEquals(i1.iyy, i2.iyy)
        self.assertAlmostEquals(i1.iyy, i2.iyy)

if __name__ == '__main__':
    unittest.main()
