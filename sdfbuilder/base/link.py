from .posable import Posable
from ..physics import Inertial
from ..structure import Collision, Visual
from ..structure.geometries import Geometry, Box, Cylinder, Sphere


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
        Shortcut method to `make_geometry` with a box.

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
        return self.make_geometry(Box(x, y, z), mass, collision=collision,
                                  visual=visual, inertia=inertia, name_prefix=name_prefix)

    def make_cylinder(self, mass, radius, length, collision=True, visual=True,
                      inertia=True, name_prefix="", tube=False, r1=None):
        """
        Shortcut method to `make_geometry` with a cylinder.
        :param mass:
        :param radius:
        :param length:
        :param collision:
        :param visual:
        :param inertia:
        :param name_prefix:
        :param tube: Whether the cylinder should have a tube inertial
        :param r1: If `tube` is `True`, inner radius of the tube
        :return:
        """
        return self.make_geometry(Cylinder(radius, length), mass=mass, collision=collision,
                                  visual=visual, inertia=inertia, name_prefix=name_prefix,
                                  tube=tube, r1=r1)

    def make_sphere(self, mass, radius, collision=True, visual=True, inertia=True,
                    name_prefix="", solid=True):
        """
        Shortcut method to `make_geometry` with a cylinder.
        :param mass:
        :param radius:
        :param collision:
        :param visual:
        :param inertia:
        :param name_prefix:
        :param solid: Whether the sphere is solid
        :return:
        """
        return self.make_geometry(Sphere(radius), mass=mass, collision=collision,
                                  visual=visual, inertia=inertia, name_prefix=name_prefix, solid=solid)

    def make_geometry(self, geometry, mass=1.0, collision=True, visual=True,
                      inertia=True, name_prefix="", **kwargs):
        """
        :param geometry:
        :type geometry: Geometry
        :param mass:
        :type mass: float
        :param collision: Add a box collision
        :type collision: bool
        :param visual: Add a box visual
        :type visual: bool
        :param inertia: Set box inertia
        :type inertia: bool
        :param name_prefix: Prefix for element names (before "visual" / "collision")
        :type name_prefix: str
        :return:
        """
        return_value = []

        if inertia:
            self.inertial = geometry.get_inertial(mass, **kwargs)

        if collision:
            col = Collision(name=name_prefix+"collision", geometry=geometry)
            return_value.append(col)
            self.add_element(col)

        if visual:
            vis = Visual(name=name_prefix+"visual", geometry=geometry)
            return_value.append(vis)
            self.add_element(vis)

        return return_value