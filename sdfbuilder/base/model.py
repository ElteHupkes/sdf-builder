from .posable import Posable
from ..joint import Joint


class Model(Posable):
    """
    SDF "model" type
    """
    TAG_NAME = 'model'

    def get_joints(self):
        """
        Returns all child elements in this model which are joints.
        :return:
        """
        return self.get_elements(Joint)