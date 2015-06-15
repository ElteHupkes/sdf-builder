"""
Simple geometries such as box, cylinder and sphere.
"""
from __future__ import division
from ..math import Vector3
from ..posable import Posable, PosableGroup
from ..util import number_format as nf
from ..physics.inertial import Inertial
import numpy as np


class Geometry(Posable):
    """
    Base geometry class. We've made this posable for a convenient use with
    the CompoundGeometry class.
    """
    TAG_NAME = 'geometry'
    RENDER_POSE = False

    def __init__(self, pose=None, **kwargs):
        """
        :param pose:
        :return:
        """
        super(Geometry, self).__init__(None, pose, **kwargs)

    def get_inertial(self, mass, **kwargs):
        """
        If implemented in the base class, returns an inertial corresponding to
        this simple shape. This inertial can then be used in a link.

        :param mass:
        :type mass: float
        :param kwargs: Other arguments this method might require in subclasses
        :return:
        :rtype: Inertial
        """
        raise NotImplementedError("`get_inertial` is not available for base geometries.")

    def get_center_of_mass(self):
        """
        Return the center of mass for this geometry. For most geometries,
        the center of mass will simply lie at the origin. This is therefore
        returned by default.

        :return: Center of mass in the local frame.
        :rtype: Vector3
        """
        return Vector3(0, 0, 0)


class CompoundGeometry(PosableGroup):
    """
    A helper class for combining multiple geometries
    """

    def __init__(self, **kwargs):
        """
        CompoundGeometry constructor
        """
        super(CompoundGeometry, self).__init__(**kwargs)
        self.geometries = []

    def add_geometry(self, geometry, mass, **kwargs):
        """
        Adds a geometry to the group along with all the possible
        arguments required to get its inertia.
        :param geometry:
        :type geometry: Geometry
        :param mass:
        :type mass: float
        :param kwargs:
        :type kwargs: dict
        """
        self.geometries.append((geometry, mass, kwargs))

    def get_inertial(self):
        """
        Returns the inertia tensor for all the combined positioned
        geometries in this compound geometry.

        Uses the first part of this question:
        http://physics.stackexchange.com/questions/17336/how-do-you-combine-two-rigid-bodies-into-one

        And the parallel axis theorem:
        https://en.wikipedia.org/wiki/Parallel_axis_theorem
        """
        total_mass = 0.0

        # Calculate the center of mass
        center_mass = Vector3(0, 0, 0)
        for geometry, mass, _ in self.geometries:
            total_mass += mass

            # Get the geometry's center of mass and translate it to the
            # frame of the posable. Since the `CompoundGeometry` is a
            # `PosableGroup`, this can be achieved by sibling translation.
            geom_center = geometry.to_sibling_frame(
                geometry.get_center_of_mass(),
                self
            )

            center_mass += mass * geom_center

        if total_mass > 0:
            center_mass /= total_mass

        # The final inertia matrix
        i_final = np.zeros((3, 3))
        for geometry, mass, args in self.geometries:
            # We need the center of mass again
            geom_center = geometry.to_sibling_frame(
                geometry.get_center_of_mass(),
                self
            )

            # Inertia matrix in local frame, I1
            ia = geometry.get_inertial(mass, **args)
            i1 = np.array([
                [ia.ixx, ia.ixy, ia.ixz],
                [ia.ixy, ia.iyy, ia.iyz],
                [ia.ixz, ia.iyz, ia.izz]
            ])

            # Calculate the rotation required to go from the compound
            # frame to the local frame of the geometry. This just
            # involves rotating the geometry's frame back over the
            # compound's rotation
            rot_quat = self.get_rotation().conjugated() * geometry.get_rotation()

            # Get the rotation matrix R1 as a 3x3 numpy array, and calculate the
            # rotated inertia tensor.
            r1 = rot_quat.get_matrix()[:3, :3]
            it = r1.dot(i1).dot(r1.T)

            # Translation to new center of mass
            t1 = center_mass - geom_center

            # J matrix as on Wikipedia
            j1 = it + mass * (t1.dot(t1) * np.eye(3) - np.outer(t1.data, t1.data))
            i_final += j1

        return Inertial(
            mass=total_mass,
            ixx=i_final[0, 0],
            iyy=i_final[1, 1],
            izz=i_final[2, 2],
            ixy=i_final[0, 1],
            ixz=i_final[0, 2],
            iyz=i_final[1, 2]
        )

class Box(Geometry):
    """
    Represents a box geometry, i.e.
    a geometry *with* a box object
    """
    def __init__(self, x, y, z, **kwargs):
        """

        :param x:
        :param y:
        :param z:
        :param kwargs:
        :return:
        """
        super(Box, self).__init__(**kwargs)
        self.size = (x, y, z)

    def render_elements(self):
        """
        Add box tag
        :return:
        """
        elements = super(Box, self).render_elements()

        x, y, z = self.size
        elements.append("<box><size>%s %s %s</size></box>" % (nf(x), nf(y), nf(z)))
        return elements

    def get_inertial(self, mass, **kwargs):
        """
        Return solid box inertial
        """
        r = mass / 12.0
        x, y, z = self.size
        ixx = r * (y**2 + z**2)
        iyy = r * (x**2 + z**2)
        izz = r * (x**2 + y**2)
        return Inertial(mass=mass, ixx=ixx, iyy=iyy, izz=izz)


class Cylinder(Geometry):
    """
    Cylinder geometry
    """
    def __init__(self, radius, length, **kwargs):
        """
        Cylinder geometry. The cylinder is defined as being a circle
        with the given radius in x / y directions, whilst having the
        given length in the z direction.
        :param radius: (x and y directions)
        :type radius: float
        :param length: Length (z-direction)
        :type length: float
        :param kwargs:
        """
        super(Cylinder, self).__init__(**kwargs)
        self.radius, self.length = radius, length

    def render_elements(self):
        """
        Add box tag
        :return:
        """
        elements = super(Cylinder, self).render_elements()

        elements.append("<cylinder><radius>%s</radius><length>%s</length></cylinder>"
                        % (nf(self.radius), nf(self.length)))
        return elements

    def get_inertial(self, mass, **kwargs):
        """
        Return cylinder inertial. You can specify `tube=True` alongside
        the radius of the center hole to get the inertia of a cylindrical tube.
        """
        tube = kwargs.get('tube', False)
        if tube:
            if 'r1' not in kwargs:
                raise AttributeError("Tube inertia requires `r1` radius for cylinder.")

            r = self.radius**2 + kwargs['r1']**2
        else:
            r = self.radius**2

        ixx = (3 * r + self.length**2) * mass / 12.0
        izz = 0.5 * mass * r
        return Inertial(mass=mass, ixx=ixx, iyy=ixx, izz=izz)


class Sphere(Geometry):
    """
    Sphere geometry
    """
    def __init__(self, radius, **kwargs):
        """
        Create a new sphere geometry
        :param radius: (x and y directions)
        :type radius: float
        :param kwargs:
        """
        super(Sphere, self).__init__(**kwargs)
        self.radius = radius

    def render_elements(self):
        """
        Add box tag
        :return:
        """
        elements = super(Sphere, self).render_elements()

        elements.append("<sphere><radius>%s</radius></sphere>"
                        % nf(self.radius))
        return elements

    def get_inertial(self, mass, **kwargs):
        """
        Return cylinder inertial
        """
        solid = kwargs.get('solid', True)
        frac = 5.0 if solid else 3.0
        ixx = (2 * mass * self.radius**2) / frac
        return Inertial(mass=mass, ixx=ixx, iyy=ixx, izz=ixx)
