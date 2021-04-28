import envtest  # modifies path
from raytracing import *

inf = float("+inf")



class TestImagingPath(envtest.RaytracingTestCase):
    def testImagingPath(self):
        path = ImagingPath()
        self.assertIsNotNone(path)
        self.assertListEqual(path.elements, [])
        self.assertEqual(path._objectHeight, 10)
        self.assertEqual(path.objectPosition, 0)
        self.assertIsNone(path.fanAngle) # Means full angle
        self.assertEqual(path.fanNumber, 3)
        self.assertEqual(path.rayNumber, 3)
        self.assertEqual(path.precision, 1e-6)
        self.assertEqual(path.maxHeight, 10000.0)
        self.assertTrue(path.showImages)
        self.assertTrue(path.showObject)
        self.assertTrue(path.showElementLabels)
        self.assertTrue(path.showPointsOfInterest)
        self.assertTrue(path.showPointsOfInterestLabels)
        self.assertTrue(path.showPlanesAcrossPointsOfInterest)
        self.assertFalse(path.showEntrancePupil)

    def testImagingPathWithElements(self):
        space = Space(10)
        tLens = ThickLens(1, 10, 20, 2)
        elements = [space, tLens]
        path = ImagingPath(elements)
        self.assertListEqual(path.elements, elements)

    def testObjectHeight(self):
        path = ImagingPath()
        self.assertTrue(path.objectHeight, 10)

    def testSetObjectHeight(self):
        path = ImagingPath()
        path.objectHeight = 100
        self.assertTrue(path.objectHeight, 100)

    def testSetObjectHeightError(self):
        path = ImagingPath()
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

    def testApertureStopNamedTuple(self):
        f1 = 10
        f2 = 20
        elements = [Space(f1), Lens(f1, 1000), Space(f1 + f2), Lens(f2, 700), Space(f2)]
        fourF = ImagingPath(elements)
        self.assertEqual(fourF.apertureStop().diameter, 700)
        self.assertEqual(fourF.apertureStop().z, 40)

    def testEntrancePupilInfiniteApertureDiam(self):
        space = Space(2)
        tLens = ThickLens(1, 10, -9, 2)
        space2 = Space(10)
        lens = Lens(4)
        elements = [space, tLens, space2, lens]
        path = ImagingPath(elements)
        self.assertTupleEqual(path.entrancePupil(), (None, None))

    def testEntrancePupilAIs0(self):
        space = Space(2)
        lens = Lens(10, 110)
        space2 = Space(10, diameter=50)
        elements = [space, lens, space2]
        path = ImagingPath(elements)
        self.assertTupleEqual(path.entrancePupil(), (float("-inf"), float("+inf")))

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

    def testFieldStopFiniteDiameter(self):
        fieldStop = (None, inf)
        space = Space(10)
        lens = Lens(10)
        space2 = Space(20)
        path = ImagingPath([Lens(10, 450), space2, lens, space])
        self.assertTupleEqual(path.fieldStop(), fieldStop)

    def testFieldStop_1(self):
        space = Space(10)
        lens = Lens(10, 100)
        space2 = Space(20)
        lens2 = Lens(10, 50)
        path = ImagingPath([space, lens, space2, lens2, space])
        self.assertTupleEqual(path.fieldStop(), (10, 100))

    def testFieldStop_2(self):
        space = Space(10)
        lens = Lens(10, 25)
        space2 = Space(20)
        lens2 = Lens(10, 50)
        path = ImagingPath([space, lens, space2, lens2, space])
        self.assertTupleEqual(path.fieldStop(), (30, 50))

    def testFieldStopNamedTuple(self):
        space = Space(10)
        lens = Lens(10, 25)
        space2 = Space(20)
        lens2 = Lens(10, 50)
        path = ImagingPath([space, lens, space2, lens2, space])
        self.assertEqual(path.fieldStop().z, 30)
        self.assertEqual(path.fieldStop().diameter, 50)

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
        filePath = self.tempFilePath("test.png")
        comments = "This is a test"
        path = ImagingPath(System4f(10, 10, 10, 10))
        path.saveFigure(filePath=filePath, comments=comments)
        if not os.path.exists(filePath):
            self.fail("No file saved (with comments)")
        os.remove(filePath)

    def testSaveWithoutComments(self):
        filePath = self.tempFilePath("test.png")
        path = ImagingPath(System4f(10, 10, 10, 10))
        path.saveFigure(filePath=filePath)
        if not os.path.exists(filePath):
            self.fail("No file saved (without comments)")
        os.remove(filePath)

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
        self.assertAlmostEqual(chiefRay.y, 10, 2)
        self.assertAlmostEqual(chiefRay.theta, -1, 3)

    def testPrincipalRayIsNone(self):
        path = ImagingPath()
        path.append(System2f(f=10, diameter=float("+inf")))
        path.append(Aperture(diameter=20))
        principalRay = path.principalRay()
        self.assertIsNone(principalRay, principalRay)

    def testPrincipalRayIsNotNone(self):
        path = ImagingPath()
        path.append(System2f(f=10, diameter=10))
        path.append(Aperture(diameter=20))
        principalRay = path.principalRay()
        self.assertAlmostEqual(principalRay.y, 10, 2)
        self.assertAlmostEqual(principalRay.theta, -1, 3)

    def testMarginalRaysNoApertureStop(self):
        path = ImagingPath(System4f(10, 10))
        ray1, ray2 = path.marginalRays()
        self.assertIsNone(ray1)
        self.assertIsNone(ray2)

    def testMarginalRaysIsImaging(self):
        path = ImagingPath(System4f(10, 10))
        path.append(Aperture(10))
        ray1, ray2 = path.marginalRays()
        self.assertIsNone(ray1)
        self.assertIsNone(ray2)

    def testMarginalRays(self):
        path = ImagingPath(System2f(10, 10))
        rays = path.marginalRays(10)
        ray1, ray2 = rays[0], rays[1]
        self.assertEqual(len(rays), 2)
        self.assertEqual(ray1.y, 10)
        self.assertEqual(ray1.theta, -0.5)
        self.assertEqual(ray2.y, 10)
        self.assertEqual(ray2.theta, -1.5)

    def testMarginalRays(self):
        path = ImagingPath(System2f(10, 10))
        rays = path.marginalRays(10)
        self.assertEqual(rays.up, rays[0])
        self.assertEqual(rays.down, rays[1])

    def testMarginalRaysThetaUpAndDownFlipped(self):
        path = ImagingPath(System2f(5))
        tl = ThickLens(1.1, 0.1, -0.1, 10)
        path.append(tl)
        path.append(Aperture(5))
        rays = path.marginalRays(10)
        ray1, ray2 = rays[0], rays[1]
        self.assertEqual(len(rays), 2)
        self.assertEqual(ray1.y, 10)
        self.assertAlmostEqual(ray1.theta, -0.38764, 5)
        self.assertEqual(ray2.y, 10)
        self.assertAlmostEqual(ray2.theta, -0.5112, 4)

    def testAxialRay(self):
        path = ImagingPath(System2f(10, 100))
        ray = path.axialRay()
        self.assertEqual(ray.y, 0)
        self.assertEqual(ray.theta, 5)

    def testNA(self):
        path = ImagingPath(System2f(f=1000, diameter=20))
        self.assertAlmostEqual(path.NA(), 0.01,4)

    def testLargeNA(self):
        path = ImagingPath(System2f(f=10, diameter=200))
        self.assertTrue(path.NA() <= 1.0)

    def test4fNA(self):
        path = ImagingPath(System4f(f1=100, diameter1=20, f2=40, diameter2=20))
        self.assertAlmostEqual(path.NA(), 0.1, 3)

    def testfNumber(self):
        path = ImagingPath(System2f(f=10, diameter=10))
        self.assertAlmostEqual(path.fNumber(), 1, 4)

    def testSmallfNumber(self):
        path = ImagingPath(System2f(f=10, diameter=2))
        self.assertAlmostEqual(path.fNumber(), 5, 4)

    def testLagrangeImagingPathNoApertureIsInfinite(self):
        path = ImagingPath()
        path.append(Space(d=50))
        path.append(Lens(f=50))
        path.append(Space(d=50))
        self.assertEqual(path.lagrangeInvariant(), float("+inf"))

    def testLagrangeImagingPathNoFieldStopIsInfinite(self):
        path = ImagingPath()
        path.append(Space(d=50))
        path.append(Lens(f=50, diameter=50))
        path.append(Space(d=50))
        self.assertEqual(path.lagrangeInvariant(), float("+inf"))

    def testLagrangeImagingPath(self):
        path = ImagingPath()
        path.append(Space(d=50))
        path.append(Lens(f=50, diameter=50))
        path.append(Space(d=50, diameter=40))
        principalRay = path.principalRay()
        axialRay = path.axialRay()
        before = path.opticalInvariant(ray1=axialRay, ray2=principalRay, z=0)
        after = path.opticalInvariant(ray1=axialRay, ray2=principalRay, z=150)
        self.assertAlmostEqual(before, after)

    def testLagrangeInvariantBothNotNone(self):
        ray1 = Ray()
        ray2 = Ray(0, 0.1)
        path = ImagingPath()
        path.append(Space(d=50))
        path.append(Lens(f=50, diameter=50))
        path.append(Space(d=50, diameter=40))
        before = path.opticalInvariant(ray1, ray2, 10)
        after = path.opticalInvariant(ray1, ray2, 70)
        self.assertAlmostEqual(before, after)

    def testChiefRayInfiniteFOVNoY(self):
        path = ImagingPath(System2f(10, 10))
        with self.assertRaises(ValueError):
            path.chiefRay()

if __name__ == '__main__':
    envtest.main()

