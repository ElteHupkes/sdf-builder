"""
Collision / visual and geometry like classes
"""
from ..posable import Posable
from ..element import Element
from .geometries import BaseGeometry


class Structure(Posable):
    """
    Base class for collision/visual elements
    """
    def __init__(self, name, geometry, **kwargs):
        """

        :param name:
        :param geometry:
        :type geometry: BaseGeometry
        :param kwargs:
        :return:
        """
        super(Structure, self).__init__(name, **kwargs)

        # Only the geometry of a structure has a pose
        self._pose = None
        self.geometry = geometry

    # Delegate all position and rotation calls to the geometry object
    def set_position(self, position):
        self.geometry.set_position(position)

    def set_rotation(self, rotation):
        self.geometry.set_rotation(rotation)

    def get_position(self):
        return self.geometry.get_position()

    def get_rotation(self):
        return self.geometry.get_rotation()

    def get_pose(self):
        return self.geometry.get_pose()

    def render_elements(self):
        """
        :return:
        """
        return super(Structure, self).render_elements() + [self.geometry]


class Collision(Structure):
    TAG_NAME = 'collision'


class Visual(Structure):
    TAG_NAME = 'visual'

    def add_color_script(self, color):
        """
        Adds a new Material element to this Visual that has a color
        script for the given color.
        :param color: One of Gazebo's supported colors, see
        `https://bitbucket.org/osrf/gazebo/src/52abccccfec20a5f96da9dc0aeda830b48a66269/media/materials/scripts/gazebo.material?at=default`
        :return:
        """
        if color.index('/') < 0:
            color = "Gazebo/"+color.title()

        self.add_element(Material(body="<script><name>%s</name></script>" % color))

    def add_color(self, r, g, b, a=1):
        """
        Simple color setter that adds a `Material` element with the
        ambient / diffuse values at the given r,g,b,a values and
        specular set to (0.1, 0.1, 0.1, a).
        :return:
        """
        color = '%.2f %.2f %.2f %.2f' % (r, g, b, a)
        specular = '0.1 0.1 0.1 %.2f' % a
        self.add_element(Material(body="<ambient>%s</ambient><diffuse>%s</diffuse><specular>%s</specular>" %
                                       (color, color, specular)))


class Material(Element):
    TAG_NAME = 'material'
