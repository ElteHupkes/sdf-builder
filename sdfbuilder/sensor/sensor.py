from ..posable import Posable


class Sensor(Posable):
    """
    Sensor base class, using the base class should
    suffice in most cases since writing the XML is
    just as easy.
    """
    # Sensor tag name
    TAG_NAME = "sensor"

    def __init__(self, name, sensor_type, pose=None, **kwargs):
        super(Sensor, self).__init__(name, pose, **kwargs)
        self.type = sensor_type

    def render_attributes(self):
        """
        Add type to the attributes to be rendered
        """
        attrs = super(Sensor, self).render_attributes()
        attrs['type'] = self.type
        return attrs