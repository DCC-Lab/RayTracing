import unittest
import envtest  # modifies path
from raytracing import *

inf = float("+inf")


class TestImagingPath(unittest.TestCase):
    def testImagingPath(self):
        path = ImagingPath()
        self.assertIsNotNone(path)
        self.assertListEqual(path.elements, [])
        self.assertEqual(path._objectHeight, 10)
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

    def testObjectHeight(self):
        path = ImagingPath()
        self.assertTrue(path.objectHeight, 10)

        with self.assertRaises(ValueError):
            path.objectHeight = -0.1

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

    def testDisplayRangeWithFiniteLens(self):
        path = ImagingPath()  # default objectHeight is 10
        path.append(Space(d=10))
        path.append(Lens(f=5, diameter=20))

        largestDiameter = 20

        self.assertEqual(path.displayRange(), largestDiameter)

    def testDisplayRange(self):
        path = ImagingPath()
        path.append(Space(2))
        path.append(CurvedMirror(-5, 10))
        self.assertAlmostEqual(path.displayRange(), 5 * 10)

        path.objectHeight = 1
        self.assertEqual(path.displayRange(), 10)

    def testDisplayRangeWithEmptyPath(self):
        path = ImagingPath()

        largestDiameter = path.objectHeight * 2

        self.assertEqual(path.displayRange(), largestDiameter)

    @unittest.skip("Maybe will change")
    def testDisplayRangeLargestDiameterBiggerThanObj(self):
        path = ImagingPath(System4f(10, 10, 10, 20))
        path.objectHeight = 1
        print(path.displayRange())

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

    def testFieldStop(self):
        space = Space(10)
        lens = Lens(10, 100)
        space2 = Space(20)
        lens2 = Lens(10, 50)
        path = ImagingPath([space, lens, space2, lens2, space])
        self.assertTupleEqual(path.fieldStop(), (10, 100))

        space = Space(10)
        lens = Lens(10, 25)
        space2 = Space(20)
        lens2 = Lens(10, 50)
        path = ImagingPath([space, lens, space2, lens2, space])
        self.assertTupleEqual(path.fieldStop(), (30, 50))

    def testEntrancePupilNoBackwardConjugate(self):
        path = ImagingPath()
        path.append(System2f(f=10))
        self.assertEqual(path.fieldOfView(), inf)

    def testImagingPathInfiniteFieldOfView2(self):
        path = ImagingPath()
        path.append(System2f(f=10, diameter=10))
        self.assertEqual(path.fieldOfView(), inf)

    def testImagingPathInfiniteFieldOfView3(self):
        path = ImagingPath()
        path.append(System2f(f=10, diameter=path.maxHeight * 2))
        path.append(Aperture(diameter=path.maxHeight * 2.3))
        self.assertEqual(path.fieldOfView(), inf)

    def testImagingPathFiniteFieldOfView(self):
        path = ImagingPath()
        path.append(System2f(f=10, diameter=10))
        path.append(Aperture(diameter=20))
        self.assertAlmostEqual(path.fieldOfView(), 20, 2)

    def testImageSizeDIs0(self):
        path = ImagingPath(System2f(f=10, diameter=10))
        path.append(Aperture(20))
        self.assertEqual(path.imageSize(), inf)

    def testImageSizeInfinite(self):
        path = ImagingPath(System4f(f1=10, f2=2, diameter1=10))
        self.assertEqual(path.imageSize(), inf)

    def testImageSize(self):
        path = ImagingPath(System4f(f1=10, f2=20, diameter1=10, diameter2=20))
        imgSize = 2 * 10 / 3 * 2
        self.assertAlmostEqual(path.imageSize(), imgSize, 2)

    def testSave(self):
        filename = "test.png"
        comments = "This is a test"
        path = ImagingPath(System4f(10, 10, 10, 10))
        path.save(filename, comments=comments)
        if not os.path.exists(filename):
            self.fail("No file saved (with comments)")
        os.remove(filename)

        path.save(filename)
        if not os.path.exists(filename):
            self.fail("No file saved (without comments)")
        os.remove(filename)

    def testRearrangeRayTraceForPlottingAllNonBlocked(self):
        path = ImagingPath([Space(10), Lens(5, 20), Space(10)])
        initialRay = Ray(0, 1)  # Will go through without being blocked
        listOfRays = path.trace(initialRay)
        xy = path.rearrangeRayTraceForPlotting(listOfRays, True)
        x = [0, 0, 10, 10, 10, 0]
        z = [0, 0, 10, 10, 10, 20]
        self.assertTupleEqual(xy, (z, x))

        initialRay = Ray(0, 1.01)  # Will be blocked
        listOfRays = path.trace(initialRay)
        xy = path.rearrangeRayTraceForPlotting(listOfRays, True)
        self.assertTupleEqual(xy, ([], []))

        initialRay = Ray(0, 1.01)  # Will be blocked
        listOfRays = path.trace(initialRay)
        xy = path.rearrangeRayTraceForPlotting(listOfRays, False)
        x = [0, 0, 10.1]
        z = [0, 0, 10]
        self.assertTupleEqual(xy, (z, x))

    def testChiefRayNoApertureStop(self):
        path = ImagingPath(System2f(10))
        chiefRay = path.chiefRay()
        self.assertIsNone(chiefRay)

    def testChiefRayBIs0(self):
        path = ImagingPath(System4f(10, 10))
        path.append(Aperture(10))
        self.assertIsNone(path.chiefRay())

    def testChiefRayYIsNone(self):
        path = ImagingPath()
        path.append(System2f(10, 10))
        path.append(Aperture(diameter=20))
        chiefRay = path.chiefRay()
        self.assertAlmostEqual(chiefRay.y, 20, 2)
        self.assertAlmostEqual(chiefRay.theta, -2, 3)

    def testPrincipalRay(self):
        path = ImagingPath(System4f(10, 10))
        self.assertIsNone(path.principalRay())

        path = ImagingPath(System4f(10, 10))
        path.append(Aperture(10))
        self.assertIsNone(path.principalRay())

        path = ImagingPath()
        path.append(System2f(10, 10))
        path.append(Aperture(diameter=20))
        principalRay = path.principalRay()
        self.assertAlmostEqual(principalRay.y, 20, 2)
        self.assertAlmostEqual(principalRay.theta, -2, 3)


    def testMarginalRaysNoApertureStop(self):
        path = ImagingPath(System4f(10, 10))
        self.assertIsNone(path.marginalRays())

    def testMarginalRaysIsImaging(self):
        path = ImagingPath(System4f(10, 10))
        path.append(Aperture(10))
        self.assertIsNone(path.marginalRays())

    def testMarginalRays(self):
        path = ImagingPath(System2f(10, 10))
        rays = path.marginalRays(10)
        self.assertEqual(len(rays), 2)
        ray1, ray2 = rays[0], rays[1]
        self.assertEqual(ray1.y, 10)
        self.assertEqual(ray1.theta, -0.5)
        self.assertEqual(ray2.y, 10)
        self.assertEqual(ray2.theta, -1.5)

        path = ImagingPath(System2f(5))
        tl = ThickLens(1.1, 0.1, -0.1, 10)
        path.append(tl)
        path.append(Aperture(5))
        rays = path.marginalRays(10)
        self.assertEqual(len(rays), 2)
        ray1, ray2 = rays[0], rays[1]
        self.assertEqual(ray1.y, 10)
        self.assertAlmostEqual(ray1.theta, -0.38764, 5)
        self.assertEqual(ray2.y, 10)
        self.assertAlmostEqual(ray2.theta, -0.5112, 4)

    def testAxialRay(self):
        path = ImagingPath(System2f(10, 100))
        rays = path.axialRay()
        self.assertEqual(len(rays), 2)
        ray1, ray2 = rays[0], rays[1]
        self.assertEqual(ray1.y, 0)
        self.assertEqual(ray1.theta, 5)
        self.assertEqual(ray2.y, 0)
        self.assertEqual(ray2.theta, -5)

    def testLagrangeImagingPathNoAperture(self):
        path = ImagingPath()
        path.append(Space(d=50))
        path.append(Lens(f=50))
        path.append(Space(d=50))
        with self.assertRaises(ValueError):
            path.lagrangeInvariant(z=0)

    def testLagrangeImagingPathNoFieldStop(self):
        path = ImagingPath()
        path.append(Space(d=50))
        path.append(Lens(f=50, diameter=50))
        path.append(Space(d=50))
        with self.assertRaises(ValueError):
            path.lagrangeInvariant(z=0)

    def testLagrangeImagingPath(self):
        path = ImagingPath()
        path.append(Space(d=50))
        path.append(Lens(f=50, diameter=50))
        path.append(Space(d=50, diameter=40))
        before = path.lagrangeInvariant(z=0)
        after = path.lagrangeInvariant(z=150)
        self.assertAlmostEqual(before, after)

    def testLagrangeInvariantBothNotNone(self):
        ray1 = Ray()
        ray2 = Ray(0, 0.1)
        path = ImagingPath()
        path.append(Space(d=50))
        path.append(Lens(f=50, diameter=50))
        path.append(Space(d=50, diameter=40))
        before = path.lagrangeInvariant(ray1, ray2, 10)
        after = path.lagrangeInvariant(ray1, ray2, 70)
        self.assertAlmostEqual(before, after)

    def testChiefRayInfiniteFOVNoY(self):
        path = ImagingPath(System2f(10, 10))
        with self.assertRaises(ValueError):
            path.chiefRay()



if __name__ == '__main__':
    unittest.main()