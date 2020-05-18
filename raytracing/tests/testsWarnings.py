import unittest
import envtest # modifies path
from raytracing import *
import warnings

inf = float("+inf")


class TestMatrix(unittest.TestCase):
    def testMatrix(self):
        m = Matrix()
        self.assertIsNotNone(m)

    def testThorlabsLensesWarning(self):
        l = thorlabs.AC254_030_A()

if __name__ == '__main__':
    unittest.main()