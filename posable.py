from element import Element
from util.euclid import Vector3, Quaternion
from util import number_format as nf


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
        # which are yaw, pitch, roll respectively.
        yaw, pitch, roll = self.rotation.get_euler()
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

    def render_attributes(self):
        """
        Adds name to the render attributes
        :return:
        """
        attrs = super().render_attributes()
        attrs.update({"name": self.name})
        return attrs

    def render_elements(self):
        """
        Adds pose to the render elements
        :return:
        """
        return super().render_elements() + [self.pose]

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

    def to_parent_direction(self, vec: Vector3):
        """
        Returns the given direction vector relative to the parent frame.
        :param vec: Vector in the local frame
        :return:
        """
        return self.get_rotation() * vec

    def to_local_direction(self, vec: Vector3):
        """
        Returns the given direction vector relative to the local frame
        :param vec: Direction vector in the parent frame
        :return:
        """
        return self.get_rotation().conjugated() * vec

    def to_parent_frame(self, vec: Vector3):
        """
        Returns the given vector relative to the parent frame
        :param vec: Vector in the local frame
        :return:
        """
        rot = self.get_rotation()
        pos = self.get_position()
        return (rot * vec) + pos

    def to_local_frame(self, vec: Vector3):
        """
        Returns the given vector relative to the local frame
        :param vec: Vector in the parent frame
        :return:
        """
        rot = self.get_rotation().conjugated()
        pos = self.get_position()
        return rot * (vec - pos)


class PosableGroup(Posable):
    """
    A PosableGroup allows grouping a set of posables with the same parent
    without introducing a new coordinate frame (i.e. without putting
    them inside a link or a model). This lets you conveniently move
    the items within the group together, whilst their position remains
    relative to the groups parent.
    """

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
            posable.set_position(posable.get_position() + translation)

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