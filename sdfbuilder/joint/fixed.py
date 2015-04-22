from .joint import Joint, Limit


class FixedJoint(Joint):
    """
    Implements a shortcut fixed joint; SDF currently does not support
    such a joint, so this is really a revolute joint with fixed limits.
    """

    def __init__(self, parent, child, axis=None, name=None):
        """

        :param parent:
        :param child:
        :return:
        """
        super(FixedJoint, self).__init__("revolute", parent, child, axis=axis, name=name)
        self.axis.limit = Limit(lower=0, upper=0, effort=0, velocity=0)