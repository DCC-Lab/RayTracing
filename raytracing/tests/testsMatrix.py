import envtest  # modifies path
import subprocess

from raytracing import *
inf = float("+inf")


class TestMatrix(envtest.RaytracingTestCase):

    def testMatrix(self):
        m = Matrix()
        self.assertIsNotNone(m)

    def testNullApertureDiameter(self):
        with self.assertRaises(ValueError):
            Matrix(apertureDiameter=0)

    def testNegativeApertureDiameter(self):
        with self.assertRaises(ValueError):
            Matrix(apertureDiameter=-0.1)

    def testNullApertureNA(self):
        with self.assertRaises(ValueError):
            Matrix(apertureNA=0)

    def testNonNullBlockingApertureNA(self):
        m = Matrix(1,0,0,1,apertureNA=0.25)
        ray = Ray(y=0, theta=0.5)
        outRay = m*ray
        self.assertTrue(outRay.isBlocked)

    def testNonNullNonBlockingApertureNA(self):
        m = Matrix(1,0,0,1,apertureNA=0.5)
        ray = Ray(y=0, theta=0.25)
        outRay = m*ray
        self.assertFalse(outRay.isBlocked)

    def testNonNullJustAtTheLimitApertureNA(self):
        m = Matrix(1,0,0,1,apertureNA=0.5)
        ray = Ray(y=0, theta=0.5)
        outRay = m*ray
        self.assertFalse(outRay.isBlocked)

    def testApertureWithNA(self):
        m = Aperture(diameter=1.0, NA=0.5)
        ray = Ray(y=0, theta=0.6)
        outRay = m*ray
        self.assertTrue(outRay.isBlocked)

        m = Aperture(diameter=0.5, NA=0.5)
        ray = Ray(y=1.0, theta=0)
        outRay = m*ray
        self.assertTrue(outRay.isBlocked)

        m = Aperture(diameter=0.5, NA=0.5)
        ray = Ray(y=1.0, theta=0.6)
        outRay = m*ray
        self.assertTrue(outRay.isBlocked)

        m = Aperture(diameter=0.5*2, NA=0.5)
        ray = Ray(y=0.5, theta=0.5)
        outRay = m*ray
        self.assertFalse(outRay.isBlocked)

    def testMatrixExplicit(self):
        m = Matrix(A=1, B=0, C=0, D=1, physicalLength=1,
                   frontVertex=0, backVertex=0, apertureDiameter=0.5)
        self.assertIsNotNone(m)
        self.assertEqual(m.A, 1)
        self.assertEqual(m.B, 0)
        self.assertEqual(m.C, 0)
        self.assertEqual(m.D, 1)
        self.assertEqual(m.L, 1)
        self.assertEqual(m.backVertex, 0)
        self.assertEqual(m.frontVertex, 0)
        self.assertEqual(m.apertureDiameter, 0.5)

    def testMatrixProductMath(self):
        m1 = Matrix(A=4, B=3, C=1, D=1)
        m2 = Matrix(A=1, B=1, C=3, D=4)
        m3 = m2 * m1
        self.assertEqual(m3.A, 5)
        self.assertEqual(m3.B, 4)
        self.assertEqual(m3.C, 16)
        self.assertEqual(m3.D, 13)

    def testIsIdentity(self):
        m = Matrix()
        self.assertTrue(m.isIdentity)

    def testIsNotIdentity(self):
        m = Matrix(1, 2, 0, 1)
        self.assertFalse(m.isIdentity)

    def testMatrixProductIndicesBoth1(self):
        m1 = Matrix()
        m2 = Matrix()
        m3 = m1 * m2
        self.assertEqual(m3.frontIndex, 1)
        self.assertEqual(m3.backIndex, 1)

    def testMatrixProductIndicesLHSIsIdentity(self):
        m1 = Matrix()
        m2 = Matrix(1, 10, 0, 1, frontIndex=1.5, backIndex=1.5)
        m3 = m1 * m2
        self.assertEqual(m3.frontIndex, 1.5)
        self.assertEqual(m3.backIndex, 1.5)

    def testMatrixProductIndicesRHSIsIdentity(self):
        m1 = Matrix()
        m2 = Matrix(1, 10, 0, 1, frontIndex=1.5, backIndex=1.5)
        m3 = m2 * m1
        self.assertEqual(m3.frontIndex, 1.5)
        self.assertEqual(m3.backIndex, 1.5)

    def testMatrixProductIndicesNoIdentity(self):
        m1 = Matrix(1, 10, 0, 0.7518796992, backIndex=1.33, frontIndex=1)
        m2 = Matrix(1.33, 10, 0, 1, backIndex=1, frontIndex=1.33)
        m3 = m2 * m1
        self.assertEqual(m3.frontIndex, 1)
        self.assertEqual(m3.backIndex, 1)

    def testMatrixProductWithRayMath(self):
        m1 = Matrix(A=1, B=1, C=3, D=4)
        rayIn = Ray(y=1, theta=0.1)
        rayOut = m1 * rayIn
        self.assertEqual(rayOut.y, 1.1)
        self.assertEqual(rayOut.theta, 3.4)

    def testMatrixProductOutputRayLength(self):
        m1 = Matrix(A=1, B=0, C=0, D=1, physicalLength=2)
        rayIn = Ray(y=1, theta=0.1, z=1)
        rayOut = m1 * rayIn
        self.assertEqual(rayOut.z, 2 + 1)

    def testMatrixProductOutputRayAperture(self):
        m1 = Matrix(A=1, B=0, C=0, D=1, physicalLength=2)
        rayIn = Ray(y=1, theta=0.1, z=1)
        rayOut = m1 * rayIn
        self.assertEqual(rayOut.apertureDiameter, inf)

    def testMatrixProductWithRayGoesOverAperture(self):
        m1 = Matrix(A=1, B=0, C=0, D=1, apertureDiameter=10)
        rayIn = Ray(y=6, theta=0.1, z=1)
        rayOut = m1 * rayIn
        self.assertTrue(rayOut.isBlocked)

    def testMatrixProductWithRayGoesUnderAperture(self):
        m1 = Matrix(A=1, B=0, C=0, D=1, apertureDiameter=10)
        rayIn = Ray(y=-6, theta=0.1, z=1)
        rayOut = m1 * rayIn
        self.assertTrue(rayOut.isBlocked)

    def testMatrixProductRayGoesInAperture(self):
        m1 = Matrix(A=1, B=0, C=0, D=1, apertureDiameter=10)
        rayIn = Ray(y=-1, theta=0.1, z=1)
        rayOut = m1 * rayIn
        self.assertFalse(rayOut.isBlocked)

    def testMatrixProductRayAlreadyBlocked(self):
        m1 = Matrix(A=1, B=0, C=0, D=1, apertureDiameter=10)
        rayIn = Ray(y=-1, theta=0.1, z=1, isBlocked=True)
        rayOut = m1 * rayIn
        self.assertTrue(rayOut.isBlocked)

    def testMatrixProductLength(self):
        m1 = Matrix(A=1, B=0, C=0, D=1)
        m2 = Matrix(A=1, B=0, C=0, D=1)
        m3 = m2 * m1
        self.assertEqual(m3.L, m1.L + m2.L)
        self.assertIsNone(m3.frontVertex)
        self.assertIsNone(m3.backVertex)

    def testMatrixProductVertices(self):
        m1 = Matrix(A=1, B=0, C=0, D=1, physicalLength=10, frontVertex=0, backVertex=10)
        self.assertEqual(m1.frontVertex, 0)
        self.assertEqual(m1.backVertex, 10)

    def testMatrixProductVerticesAllNone(self):
        m1 = Matrix(A=1, B=0, C=0, D=1)
        m2 = Matrix(A=1, B=0, C=0, D=1)
        m3 = m2 * m1
        self.assertEqual(m3.L, m1.L + m2.L)
        self.assertIsNone(m3.frontVertex)
        self.assertIsNone(m3.backVertex)

    def testMatrixProductVerticesSecondNone(self):
        m1 = Matrix(A=1, B=0, C=0, D=1, physicalLength=10, frontVertex=0, backVertex=10)
        m2 = Matrix(A=1, B=0, C=0, D=1)
        m3 = m2 * m1
        self.assertEqual(m3.L, m1.L + m2.L)
        self.assertEqual(m3.frontVertex, 0)
        self.assertEqual(m3.backVertex, 10)

    def testMatrixProductVerticesFirstNone(self):
        m1 = Matrix(A=1, B=0, C=0, D=1)
        m2 = Matrix(A=1, B=0, C=0, D=1, physicalLength=10, frontVertex=0, backVertex=10)
        m3 = m2 * m1
        self.assertEqual(m3.L, m1.L + m2.L)
        self.assertEqual(m3.frontVertex, 0)
        self.assertEqual(m3.backVertex, 10)

    def testMatrixProductVerticesTwoElements(self):
        m1 = Matrix(A=1, B=0, C=0, D=1, physicalLength=5, frontVertex=0, backVertex=5)
        m2 = Matrix(A=1, B=0, C=0, D=1, physicalLength=10, frontVertex=0, backVertex=10)
        m3 = m2 * m1
        self.assertEqual(m3.L, m1.L + m2.L)
        self.assertEqual(m3.frontVertex, 0)
        self.assertEqual(m3.backVertex, 15)

    def testMatrixProductVerticesTwoElementsRepresentingGroups(self):
        m1 = Matrix(A=1, B=0, C=0, D=1, physicalLength=5, frontVertex=1, backVertex=4)
        m2 = Matrix(A=1, B=0, C=0, D=1, physicalLength=10, frontVertex=2, backVertex=9)
        m3 = m2 * m1
        self.assertEqual(m3.L, m1.L + m2.L)
        self.assertEqual(m3.frontVertex, 1)
        self.assertEqual(m3.backVertex, 14)

        m3 = m1 * m2
        self.assertEqual(m3.L, m1.L + m2.L)
        self.assertEqual(m3.frontVertex, 2)
        self.assertEqual(m3.backVertex, 14)

    def testMatrixProductGaussianBeamMath(self):
        m = Matrix(A=2, B=1, C=3, D=2)
        beamIn = GaussianBeam(w=1, wavelength=1)  # q = j*pi
        beamOut = m * beamIn
        self.assertEqual(beamOut.q, (2j * pi + 1) / (3j * pi + 2))

    def testMatrixProductGaussianNotSameRefractionIndex(self):
        m = Matrix(A=1, B=0, C=0, D=1)
        beam = GaussianBeam(w=1, n=1.2)

        with self.assertRaises(RuntimeError):
            m * beam

    def testMatrixProductGaussianBeamWavelengthOut(self):
        m = Matrix(A=1, B=0, C=0, D=1, )
        beamIn = GaussianBeam(w=1, wavelength=1)
        beamOut = m * beamIn
        self.assertEqual(beamOut.wavelength, 1)

    def testMatrixProductGaussianRefractIndexOut(self):
        m = Matrix(A=1, B=0, C=0, D=1, frontIndex=1.33, backIndex=1.33)
        beamIn = GaussianBeam(w=1, wavelength=1, n=1.33)
        beamOut = m * beamIn
        self.assertEqual(beamOut.n, 1.33)

    def testMatrixProductGaussianLength(self):
        m = Matrix(A=1, B=0, C=0, D=1.33, frontIndex=1.33, physicalLength=1.2)
        beamIn = GaussianBeam(w=1, wavelength=1, z=1, n=1.33)
        beamOut = m * beamIn
        self.assertEqual(beamOut.z, 2.2)

    def testMatrixProductGaussianClippedOverAperture(self):
        m = Matrix(A=1, B=0, C=0, D=1, physicalLength=1.2, apertureDiameter=2)
        beamIn = GaussianBeam(w=1.1, wavelength=1, z=1)
        beamOut = m * beamIn
        self.assertTrue(beamOut.isClipped)

    def testMatrixProductGaussianInitiallyClipped(self):
        m = Matrix(A=1, B=0, C=0, D=1, physicalLength=1.2, apertureDiameter=2)
        beamIn = GaussianBeam(w=0.5, wavelength=1, z=1)
        beamIn.isClipped = True
        beamOut = m * beamIn
        self.assertTrue(beamOut.isClipped)

    def testMatrixProductGaussianNotClipped(self):
        m = Matrix(A=1, B=0, C=0, D=1, physicalLength=1.2)
        beamIn = GaussianBeam(w=1.1, wavelength=1, z=1)
        beamOut = m * beamIn
        self.assertFalse(beamOut.isClipped)

    def testMatrixProductUnknownRightSide(self):
        m = Matrix()
        other = TypeError
        with self.assertRaises(TypeError):
            m * other

    def testApertureDiameter(self):
        m1 = Matrix(A=1, B=0, C=0, D=1, apertureDiameter=2)
        self.assertTrue(m1.hasFiniteApertureDiameter())
        self.assertEqual(m1.largestDiameter, 2.0)
        m2 = Matrix(A=1, B=0, C=0, D=1)
        self.assertFalse(m2.hasFiniteApertureDiameter())
        self.assertEqual(m2.largestDiameter, float("+inf"))

    def testTransferMatrix(self):
        m1 = Matrix(A=1, B=0, C=0, D=1)
        # Null length returns self
        self.assertEqual(m1.transferMatrix(), m1)

        # Length == 1 returns self if upTo >= 1
        m2 = Matrix(A=1, B=0, C=0, D=1, physicalLength=1)
        self.assertEqual(m2.transferMatrix(upTo=1), m2)
        self.assertEqual(m2.transferMatrix(upTo=2), m2)

        # Length == 1 raises exception if upTo<1: can't do partial
        # Subclasses Space() and DielectricSlab() can handle this
        # (not the generic matrix).
        with self.assertRaises(Exception) as context:
            m2.transferMatrix(upTo=0.5)

    def testTransferMatrices(self):
        m1 = Matrix(A=1, B=0, C=0, D=2, frontIndex=2)
        self.assertEqual(m1.transferMatrices(), [m1])

    def testTrace(self):
        ray = Ray(y=1, theta=1)
        m = Matrix(A=1, B=0, C=0, D=1, physicalLength=1)
        trace = [ray, m * ray]
        self.assertListEqual(m.trace(ray), trace)

    def testTraceNullLength(self):
        ray = Ray(y=1, theta=1)
        m = Matrix(A=1, B=0, C=0, D=1)
        trace = [m * ray]
        self.assertListEqual(m.trace(ray), trace)

    def testTraceBlocked(self):
        ray = Ray(y=10, theta=1)
        m = Matrix(A=1, B=0, C=0, D=1, apertureDiameter=10, physicalLength=1)
        trace = m.trace(ray)
        self.assertTrue(all(x.isBlocked for x in trace))

    def testTraceGaussianBeam(self):
        beam = GaussianBeam(w=1)
        m = Matrix(A=1, B=0, C=0, D=1, apertureDiameter=10)
        outputBeam = m * beam
        tracedBeam = m.trace(beam)[-1]
        self.assertEqual(tracedBeam.w, outputBeam.w)
        self.assertEqual(tracedBeam.q, outputBeam.q)
        self.assertEqual(tracedBeam.z, outputBeam.z)
        self.assertEqual(tracedBeam.n, outputBeam.n)
        self.assertEqual(tracedBeam.isClipped, outputBeam.isClipped)

    def testTraceThrough(self):
        ray = Ray()
        m = Matrix(A=1, B=0, C=0, D=1, apertureDiameter=10)
        trace = m.traceThrough(ray)
        self.assertEqual(trace, m * ray)

    def testTraceMany(self):
        rays = [Ray(y, theta) for y, theta in zip(range(10, 20), range(10))]
        m = Matrix(physicalLength=1.01)
        traceMany = [[ray, ray] for ray in rays]
        self.assertListEqual(m.traceMany(rays), traceMany)

    def testTraceManyJustOne(self):
        rays = [Ray()]
        m = Matrix(physicalLength=1e-9)
        traceMany = [rays * 2]
        self.assertListEqual(m.traceMany(rays), traceMany)

    def testTraceManyThroughIterable(self):
        rays = [Ray(y, y) for y in range(10)]
        m = Matrix(physicalLength=1)
        iterable = tuple(rays)
        raysObj = Rays(iterable)

        traceManyThroughList = m.traceManyThrough(rays)
        traceManyThroughTuple = m.traceManyThrough(iterable)
        traceManyThroughRays = m.traceManyThrough(raysObj)
        for i in range(len(rays)):
            self.assertEqual(rays[i], traceManyThroughList[i])
            self.assertEqual(rays[i], traceManyThroughTuple[i])
            self.assertEqual(rays[i], traceManyThroughRays[i])

    def testTraceManyThroughNotIterable(self):
        with self.assertRaises(TypeError):
            m = Matrix()
            m.traceManyThrough(self.assertIs)

    def testTraceManyThroughOutput(self):
        rays = [Ray(y, y) for y in range(10_000)]
        m = Matrix(physicalLength=1)
        self.assertPrints(m.traceManyThrough, "Progress 10000/10000 (100%)", inputRays=rays, progress=True)

    def testTraceManyThroughNoOutput(self):
        rays = [Ray(y, y) for y in range(10_000)]
        m = Matrix(physicalLength=1)
        self.assertPrints(m.traceManyThrough, "", inputRays=rays, progress=False)

    def testTraceManyThroughLastRayBlocked(self):
        m = Matrix()
        rays = Rays([Ray(), Ray(-1, -1)])
        rays[-1].isBlocked = True
        traceManyThrough = m.traceManyThrough(rays)
        # One less ray, because last is blocked
        self.assertEqual(len(traceManyThrough), len(rays) - 1)

    @envtest.skipIf(sys.platform == 'darwin' and sys.version_info.major == 3 and sys.version_info.minor <= 7,
                    "Endless loop on macOS")
    # Some information here: https://github.com/gammapy/gammapy/issues/2453
    def testTraceManyThroughInParallel(self):
        rays = [Ray(y, y) for y in range(5)]
        m = Matrix(physicalLength=1)
        trace = self.assertDoesNotRaise(m.traceManyThroughInParallel, None, rays)
        for i in range(len(rays)):
            # Order is not kept, we have to check if the ray traced is in the original list
            self.assertIn(trace[i], rays)

    @envtest.skipIf(sys.platform == 'darwin' and sys.version_info.major == 3 and sys.version_info.minor <= 7,
                    "Endless loop on macOS")
    # Some information here: https://github.com/gammapy/gammapy/issues/2453
    def testTraceManyThroughInParallel(self):
        rays = [Ray(y, y) for y in range(5)]
        m = Matrix(physicalLength=1)
        trace = self.assertDoesNotRaise(m.traceManyThroughInParallel, None, rays, processes=2)
        for i in range(len(rays)):
            # Order is not kept, we have to check if the ray traced is in the original list
            self.assertIn(trace[i], rays)

    @envtest.skipIf(sys.platform == 'darwin' and sys.version_info.major == 3 and sys.version_info.minor <= 7,
                    "Endless loop on macOS")
    # Some information here: https://github.com/gammapy/gammapy/issues/2453
    def testTraceManyThroughInParallelNoOutput(self):
        processComplete = subprocess.run([sys.executable, "traceManyThroughInParallelNoOutput.py"], capture_output=True,
                                         universal_newlines=True)
        self.assertEqual(processComplete.stdout, "")

    @envtest.skipIf(sys.platform == 'darwin' and sys.version_info.major == 3 and sys.version_info.minor <= 7,
                    "Endless loop on macOS")
    # Some information here: https://github.com/gammapy/gammapy/issues/2453
    def testTraceManyThroughInParallelWithOutput(self):
        processComplete = subprocess.run([sys.executable, "traceManyThroughInParallelWithOutput.py"],
                                         capture_output=True, universal_newlines=True)
        self.assertEqual(processComplete.stdout.strip(), "Progress 10000/10000 (100%) \nProgress 10000/10000 (100%)")

    def testPointsOfInterest(self):
        m = Matrix()
        self.assertListEqual(m.pointsOfInterest(1), [])

    def testIsImaging(self):
        m = Matrix(A=1, B=0, C=3, D=1)
        self.assertTrue(m.isImaging)

    def testIsNotImaging(self):
        m = Matrix(A=1, B=1, C=3, D=4)
        self.assertFalse(m.isImaging)

    def testOpticalInvariantSpace(self):
        m = Space(d=10)
        self.assertIsNotNone(m)
        before = m.opticalInvariant(z=0, ray1=Ray(1, 2), ray2=Ray(2, 1))
        after = m.opticalInvariant(z=10, ray1=Ray(1, 2), ray2=Ray(2, 1))
        self.assertAlmostEqual(before, after)

    def testHasNoPower(self):
        f1 = 1.0000000000000017
        f2 = 2.05 * f1

        # This simulates a 4f system (since we test Matrix, we should only use basic matrices)
        m = Matrix(1, f1, 0, 1) * Matrix(1, 0, -1 / f1, 1) * Matrix(1, f1, 0, 1) * Matrix(1, f2, 0, 1)
        m = m * Matrix(1, 0, -1 / f2, 1) * Matrix(1, f1, 0, 1)
        self.assertFalse(m.hasPower)

    def testEffectiveFocalLengthsHasPower(self):
        m = Matrix(A=1, B=0, C=3, D=1)
        focalLengths = (-1 / 3, -1 / 3)
        self.assertTupleEqual(m.effectiveFocalLengths(), focalLengths)

    def testEffectiveFocalIsNamedTuple(self):
        m = Matrix(A=1, B=0, C=3, D=1)
        focalLengths = (-1 / 3, -1 / 3)

        actualFocalLengths = m.effectiveFocalLengths() 
        self.assertEqual(actualFocalLengths.f1, focalLengths[0])
        self.assertEqual(actualFocalLengths.f2, focalLengths[0])

    def testEffectiveFocalIsNamedTuple(self):
        m = Matrix(A=1, B=0, C=3, D=1)

        focalLengths = FocalLengths(f1=-1 / 3, f2=-1 / 3)
        self.assertEqual(focalLengths.f1, -1/3)
        self.assertEqual(focalLengths.f2, -1/3)


    def testEffectiveFocalLengthsNoPower(self):
        m = Matrix(1, 0, 0, 1)
        focalLengths = (inf, inf)
        self.assertTupleEqual(m.effectiveFocalLengths(), focalLengths)

    def testMatrixBackFocalLength(self):
        R = 10
        n1 = 1.2
        n2 = 1.5
        m = DielectricInterface(n1=n1, n2=n2, R=R)
        self.assertAlmostEqual(m.backFocalLength(), -m.A / m.C)

    def testBackFocalLengthSupposedNone(self):
        m = Matrix()
        self.assertIsNone(m.backFocalLength())

    def testMatrixFrontFocalLength(self):
        R = 10
        n1 = 1.2
        n2 = 1.5
        m = DielectricInterface(n1=n1, n2=n2, R=R)
        self.assertAlmostEqual(m.frontFocalLength(), -m.D / m.C)

    def testFrontFocalLengthSupposedNone(self):
        m = Matrix()
        self.assertIsNone(m.frontFocalLength())

    def testPrincipalPlanePositions(self):
        m = Matrix(A=1, B=0, C=1, D=1, physicalLength=1)
        p1 = 0
        p2 = 1
        self.assertTupleEqual(m.principalPlanePositions(0), (p1, p2))

    def testPrincipalPlanePositionsIsNamedTuple(self):
        m = Matrix(A=1, B=0, C=1, D=1, physicalLength=1)
        p1 = 0
        p2 = 1
        self.assertEqual(m.principalPlanePositions(0).z1, p1)
        self.assertEqual(m.principalPlanePositions(0).z2, p2)

    def testPrincipalPlanePositionsNoPower(self):
        m = Matrix()
        self.assertTupleEqual(m.principalPlanePositions(0), (None, None))

    def testFocusPositions(self):
        m = Matrix(A=1 / 3, B=0, C=10, D=3, physicalLength=1)
        f1 = -0.1
        p1 = 0.2
        f2 = -0.1
        p2 = 16 / 15
        self.assertTupleEqual(m.focusPositions(0), (p1 - f1, p2 + f2))

    def testFocusPositionsIsNamedTuple(self):
        m = Matrix(A=1 / 3, B=0, C=10, D=3, physicalLength=1)
        f1 = -0.1
        p1 = 0.2
        f2 = -0.1
        p2 = 16 / 15
        self.assertEqual(m.focusPositions(0).z1, p1 - f1)
        self.assertEqual(m.focusPositions(0).z2, p2 + f2)

    def testFocusPositionsNoPower(self):
        m = Matrix()
        self.assertTupleEqual(m.focusPositions(0), (None, None))

    def testDielectricInterfaceEffectiveFocalLengths(self):
        # Positive R is convex for ray
        n1 = 1
        n2 = 1.5
        R = 10
        m = DielectricInterface(n1=n1, n2=n2, R=R)
        (f1, f2) = m.effectiveFocalLengths()
        self.assertTrue(f2 == n2 * R / (n2 - n1))
        self.assertTrue(f1 == n1 * R / (n2 - n1))  # flip R and n1,n2

    def testFiniteForwardConjugate(self):
        m1 = Lens(f=5) * Space(d=10)
        (d, m2) = m1.forwardConjugate()
        self.assertTrue(m2.isImaging)
        self.assertEqual(d, 10)
        self.assertEqual(m1.determinant, 1)
        self.assertEqual(m2.determinant, 1)

    def testForwardConjugateIsNamedTuple(self):
        m1 = Lens(f=5) * Space(d=10)
        conjugate = m1.forwardConjugate()
        self.assertEqual(conjugate.d, 10)
        self.assertIsNotNone(conjugate.transferMatrix)

    def testFiniteForwardConjugates_2(self):
        m1 = Matrix(1, 5, 0, 1) * Matrix(1, 0, -1 / 5, 1) * Matrix(1, 10, 0, 1)
        (d, m2) = m1.forwardConjugate()
        self.assertTrue(m2.isImaging)
        self.assertEqual(d, 5)
        self.assertEqual(m2.determinant, 1)

    def testInfiniteForwardConjugate(self):
        m1 = Matrix(1, 0, -1 / 5, 1) * Matrix(1, 5, 0, 1)
        (d, m2) = m1.forwardConjugate()
        self.assertIsNone(m2)
        self.assertEqual(d, inf)
        self.assertEqual(m1.determinant, 1)

    def testInfiniteBackConjugate(self):
        m = Matrix(A=0, B=1, C=-1, D=0)
        d, mat = m.backwardConjugate()
        self.assertEqual(d, inf)
        self.assertIsNotNone(mat)


    def testBackConjugateIsNamedTuple(self):
        m = Matrix(A=0, B=1, C=-1, D=0)
        conjugate = m.backwardConjugate()
        self.assertEqual(conjugate.d, inf)
        self.assertIsNotNone(conjugate.transferMatrix)

    def testFiniteBackConjugate_1(self):
        m1 = Matrix(1, 10, 0, 1) * Matrix(1, 0, -1 / 5, 1)
        (d, m2) = m1.backwardConjugate()
        self.assertTrue(m2.isImaging)
        self.assertEqual(d, 10)
        self.assertEqual(m1.determinant, 1)
        self.assertEqual(m2.determinant, 1)

    def testFiniteBackConjugate_2(self):
        m1 = Matrix(1, 10, 0, 1) * Matrix(1, 0, -1 / 5, 1) * Matrix(1, 5, 0, 1)
        (d, m2) = m1.backwardConjugate()
        self.assertTrue(m2.isImaging)
        self.assertEqual(d, 5)
        self.assertEqual(m1.determinant, 1)
        self.assertEqual(m2.determinant, 1)

    def testMagnificationImaging(self):
        m = Matrix()
        self.assertTupleEqual(m.magnification(), (1, 1))

    def testMagnificationNamedTupleImaging(self):
        m = Matrix()
        mag = m.magnification()
        self.assertAlmostEqual(mag.transverse, 1)
        self.assertAlmostEqual(mag.angular, 1)

    def testMagnificationNotImaging(self):
        m = Matrix(B=1)
        self.assertTupleEqual(m.magnification(), (None, None))

    def testMatrixFlipOrientation(self):
        frontVertexInit = 10
        backVertexInit = 20
        frontIndexInit = 1
        backIndexInit = 2
        m = Matrix(A=0.5, frontVertex=frontVertexInit, backVertex=backVertexInit, frontIndex=frontIndexInit,
                   backIndex=backIndexInit)
        m.flipOrientation()
        self.assertTrue(m.isFlipped)
        self.assertEqual(m.backIndex, frontIndexInit)
        self.assertEqual(m.frontIndex, backIndexInit)
        self.assertEqual(m.frontVertex, backVertexInit)
        self.assertEqual(m.backVertex, frontVertexInit)

    def testStrRepresentation(self):
        m = Matrix(C=1)
        strRepresentation = r""" |  1.000    0.000 |
|                 |
|  1.000    1.000 |
f=-1.000
"""
        self.assertEqual(str(m).strip(), strRepresentation.strip())

    def testStrRepresentationAfocal(self):
        m = Matrix()
        strRepresentation = r""" |  1.000    0.000 |
|                 |
|  0.000    1.000 |
f = +inf (afocal)
"""
        self.assertEqual(str(m).strip(), strRepresentation.strip())

    def testDisplayHalfHeight(self):
        m = Matrix(apertureDiameter=10)
        self.assertEqual(m.displayHalfHeight(), m.apertureDiameter / 2)

    def testDisplayHalfHeightInfiniteDiameter(self):
        m = Matrix(apertureDiameter=inf)
        self.assertEqual(m.displayHalfHeight(), 4)

    def testEqualityNotSameClassInstance(self):
        m = Matrix()
        self.assertNotEqual(m, 10)
        self.assertNotEqual(m, Ray())
        self.assertNotEqual(m, "Trust me, this is a Matrix. This is equal to Matrix()")

    def testEqualityMatricesNotEqualSameABCD(self):
        m = Matrix(1, 0, 0, 1)
        m2 = Matrix(1, 0, 0, 1, frontVertex=1)
        self.assertNotEqual(m, m2)
        m2 = Matrix(1, 0, 0, 1, backVertex=1)
        self.assertNotEqual(m, m2)
        m2 = Matrix(1, 0, 0, 1, frontIndex=10, backIndex=10)
        self.assertNotEqual(m, m2)

    def testEqualityMatricesNotEqualDifferentABCD(self):
        m = Matrix(1, 0, 0, 1)
        m2 = Matrix(A=1 / 2, D=2)
        self.assertNotEqual(m, m2)

    def testEqualityMatricesAreEqual(self):
        m = Matrix()
        m2 = Matrix()
        self.assertEqual(m, m2)

    def testEqualityMatrixAndSpaceEqual(self):
        d = 10
        m = Matrix(B=d, physicalLength=d)
        space = Space(d)
        self.assertEqual(m, space)


if __name__ == '__main__':
    envtest.main()
