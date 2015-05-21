from sdfbuilder import Element
import unittest

class A(Element):
    pass

class B(Element):
    pass


class TestElement(unittest.TestCase):
    def test_filter(self):
        root = Element()
        sub1 = A()
        sub2 = B()

        sub1a = B()
        sub1b = A()

        sub1.add_elements([sub1a, sub1b])
        root.add_elements([sub1, sub2])

        check = root.get_elements_of_type(B)
        self.assertEquals([sub2], check)

        check = root.get_elements_of_type(B, True)
        self.assertEquals([sub1a, sub2], check)

if __name__ == '__main__':
    unittest.main()
