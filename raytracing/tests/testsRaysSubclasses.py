import unittest
import envtest  # modifies path
from raytracing import *

inf = float("+inf")


class TestRandomRays(unittest.TestCase):

    def testRandomRay(self):
        rays = RandomRays()  # We keep default value, we are not intersted in the construction of a specific object
        with self.assertRaises(NotImplementedError):
            # This works
            rays.randomRay()
