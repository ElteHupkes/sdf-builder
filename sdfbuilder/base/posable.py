from .element import Element
from ..math import Vector3, Quaternion, RotationMatrix
from ..math import vectors_orthogonal, vectors_parallel
from ..util import number_format as nf


class Pose(Element):
    """
    An SDF "pose" element, which is an x, y, z position
    plus a roll, pitch, yaw.
    """

    TAG_NAME = 'pose'

    def __init__(self, **kwargs):
        """
        """
        super().__init__(**kwargs)

        # Zero position and identity rotation
        self.position = Vector3()
        self.rotation = Quaternion()

    def euler_rotation(self):
        """
        Returns roll, pitch, yaw from the
        rotation Quaternion.
        """
        # Quaternion.get_euler() returns heading, attitude, bank,
        # which are rotations along the Y, Z and X attitude
        # respectively according to the pyeuclid docs. Gazebo
        # uses roll, pitch, yaw thus capture them in that order
        pitch, yaw, roll = self.rotation.get_euler()
        return roll, pitch, yaw

    def render_body(self):
        """

        :return:
        """
        body = super().render_body()
        roll, pitch, yaw = self.euler_rotation()
        x, y, z = self.position.x, self.position.y, self.position.z

        body += "%s %s %s %s %s %s" % (nf(x), nf(y), nf(z),
                                       nf(roll), nf(pitch), nf(yaw))

        return body


class Posable(Element):
    """
    Posable is a base class for elements with a name
    and a pose.
    """

    # Whether the pose for this element is in the parent frame
    # or not. A joint, for instance, has a pose, but it is
    # expressed in the child link frame. A parent posable
    # can use this property to decide not to affect this
    # element with transformations.
    PARENT_FRAME = True

    def __init__(self, name, pose=None, **kwargs):
        """
        :param name:
        :param kwargs:
        :return:
        """
        super().__init__(**kwargs)

        self.pose = Pose() if pose is None else pose
        self.name = name

    def set_rotation(self, rotation: Quaternion):
        """

        :param rotation: Rotation Quaternion
        :return:

        """
        self.pose.rotation = rotation

    def get_rotation(self):
        """
        Return the rotation quaternion of this posable's pose
        :return:
        """
        return self.pose.rotation

    def set_position(self, position: Vector3):
        """
        :param position:
        :return:
        """
        self.pose.position = position

    def get_position(self):
        """
        Return the 3-vector position of this posable's pose
        :return:
        """
        return self.pose.position

    def translate(self, translation: Vector3):
        """
        :param translation:
        :return:
        """
        self.set_position(self.get_position() + translation)

    def rotate(self, rotation: Quaternion):
        """
        :param rotation:
        :return:
        """
        self.set_rotation(rotation * self.get_rotation())

    def render_attributes(self) -> dict:
        """
        Adds name to the render attributes
        :return:
        """
        attrs = super().render_attributes()
        attrs.update({"name": self.name})
        return attrs

    def render_elements(self) -> list:
        """
        Adds pose to the render elements
        :return:
        """
        return [self.pose] + super().render_elements()

    def rotate_around(self, axis: Vector3, angle, relative_to_child=False):
        """
        Rotates this posable `angle` degrees around the given vector.
        :param axis:
        :param angle:
        :param relative_to_child:
        :return:
        """
        if relative_to_child:
            axis = self.to_parent_direction(axis)

        quat = Quaternion.new_rotate_axis(angle, axis)
        self.set_rotation(quat * self.get_rotation())

    def to_parent_direction(self, vec: Vector3) -> Vector3:
        """
        Returns the given direction vector relative to the parent frame.
        :param vec: Vector in the local frame
        :return:
        """
        return self.get_rotation() * vec

    def to_local_direction(self, vec: Vector3) -> Vector3:
        """
        Returns the given direction vector relative to the local frame
        :param vec: Direction vector in the parent frame
        :return:
        """
        return self.get_rotation().conjugated() * vec

    def to_parent_frame(self, vec: Vector3) -> Vector3:
        """
        Returns the given vector relative to the parent frame
        :param vec: Vector in the local frame
        :return:
        """
        rot = self.get_rotation()
        pos = self.get_position()
        return (rot * vec) + pos

    def to_local_frame(self, vec: Vector3) -> Vector3:
        """
        Returns the given vector relative to the local frame
        :param vec: Vector in the parent frame
        :return:
        """
        rot = self.get_rotation().conjugated()
        pos = self.get_position()
        return rot * (vec - pos)

    def align(self, my: Vector3, my_normal: Vector3, my_tangent: Vector3, at: Vector3,
              at_normal: Vector3, at_tangent: Vector3, of, relative_to_child=True):
        """
        Rotates and translates this posable, such that the
        ends of the vectors `my` and `at` touch, aligning
        such that `my_normal` points in the opposite direction of `at_normal`
        and `my_tangent` and `at_tangent` align.

        The two posables need to be in the same parent frame
        for this to work.

        You can choose to specify the positions and orientations either in the parent
        frame or in the child frame using the final argument to this method.
        Be aware that representing orientation vectors in the parent frame
        merely means that they are already rotated with respect to their parent,
        not translated.
        :param my:
        :param my_normal:
        :param my_tangent:
        :param at:
        :param at_normal:
        :param at_tangent:
        :param of:
        :type of: Posable
        :param relative_to_child:
        :return:
        """
        if not vectors_orthogonal(my_normal, my_tangent):
            raise ValueError("`my_normal` and `my_tangent` should be orthogonal.")

        if not vectors_orthogonal(at_normal, at_tangent):
            raise ValueError("`at_normal` and `at_tangent` should be orthogonal.")

        # Convert all vectors to local frame if not currently there,
        # we will need this as reference after rotation.
        if not relative_to_child:
            my = self.to_local_frame(my)
            my_normal = self.to_local_direction(my_normal)
            my_tangent = self.to_local_direction(my_tangent)

            at = of.to_local_frame(at)
            at_normal = of.to_local_direction(at_normal)
            at_tangent = of.to_local_direction(at_tangent)

        # This explains how to do the alignment easily:
        # http://stackoverflow.com/questions/21828801/how-to-find-correct-rotation-from-one-vector-to-another

        # We define coordinate systems in which "normal", "tangent" and "normal x tangent" are
        # the x, y and z axis (normal x tangent is the cross product). We then determine two
        # rotation matrices, one for the rotation of the standard basis to "my" (R1):
        my_x = self.to_parent_direction(my_normal).normalized()
        my_y = self.to_parent_direction(my_tangent).normalized()
        my_z = my_x.cross(my_y)

        # and one for the rotation of "at" (R2):
        at_x = of.to_parent_direction(-at_normal).normalized()
        at_y = of.to_parent_direction(at_tangent).normalized()
        at_z = at_x.cross(at_y)

        # We now want to provide the rotation matrix from R1 to R2.
        # The easiest way to visualize this is if we first perform
        # the inverse rotation from R1 back to the standard basis,
        # and then rotate to R2.
        r1 = RotationMatrix()
        r2 = RotationMatrix()

        # Warning: `RotationMatrix` is a Matrix4 that can potentially
        # do translations. We want to assign the first block of
        # these matrices only. Assignment happens by columns.
        r1[0:3], r1[4:7], r1[8:11] = my_x, my_y, my_z
        r2[0:3], r2[4:7], r2[8:11] = at_x, at_y, at_z

        # The columns of r1 are orthonormal, so we can simply
        # transpose the matrix to get the inverse rotation
        r1.transpose()

        # The final rotation is the inverse of r1, followed by r2
        # (left multiplication)
        """:type : RotationMatrix"""
        rotation = r2 * r1
        self.set_rotation(rotation.get_quaternion())

        assert vectors_parallel(self.to_parent_direction(my_normal),
                                of.to_parent_direction(-at_normal)), "Normal vectors failed to align!"
        assert vectors_parallel(self.to_parent_direction(my_tangent),
                                of.to_parent_direction(at_tangent)), "Tangent vectors failed to align!"

        # Finally, translate so that `my` lands at `at`
        my_pos = self.to_parent_frame(my)
        at_pos = of.to_parent_frame(at)
        translation = at_pos - my_pos
        self.translate(translation)


class PosableGroup(Posable):
    """
    A PosableGroup allows grouping a set of posables with the same parent
    without introducing a new coordinate frame (i.e. without putting
    them inside a link or a model). This lets you conveniently move
    the items within the group together, whilst their position remains
    relative to the groups parent.
    """

    # We don't want to render outer posable group
    TAG_NAME = None

    def __init__(self, name=None, **kwargs):
        """
        Overrides init to make name optional, it is not useful
        for posable groups.
        :param name:
        :param kwargs:
        :return:
        """
        super().__init__(name=name, **kwargs)

    def set_position(self, position: Vector3):
        """
        Sets the position of this posable group, translating all the
        posables within it.

        :param position:
        :return:
        """
        translation = position - self.get_position()

        # Get posables from the element list. It is good practice
        # to only have posables here, but we can easily make sure.
        posables = self.get_affected_posables()

        for posable in posables:
            posable.translate(translation)

        # Store root position
        super().set_position(position)

    def get_affected_posables(self):
        """
        Returns all sub elements which are posable and have their
        pose in the parent frame.
        :return:
        """
        return [posable for posable in self.elements
                if isinstance(posable, Posable) and posable.PARENT_FRAME]

    def render_elements(self):
        """
        Filter the pose out of the group's elements; we don't
        want it rendered
        :return:
        """
        return [el for el in super().render_elements() if not isinstance(el, Pose)]


    def set_rotation(self, rotation: Quaternion):
        """
        Set the rotation of this posable group, moving all the posables
        within it accordingly.

        :param rotation:
        :return:
        """
        root_position = self.get_position()
        inv_rotation = self.get_rotation().conjugated()

        posables = self.get_affected_posables()
        for posable in posables:
            # Get the position and rotation of the child relative
            # to this posable (i.e. as if the posable was in [0, 0]
            # with zero rotation)
            orig_position = inv_rotation * (posable.get_position() - root_position)

            # The original rotation follows from multiplying the child's rotation
            # with this group's inverse rotation
            orig_rotation = inv_rotation * posable.get_rotation()

            # New position means rotating the original point according to the new
            # rotation, and adding the current position
            new_position = (rotation * orig_position) + root_position

            # New rotation is acquired by multiplying the new rotation
            # with the existing rotation
            new_rotation = rotation * orig_rotation

            posable.set_position(new_position)
            posable.set_rotation(new_rotation)

        # We should still store our own root rotation
        super().set_rotation(rotation)