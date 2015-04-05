from .element import Element


class SDF(Element):
    """
    Root SDF element
    """
    TAG_NAME = "sdf"

    def __init__(self, version="1.5", **kwargs):
        """

        :param version:
        :param kwargs:
        :return:
        """
        super().__init__(**kwargs)
        self.version = version

    def render_attributes(self):
        """
        Adds version attribute
        :return:
        """
        attrs = super().render_attributes()
        attrs["version"] = self.version
        return attrs

    def render(self):
        """
        Adds XML header to render
        :return:
        """
        body = super().render()
        return "<?xml version=\"1.0\"?>\n"+body