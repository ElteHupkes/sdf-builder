from .posable import Posable
from ..physics import Inertial
from ..structure import Collision, Visual
from ..structure.geometries import Box


class Link(Posable):
    """
    Represents a link object
    """
    TAG_NAME = 'link'

    def __init__(self, name, **kwargs):
        """

        :param name:
        :param kwargs:
        :return:
        """
        super(Link, self).__init__(name=name, **kwargs)

        # Only create inertial if required
        """:type : Inertial"""
        self.inertial = None

    def render_elements(self):
        """
        :return:
        """
        elements = super(Link, self).render_elements()
        return elements if self.inertial is None else elements + [self.inertial]

    def ensure_inertial(self):
        """
        Creates an inertial element if this
        link does not have one.
        :return:
        """
        if self.inertial is None:
            self.inertial = Inertial()

    def make_box(self, mass, x, y, z, collision=True, visual=True, inertia=True, name_prefix=""):
        """
        Gives this link box properties.

        :param mass:
        :param x:
        :param y:
        :param z:
        :param collision: Add a box collision
        :param visual: Add a box visual
        :param inertia: Set box inertia
        :param name_prefix:
        :return: Newly created visual and collision elements, if applicable
        """
        return_value = []

        if inertia:
            self.ensure_inertial()
            self.inertial.set_box(mass, x, y, z)

        if collision:
            col = Collision(name=name_prefix+"collision", geometry=Box(x, y, z))
            return_value.append(col)
            self.add_element(col)

        if visual:
            vis = Visual(name=name_prefix+"visual", geometry=Box(x, y, z))
            return_value.append(vis)
            self.add_element(vis)

        return return_value