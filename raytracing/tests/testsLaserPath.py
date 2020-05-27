import unittest
import envtest  # modifies path
from raytracing import *

inf = float("+inf")


class TestLaserPath(unittest.TestCase):

    def testEigenModes(self):
        lp = LaserPath([Space(10)])
        self.assertTupleEqual(lp.eigenModes(), (None, None))

        lp = LaserPath()
        self.assertTupleEqual(lp.eigenModes(), (None, None))

        lp = LaserPath([CurvedMirror(-10)])
        self.assertNotEqual(lp.eigenModes(), (None, None))

    def testLaserModes(self):
        lp = LaserPath()
        self.assertListEqual(lp.laserModes(), [])


if __name__ == '__main__':
    unittest.main()
