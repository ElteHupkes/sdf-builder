"""
Tests a relatively complex align feature
"""
import unittest
from sdfbuilder.link import Link
from sdfbuilder.posable import PosableGroup
from sdfbuilder.math import Vector3
from math import pi, sqrt


class TestPosable(unittest.TestCase):
    """
    Tests various aspects of the Posable class, such as
    alignment and rotation.
    """
    def test_direction_conversion(self):
        """
        Tests converting vectors between direction frames.
        :return:
        """
        link = Link("my_link")
        point = Vector3(0, 0, 1)

        # At this point, it should be the same in the
        # parent direction
        x, y, z = link.to_parent_direction(point)
        self.assertAlmostEqual(x, point.x)
        self.assertAlmostEqual(y, point.y)
        self.assertAlmostEqual(z, point.z)

        # Now rotate the link 90 degrees over (1, 1, 0),
        # this should cause the local vector (0, 1, 1)
        # to land at 0.5 * [sqrt(2), -sqrt(2), 0]
        link.rotate_around(Vector3(1, 1, 0), 0.5 * pi, relative_to_child=False)
        hs2 = 0.5 * sqrt(2)
        x, y, z = link.to_parent_direction(point)
        self.assertAlmostEqual(x, hs2)
        self.assertAlmostEqual(y, -hs2)
        self.assertAlmostEqual(z, 0)

    def test_complex_align(self):
        """
        Create a structure with some complicated rotation /
        align transformations and tests the resulting positions.
        :return:
        """
        link = Link("my_link")

        minibox = Link("my_minibox")

        # Link one is a vertical box
        link.make_box(1.0, 2, 2, 4)

        # Minibox is... well, a mini box
        minibox.make_box(0.1, 0.2, 0.2, 0.2)

        minibox.align(
            # Bottom left corner of minibox
            Vector3(-0.1, -0.1, -0.1),

            # Normal vector
            Vector3(-0.1, -0.1, -0.1),

            # Tangent vector
            Vector3(-0.1, -0.1, 0.2),

            # Top left of link (note, we're positioning
            # the center of minibox, so subtract half its size)
            Vector3(-1, -1, 2),

            # Normal vector
            Vector3(0, 0, 1),

            # Tangent vector
            Vector3(1, 0, 0),

            # Link to align with
            link,

            # All vectors relative to child frame
            relative_to_child=True
        )

        # Add link and minibox to a posable group so we can move
        # them around together.
        group = PosableGroup()
        group.add_element(link)
        group.add_element(minibox)

        # Move and rotate the group to confuse the mechanism
        # (this should just be undone at the align later)
        group.rotate_around(Vector3(1, 1, 0), 0.1 * pi)
        group.translate(Vector3(0.6, 0.7, 0.8))

        # Create a new, larger box called link 2
        link2 = Link("my_link_2")
        link2.make_box(2.0, 4, 3, 3)

        # Translate and rotate just to add some extra complexity
        link2.translate(Vector3(0.5, 0.5, 2))
        link2.rotate_around(Vector3(1, 1, 1), 0.5 * pi)

        # Now align the group so its right center lands at
        # the top center of link 2
        group.align(
            # Center of the right face of box 1
            Vector3(1, 0, 0),

            # Vector normal to box 2 right face
            Vector3(1, 0, 0),

            # Vector normal to box 2 top face should align with...(*)
            Vector3(0, 0, 1),

            # Center of the top face of box 2
            Vector3(0, 0, 1.5),

            # Vector normal to box 2 top face
            Vector3(0, 0, 1),

            # (*)...vector normal to box 2 right face
            Vector3(1, 0, 0),

            # the link to align with
            link2
        )

        # Now, the asserts. These positions have been verified through
        # visual inspection and then copied from the SDF - we might thus
        # say this functions as a regression test.

        # First, the position of the first link.
        roll, pitch, yaw = link.pose.euler_rotation()
        x, y, z = link.get_position()
        self.assertAlmostEqual(x, 2.776709, msg="Incorrect x position.")
        self.assertAlmostEqual(y, -0.1100423, msg="Incorrect y position.")
        self.assertAlmostEqual(z, 2.8333333, msg="Incorrect z position.")
        self.assertAlmostEqual(roll, 1.8325957145940461, msg="Incorrect roll.")
        self.assertAlmostEqual(pitch, 0.3398369, msg="Incorrect pitch.")
        self.assertAlmostEqual(yaw, 2.8797932657906435, msg="Incorrect yaw.")

        # Now, position of the minibox
        roll, pitch, yaw = minibox.pose.euler_rotation()
        x, y, z = minibox.get_position()
        self.assertAlmostEqual(x, 4.655811238272279, msg="Incorrect x position.")
        self.assertAlmostEqual(y, 1.291709623134523, msg="Incorrect y position.")
        self.assertAlmostEqual(z, 1.7256842193500852, msg="Incorrect z position.")
        self.assertAlmostEqual(roll, -2.1377528428632186, msg="Incorrect roll.")
        self.assertAlmostEqual(pitch, -0.6933926357494202, msg="Incorrect pitch.")
        self.assertAlmostEqual(yaw, 1.0364317772632718, msg="Incorrect yaw.")

        # Finally, position of link2
        roll, pitch, yaw = link2.pose.euler_rotation()
        x, y, z = link2.get_position()
        self.assertAlmostEqual(x, 0.5, msg="Incorrect x position.")
        self.assertAlmostEqual(y, 0.5, msg="Incorrect y position.")
        self.assertAlmostEqual(z, 2, msg="Incorrect z position.")
        self.assertAlmostEqual(roll, 1.2199169159226388, msg="Incorrect roll.")
        self.assertAlmostEqual(pitch, 0.24650585550379217, msg="Incorrect pitch.")
        self.assertAlmostEqual(yaw, 1.2199169159226388, msg="Incorrect yaw.")

if __name__ == '__main__':
    unittest.main()
