import unittest
import envtest # modifies path
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

    def testDisplayRangeWithFiniteLens(self):
        path = ImagingPath()  # default objectHeight is 10
        path.append(Space(d=10))
        path.append(Lens(f=5, diameter=20))

        largestDiameter = 20

        self.assertEqual(path.displayRange(), largestDiameter)

    def testDisplayRangeWithObjectHigherThanLens(self):
        path = ImagingPath()
        path.objectHeight = 20
        path.append(Space(d=10))
        path.append(Lens(f=5, diameter=20))

        largestDiameter = path.objectHeight * 2

        self.assertEqual(path.displayRange(), largestDiameter)

    def testDisplayRangeWithEmptyPath(self):
        path = ImagingPath()

        largestDiameter = path.objectHeight * 2

        self.assertEqual(path.displayRange(), largestDiameter)

    def testEntrancePupilAIs0(self):
        space = Space(2)
        lens = Lens(10, 110)
        space2 = Space(10, diameter=50)
        elements = [space, lens, space2]
        path = ImagingPath(elements)
        self.assertIsNotNone(path.entrancePupil())


if __name__ == '__main__':
    unittest.main()
