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


if __name__ == '__main__':
    unittest.main()
