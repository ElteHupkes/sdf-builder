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
