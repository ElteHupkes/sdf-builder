"""
Geometries such as box, cylinder
"""
from ..base.element import Element
from ..util import number_format as nf


class Geometry(Element):
    TAG_NAME = 'geometry'


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