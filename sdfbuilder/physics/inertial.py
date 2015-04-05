from ..base import Element
from ..util import number_format as nf


class Inertial(Element):
    """
    Convenience class for inertial elements
    """
    TAG_NAME = 'inertial'

    def __init__(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        super().__init__(**kwargs)

        self.ixx, self.ixy, self.ixz = 1, 0, 0
        self.iyy, self.iyz = 1, 0
        self.izz = 1

        self.mass = 1.0

    def set_box(self, mass, x, y, z):
        """
        Set inertial box properties
        :param mass:
        :param x:
        :param y:
        :param z:
        :return:
        """
        r = mass / 12.0
        self.ixy = self.ixz = self.iyz = 0

        self.ixx = r * (y**2 + z**2)
        self.iyy = r * (x**2 + z**2)
        self.izz = r * (x**2 + y**2)

    def set_cylinder(self, mass, radius, height):
        """
        :param mass:
        :param radius:
        :param height:
        :return:
        """
        raise NotImplementedError("This method is not yet implemented.")

    def render_body(self):
        """

        :return:
        """
        body = super().render_body()
        body += "<mass>%s</mass>" % nf(self.mass)
        body += ("<inertia>"
                 "<ixx>%s</ixx>"
                 "<ixy>%s</ixy>"
                 "<ixz>%s</ixz>"
                 "<iyy>%s</iyy>"
                 "<iyz>%s</iyz>"
                 "<izz>%s</izz>"
                 "</inertia>" % (nf(self.ixx), nf(self.ixy), nf(self.ixz),
                                 nf(self.iyy), nf(self.iyz), nf(self.izz)))
        return body