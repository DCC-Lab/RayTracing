import unittest
import envtest  # modifies path
from raytracing import *

inf = float("+inf")


class TestImagingPath(unittest.TestCase):
    def testImagingPath(self):
        path = ImagingPath()
        self.assertIsNotNone(path)
        self.assertListEqual(path.elements, [])
        self.assertEqual(path.objectHeight, 10)
        self.assertEqual(path.objectPosition, 0)
        self.assertEqual(path.fanAngle, 0.1)
        self.assertEqual(path.fanNumber, 9)
        self.assertEqual(path.rayNumber, 3)
        self.assertEqual(path.precision, 0.001)
        self.assertEqual(path.maxHeight, 10000.0)
        self.assertTrue(path.showImages)
        self.assertTrue(path.showObject)
        self.assertTrue(path.showElementLabels)
        self.assertTrue(path.showPointsOfInterest)
        self.assertTrue(path.showPointsOfInterestLabels)
        self.assertTrue(path.showPlanesAcrossPointsOfInterest)
        self.assertFalse(path.showEntrancePupil)

        space = Space(10)
        tLens = ThickLens(1, 10, 20, 2)
        elements = [space, tLens]
        path = ImagingPath(elements)
        self.assertListEqual(path.elements, elements)

    def testApertureStopInfiniteAperture(self):
        space = Space(10)
        slab = DielectricSlab(1.45, 125)
        mirror = CurvedMirror(10)
        path = ImagingPath([space, slab, mirror])
        self.assertTupleEqual(path.apertureStop(), (None, inf))

    def testApertureStop(self):
        f1 = 10
        f2 = 20
        elements = [Space(f1), Lens(f1, 1000), Space(f1 + f2), Lens(f2, 700), Space(f2)]
        fourF = ImagingPath(elements)
        self.assertTupleEqual(fourF.apertureStop(), (40, 700))

    def testEntrancePupilInfiniteApertureDiam(self):
        space = Space(2)
        tLens = ThickLens(1, 10, -9, 2)
        space2 = Space(10)
        lens = Lens(4)
        elements = [space, tLens, space2, lens]
        path = ImagingPath(elements)
        self.assertTupleEqual(path.entrancePupil(), (None, None))

    def testEntrancePupil(self):
        space = Space(2)
        tLens = Lens(10)
        space2 = Space(10, diameter=125)
        lens = Lens(4, 400)
        elements = [space, tLens, space2, lens]
        path = ImagingPath(elements)
        print(path.apertureStop())


    # def testImagingPathInfiniteFieldOfView(self):
    #     path = ImagingPath()
    #     path.append(System2f(f=10))
    #     self.assertEqual(path.fieldOfView(), inf)
    #
    # def testImagingPathInfiniteFieldOfView2(self):
    #     path = ImagingPath()
    #     path.append(System2f(f=10, diameter=10))
    #     self.assertEqual(path.fieldOfView(), inf)
    #
    # def testImagingPathInfiniteFieldOfView3(self):
    #     path = ImagingPath()
    #     path.append(System2f(f=10, diameter=10))
    #     path.append(Aperture(diameter=20))
    #     self.assertAlmostEqual(path.fieldOfView(), 20, 2)


if __name__ == '__main__':
    unittest.main()
