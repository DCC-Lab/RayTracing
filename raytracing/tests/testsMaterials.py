import unittest
import env # modifies path
from raytracing import *


class TestMaterial(unittest.TestCase):
    def testMaterialInvalid(self):
        self.assertRaises(TypeError, Material.n, 5)


class TestN_BK7(unittest.TestCase):
    def testN_BK7TypeErrors(self):
        self.assertRaises(TypeError, N_BK7.n, None)
        self.assertRaises(TypeError, N_BK7.n, 'test')

    def testN_BK7ValueErrors(self):
        self.assertRaises(ValueError, N_BK7.n, 100)
        self.assertRaises(ValueError, N_BK7.n, 0)
        self.assertRaises(ValueError, N_BK7.n, -100)

    def testN_BK7(self):
        self.assertEqual(N_BK7.n(5), 1.3965252243506636)


if __name__ == '__main__':
    unittest.main()



