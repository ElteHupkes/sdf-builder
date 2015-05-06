"""
Basic SDF builder element.
"""
from xml.sax.saxutils import quoteattr
from .util import number_format as nf


class Element(object):
    """
    Basic element class
    """

    """
    Tag name to override in subclass. If the tag name is None,
    the wrapper is not rendered.
    """
    TAG_NAME = None

    def __init__(self, **kwargs):
        """
        Create a new Element with the given attributes.

        :param tag_name: Can be used to dynamically add a tag name different
                         from the class tag name.
        :param attributes: The element attributes
        :return:
        """
        self.attributes = kwargs["attributes"] if "attributes" in kwargs else {}
        self.tag_name = kwargs["tag_name"] if "tag_name" in kwargs else None
        self.body = kwargs["body"] if "body" in kwargs else ""

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

    def add_elements(self, elements):
        """
        Convenience method to add multiple elements at once as a list.
        :param elements:
        :return:
        """
        self.elements += elements

    def has_element(self, class_type):
        """
        Returns whether or not this element contains a child
        element of the given type
        :param class_type:
        :return:
        """
        return len(self.get_elements(class_type)) > 0

    def get_elements(self, class_type):
        """
        Returns all elements of the given class type
        :param class_type:
        :return:
        """
        return [el for el in self.elements if isinstance(el, class_type)]

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
        return self.elements[:]

    def render_body(self):
        """
        Returns the string representation of this element's body.
        By default, this is the concatenation of all subelements.
        You can override this method to call super and add your
        own body.
        :return:
        """
        elements = self.render_elements()
        return "\n".join(str(element) for element in elements) + self.body

    def render(self):
        """
        Renders this element according to its properties.
        :return:
        """
        all_attrs = self.render_attributes()

        body = self.render_body()
        tag_name = self.TAG_NAME if self.tag_name is None else self.tag_name

        if tag_name is None:
            return body
        else:
            attrs = " ".join([a+"="+quoteattr(
                # Use number format if a number is detected
                nf(all_attrs[a]) if isinstance(all_attrs[a], float) else str(all_attrs[a])
            ) for a in all_attrs])
            tag_open = tag_name + " " + attrs if len(attrs) else tag_name
            return "<%s />" % tag_open if len(body) == 0 else "<%s>%s</%s>" % (tag_open, body, tag_name)

    def __str__(self):
        """
        Create the XML representation of this element. By default, this
        calls `render` without arguments. The way to add just-in-time elements
        to a custom element is by overriding this to change the render call.
        :return: String XML representation
        """
        return self.render()
