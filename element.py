"""
Basic SDF builder element.
"""
from xml.sax.saxutils import quoteattr


class Element:
    """
    Override tag name in sub class
    """
    TAG_NAME = 'element'

    """
    Basic element class
    """
    def __init__(self, attributes=None, tag_name=None):
        """
        Create a new Element with the given attributes.

        :param tag_name: Can be used to dynamically add a tag name different
                         from the class tag name.
        :param attributes: The element attributes
        :return:
        """
        self.attributes = attributes if attributes else {}
        self.tag_name = tag_name

        # Array of sub-elements, each of these elements
        # is converted
        self.elements = []

    def add_element(self, element):
        """
        Adds a child element.
        :param element:
        :return:
        """
        self.elements.append(element)

    def render_attributes(self):
        """
        Returns the dictionary of attributes that should
        be rendered. You can safely add your own attributes
        to this list by calling super when overriding this
        method.
        :return:
        """
        return self.attributes.copy()

    def render_elements(self):
        """
        Returns the list of elements that should be rendered.
        :return:
        """
        return self.elements.copy()

    def render_body(self):
        """
        Returns the string representation of this element's body.
        By default, this is the concatenation of all subelements.
        You can override this method to call super and add your
        own body.
        :return:
        """
        elements = self.render_elements()
        return "\n".join(str(element) for element in elements)

    def render(self):
        """
        Renders this element according to its properties, using the
        additional attributes "attributes"
        :param attributes: Dictionary with element attributes
        :param elements: Extra elements to add
        :param body: String body
        :return:
        """
        all_attrs = self.render_attributes()

        attrs = " ".join([a+"="+quoteattr(all_attrs[a]) for a in all_attrs])
        body = self.render_body()
        tag_name = self.TAG_NAME if self.tag_name is None else self.tag_name
        tag_open = tag_name + " " + attrs if len(attrs) else tag_name

        return "<%s>%s</%s>" % (tag_open, body, self.TAG_NAME)

    def __str__(self):
        """
        Create the XML representation of this element. By default, this
        calls `render` without arguments. The way to add just-in-time elements
        to a custom element is by overriding this to change the render call.
        :return: String XML representation
        """
        return self.render()
