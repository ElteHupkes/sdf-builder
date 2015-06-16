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
        mass = 250
        box = Box(x, y, z, mass=mass)
        inert = box.get_inertial()

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
        simple_box = Box(4, 8, 12, mass=total_mass)
        i1 = simple_box.get_inertial()

        # # First the most trivial case - two same size
        # # boxes with half the mass.
        compound = CompoundGeometry()
        sub1 = Box(4, 8, 12, mass=0.5 * total_mass)
        sub2 = Box(4, 8, 12, mass=0.5 * total_mass)
        compound.add_geometry(sub1)
        compound.add_geometry(sub2)
        i2 = compound.get_inertial()
        self.assertEqualTensors(i1, i2)

        # Next, we try to boxes positioned on top
        # of each other, with the mass divided over them.
        compound = CompoundGeometry()
        sub1 = Box(4, 8, 5, mass=total_mass * 5.0 / 12)
        sub2 = Box(4, 8, 7, mass=total_mass * 7.0 / 12)
        sub1.translate(Vector3(0, 0, 2.5))
        sub2.translate(Vector3(0, 0, -3.5))
        compound.add_geometry(sub1)
        compound.add_geometry(sub2)
        i2 = compound.get_inertial()
        self.assertEqualTensors(i1, i2)

        # Finally, something involving rotation,
        # and different sizes.
        compound = CompoundGeometry()

        # We'll divide the z-axis
        frac = total_mass / 12.0
        total_up = 4 * frac
        frac_up = total_up / 8.0
        total_down = 8 * frac
        frac_down = total_down / 8.0

        # Rotate such that the x axis becomes the z axis (and
        # vice versa). Then divide that axis into 4/12 above,
        # 8/12 below. Above then into 3/5, below into 6/2 at
        # the y-axis.
        sub1 = Box(4, 3, 4, mass=3 * frac_up)
        sub2 = Box(4, 5, 4, mass=5 * frac_up)
        sub1.rotate_around(Vector3(0, 1, 0), -0.5 * math.pi)
        sub2.rotate_around(Vector3(0, 1, 0), -0.5 * math.pi)
        sub1.translate(Vector3(0, -1.5, 2))
        sub2.translate(Vector3(0, 2.5, 2))
        compound.add_geometry(sub1)
        compound.add_geometry(sub2)

        sub3 = Box(4, 8, 8, mass=total_down)
        sub3.translate(Vector3(0, 0, -4))
        compound.add_geometry(sub3)

        # sub3 = Box(8, 6, 4, mass=6 * frac_down)
        # sub4 = Box(8, 2, 4, mass=2 * frac_down)
        # sub3.rotate_around(Vector3(0, 1, 0), -0.5 * math.pi)
        # sub4.rotate_around(Vector3(0, 1, 0), -0.5 * math.pi)
        # sub3.translate(Vector3(0, -3, -4))
        # sub4.translate(Vector3(0, 1, -4))
        # compound.add_geometry(sub3)
        # compound.add_geometry(sub4)

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
