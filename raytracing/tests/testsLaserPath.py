import unittest
import envtest # modifies path
from raytracing import *

inf = float("+inf")

class TestLaserPath(unittest.TestCase):

    def testEigenModes(self):
        lp = LaserPath([Space(10)])
        self.assertIsNotNone(lp.eigenModes())