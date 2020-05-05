import unittest
import env # modifies path
from raytracing import *

inf = float("+inf")


class TestImagingPath(unittest.TestCase):
    def testImagingPathInfiniteFieldOfView(self):
        path = ImagingPath()
        path.append(System2f(f=10))
        self.assertEqual(path.fieldOfView(), inf)
    def testImagingPathInfiniteFieldOfView2(self):
        path = ImagingPath()
        path.append(System2f(f=10, diameter=10))
        self.assertEqual(path.fieldOfView(), inf)
    def testImagingPathInfiniteFieldOfView3(self):
        path = ImagingPath()
        path.append(System2f(f=10, diameter=10))
        path.append(Aperture(diameter=20))
        self.assertAlmostEqual(path.fieldOfView(), 20, 2)



if __name__ == '__main__':
    unittest.main()