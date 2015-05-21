from sdfbuilder import Element
import unittest

class A(Element):
    pass

class B(Element):
    pass

class C(B):
    pass

class TestElement(unittest.TestCase):
    def test_filter(self):
        root = Element()
        sub1 = A()
        sub2 = B()

        sub1a = A()
        sub1b = B()
        sub1c = C()

        sub1.add_elements([sub1a, sub1b, sub1c])
        root.add_elements([sub1, sub2])

        check = root.get_elements_of_type(B)
        self.assertEquals([sub2], check)

        check = root.get_elements_of_type(B, True)
        self.assertEquals([sub1b, sub1c, sub2], check)

if __name__ == '__main__':
    unittest.main()
