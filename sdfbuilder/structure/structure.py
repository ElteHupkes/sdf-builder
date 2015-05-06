"""
Collision / visual and geometry like classes
"""
from ..posable import Posable


class Structure(Posable):
    """
    Base class for collision/visual elements
    """
    def __init__(self, name, geometry, **kwargs):
        """

        :param name:
        :param kwargs:
        :return:
        """
        super(Structure, self).__init__(name, **kwargs)

        """:type : Geometry"""
        self.geometry = geometry

    def render_elements(self):
        """
        :return:
        """
        return super(Structure, self).render_elements() + [self.geometry]


class Collision(Structure):
    TAG_NAME = 'collision'


class Visual(Structure):
    TAG_NAME = 'visual'