import unittest
import envtest  # modifies path
from raytracing import *

inf = float("+inf")


class TestRandomRays(unittest.TestCase):

    def testRandomRay(self):
        rays = RandomRays()  # We keep default value, we are not interested in the construction of a specific object
        with self.assertRaises(NotImplementedError):
            # This works
            rays.randomRay()

    def testGetItem(self):
        rays = RandomRays(maxCount=10)
        with self.assertRaises(NotImplementedError):
            rays[11]  # Ok, 11 > 10

        with self.assertRaises(NotImplementedError):
            rays[-1]
