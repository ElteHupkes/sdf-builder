"""
Geometries such as box, cylinder
"""
from ..base import Element
from ..util import number_format as nf


class Geometry(Element):
    TAG_NAME = 'Geometry'


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
        super().__init__(self, **kwargs)
        self.size = (x, y, z)

    def render_elements(self):
        """
        :return:
        """
        x, y, z = self.size
        box = "<box><size>%s %s %s</size></box>" % (nf(x), nf(y), nf(z))
        return super().render_elements() + [box]