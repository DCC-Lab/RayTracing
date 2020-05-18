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

    def testEntrancePupilNoBackwardConjugate(self):
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

        self.assertEqual(path.displayRange, largestDiameter)

    def testDisplayRangeWithObjectHigherThanLens(self):
        path = ImagingPath()
        path.objectHeight = 20
        path.append(Space(d=10))
        path.append(Lens(f=5, diameter=20))

        largestDiameter = path.objectHeight * 2

        self.assertEqual(path.displayRange, largestDiameter)

    def testDisplayRangeWithEmptyPath(self):
        path = ImagingPath()

        largestDiameter = path.objectHeight * 2

        self.assertEqual(path.displayRange, largestDiameter)

   def testEntrancePupilAIs0(self):
        space = Space(2)
        lens = Lens(10, 110)
        space2 = Space(10, diameter=50)
        elements = [space, lens, space2]
        path = ImagingPath(elements)
        self.assertTupleEqual(path.entrancePupil(), (None, None))

    def testEntrancePupil(self):
        space = Space(2)
        lens = Lens(10, 110)
        space2 = Space(10)
        lens2 = ThickLens(4, 12, -4, 2, 600)
        elements = [space, lens, space2, lens2]
        path = ImagingPath(elements)
        pupilPosition = 2
        stopDiameter = 110
        Mt = 1
        self.assertTupleEqual(path.entrancePupil(), (pupilPosition, stopDiameter / Mt))

    def testFieldStopInfiniteDiameter(self):
        fieldStop = (None, inf)
        space = Space(10)
        lens = Lens(10)
        space2 = Space(20)
        path = ImagingPath([space, lens, space2, lens, space])
        self.assertTupleEqual(path.fieldStop(), fieldStop)

        path = ImagingPath([Lens(10, 450), space2, lens, space])
        self.assertTupleEqual(path.fieldStop(), fieldStop)

        path = ImagingPath([space, Lens(10, 450), space2, lens, space])
        self.assertTupleEqual(path.fieldStop(), fieldStop)

    @unittest.skip
    def testFieldStop(self):
        space = Space(10)
        lens = Lens(10, 100)
        space2 = Space(20)
        lens2 = Lens(10, 50)
        path = ImagingPath([space, lens, space2, lens2, space])
        print(path.apertureStop())
        # FIXME: I think this should be (30, 50)...
        self.assertTupleEqual(path.fieldStop(), (30, 50))

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
