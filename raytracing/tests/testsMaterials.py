import unittest
import env # modifies path
from raytracing import *


class TestMaterial(unittest.TestCase):
    def testMaterialInvalid(self):
        self.assertRaises(TypeError, Material.n, 5)

class TestN_BK7(unittest.TestCase):
    def testN_BK7Invalid(self):
        



if __name__ == '__main__':
    unittest.main()



