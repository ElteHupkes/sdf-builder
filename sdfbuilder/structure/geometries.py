"""
Simple geometries such as box, cylinder and sphere.
"""
from ..base.element import Element
from ..util import number_format as nf
from ..physics.inertial import Inertial


class Geometry(Element):
    TAG_NAME = 'geometry'

    def get_inertial(self, mass):
        """
        If implemented in the base class, returns an inertial corresponding to
        this simple shape. This inertial can then be used in a link.

        :param mass:
        :type mass: float
        :return:
        :rtype: Inertial
        """
        raise NotImplementedError("`get_inertial` is not available for base geometries.")


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

    def get_inertial(self, mass):
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

    def get_inertial(self, mass):
        """
        Return cylinder inertial
        """
        ixx = (3 * self.radius**2 + self.length**2) * mass / 12.0
        izz = 0.5 * mass * self.radius**2
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

    def get_inertial(self, mass):
        """
        Return cylinder inertial
        """
        ixx = (2 * mass * self.radius**2) / 3.0
        return Inertial(mass=mass, ixx=ixx, iyy=ixx, izz=ixx)
