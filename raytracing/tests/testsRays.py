import unittest
import envtest  # modifies path
from raytracing import *

inf = float("+inf")


class TestRays(unittest.TestCase):

    def testRayCountHist(self):
        r = Rays([Ray()])
        self.assertIsNotNone(r.rayCountHistogram())  # First time compute
        self.assertIsNotNone(r.rayCountHistogram())  # Second time compute, doesn't work

    def testRayAnglesHist(self):
        r = Rays([Ray()])
        self.assertIsNotNone(r.rayAnglesHistogram())  # First time compute
        self.assertIsNotNone(r.rayAnglesHistogram())  # Second time compute, doesn't work


if __name__ == '__main__':
    unittest.main()
