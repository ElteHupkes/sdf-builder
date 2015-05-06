from ..element import Element
from ..util import number_format as nf


class Inertial(Element):
    """
    Convenience class for inertial elements
    """
    TAG_NAME = 'inertial'

    def __init__(self, mass=1.0, ixx=0, iyy=0, izz=0, ixy=0, ixz=0, iyz=0, **kwargs):
        """
        :param mass:
        :param ixx:
        :param iyy:
        :param izz:
        :param ixy:
        :param ixz:
        :param iyz:
        :param kwargs:
        """
        super(Inertial, self).__init__(**kwargs)

        self.ixx, self.ixy, self.ixz = (ixx, ixy, ixz)
        self.iyy, self.iyz = (iyy, iyz)
        self.izz = izz
        self.mass = mass

    def render_body(self):
        """
        Adds inertia to body before render.
        :return:
        """
        body = super(Inertial, self).render_body()
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