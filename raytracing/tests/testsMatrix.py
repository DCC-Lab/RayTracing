import unittest
import envtest  # modifies path

from raytracing import *

inf = float("+inf")


class TestMatrix(unittest.TestCase):
    def testWarningsFormat(self):
        message = "This is a test."
        filename = "test.py"
        lineno = 10
        category = UserWarning
        warningsMessage = warningLineFormat(message, category, filename, lineno)
        self.assertEqual(warningsMessage, "\ntest.py:10\nUserWarning:This is a test.\n")

    def testMatrix(self):
        m = Matrix()
        self.assertIsNotNone(m)

    def testMatrixExplicit(self):
        m = Matrix(A=1, B=2, C=3, D=4, physicalLength=1,
                   frontVertex=0, backVertex=0, apertureDiameter=1.0)
        self.assertIsNotNone(m)
        self.assertEqual(m.A, 1)
        self.assertEqual(m.B, 2)
        self.assertEqual(m.C, 3)
        self.assertEqual(m.D, 4)

    def testMatrixProductMath(self):
        m1 = Matrix(A=1, B=2, C=3, D=4)
        m2 = Matrix(A=5, B=6, C=7, D=8)
        m3 = m2 * m1
        self.assertEqual(m3.A, 1 * 5 + 3 * 6)
        self.assertEqual(m3.B, 2 * 5 + 4 * 6)
        self.assertEqual(m3.C, 1 * 7 + 3 * 8)
        self.assertEqual(m3.D, 2 * 7 + 4 * 8)

    def testMatrixProductWithRayMath(self):
        m1 = Matrix(A=1, B=2, C=3, D=4)
        rayIn = Ray(y=1, theta=0.1)
        rayOut = m1 * rayIn
        self.assertEqual(rayOut.y, 1 * 1 + 2 * 0.1)
        self.assertEqual(rayOut.theta, 3 * 1 + 4 * 0.1)

    def testMatrixProductOutpuRayLength(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, physicalLength=2)
        rayIn = Ray(y=1, theta=0.1, z=1)
        rayOut = m1 * rayIn
        self.assertEqual(rayOut.z, 2 + 1)

    def testMatrixProductOutputRayAperture(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, physicalLength=2)
        rayIn = Ray(y=1, theta=0.1, z=1)
        rayOut = m1 * rayIn
        self.assertEqual(rayOut.apertureDiameter, inf)

    def testMatrixProductWithRayGoesOverAperture(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, apertureDiameter=10)
        rayIn = Ray(y=6, theta=0.1, z=1)
        rayOut = m1 * rayIn
        self.assertTrue(rayOut.isBlocked)

    def testMatrixProductWithRayGoesUnderAperture(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, apertureDiameter=10)
        rayIn = Ray(y=-6, theta=0.1, z=1)
        rayOut = m1 * rayIn
        self.assertTrue(rayOut.isBlocked)

    def testMatrixProductRayGoesInAperture(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, apertureDiameter=10)
        rayIn = Ray(y=-1, theta=0.1, z=1)
        rayOut = m1 * rayIn
        self.assertFalse(rayOut.isBlocked)

    def testMatrixProductRayAlreadyBlocked(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, apertureDiameter=10)
        rayIn = Ray(y=-1, theta=0.1, z=1, isBlocked=True)
        rayOut = m1 * rayIn
        self.assertTrue(rayOut.isBlocked)

    def testMatrixProductLength(self):
        m1 = Matrix(A=1, B=2, C=3, D=4)
        m2 = Matrix(A=5, B=6, C=7, D=8)
        m3 = m2 * m1
        self.assertEqual(m3.L, m1.L + m2.L)
        self.assertIsNone(m3.frontVertex)
        self.assertIsNone(m3.backVertex)

    def testMatrixProductVertices(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, physicalLength=10, frontVertex=0, backVertex=10)
        self.assertEqual(m1.frontVertex, 0)
        self.assertEqual(m1.backVertex, 10)

    def testMatrixProductVerticesAllNone(self):
        m1 = Matrix(A=1, B=2, C=3, D=4)
        m2 = Matrix(A=5, B=6, C=7, D=8)
        m3 = m2 * m1
        self.assertEqual(m3.L, m1.L + m2.L)
        self.assertIsNone(m3.frontVertex)
        self.assertIsNone(m3.backVertex)

    def testMatrixProductVerticesSecondNone(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, physicalLength=10, frontVertex=0, backVertex=10)
        m2 = Matrix(A=5, B=6, C=7, D=8)
        m3 = m2 * m1
        self.assertEqual(m3.L, m1.L + m2.L)
        self.assertEqual(m3.frontVertex, 0)
        self.assertEqual(m3.backVertex, 10)

    def testMatrixProductVerticesFirstNone(self):
        m1 = Matrix(A=1, B=2, C=3, D=4)
        m2 = Matrix(A=5, B=6, C=7, D=8, physicalLength=10, frontVertex=0, backVertex=10)
        m3 = m2 * m1
        self.assertEqual(m3.L, m1.L + m2.L)
        self.assertEqual(m3.frontVertex, 0)
        self.assertEqual(m3.backVertex, 10)

    def testMatrixProductVerticesTwoElements(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, physicalLength=5, frontVertex=0, backVertex=5)
        m2 = Matrix(A=5, B=6, C=7, D=8, physicalLength=10, frontVertex=0, backVertex=10)
        m3 = m2 * m1
        self.assertEqual(m3.L, m1.L + m2.L)
        self.assertEqual(m3.frontVertex, 0)
        self.assertEqual(m3.backVertex, 15)

    def testMatrixProductVerticesTwoElementsRepresentingGroups(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, physicalLength=5, frontVertex=1, backVertex=4)
        m2 = Matrix(A=5, B=6, C=7, D=8, physicalLength=10, frontVertex=2, backVertex=9)
        m3 = m2 * m1
        self.assertEqual(m3.L, m1.L + m2.L)
        self.assertEqual(m3.frontVertex, 1)
        self.assertEqual(m3.backVertex, 14)

        m3 = m1 * m2
        self.assertEqual(m3.L, m1.L + m2.L)
        self.assertEqual(m3.frontVertex, 2)
        self.assertEqual(m3.backVertex, 14)

    def testMatrixProductGaussianBeamMath(self):
        m = Matrix(A=1, B=2, C=3, D=4)
        beamIn = GaussianBeam(w=1, wavelength=1)  # q = j\pi
        beamOut = m * beamIn
        q = complex(0, math.pi)
        self.assertEqual(beamOut.q, (1 * q + 2) / (3 * q + 4))

    def testMatrixProductGaussianNotSameRefractionIndex(self):
        m = Matrix(A=1, B=2, C=3, D=4)
        beam = GaussianBeam(w=1, n=1.2)

        with self.assertRaises(UserWarning):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("error")
                m * beam

    def testMatrixProductGaussianBeamWavelengthOut(self):
        m = Matrix(A=1, B=2, C=3, D=4, )
        beamIn = GaussianBeam(w=1, wavelength=1)
        beamOut = m * beamIn
        self.assertEqual(beamOut.wavelength, 1)

    def testMatrixProductGaussianRefractIndexOut(self):
        m = Matrix(A=1, B=2, C=3, D=4, frontIndex=1.33, backIndex=1.33)
        beamIn = GaussianBeam(w=1, wavelength=1, n=1.33)
        beamOut = m * beamIn
        self.assertEqual(beamOut.n, 1.33)

    def testMatrixProductGaussianLength(self):
        m = Matrix(A=1, B=2, C=3, D=4, frontIndex=1.33, physicalLength=1.2)
        beamIn = GaussianBeam(w=1, wavelength=1, z=1, n=1.33)
        beamOut = m * beamIn
        self.assertEqual(beamOut.z, 2.2)

    def testMatrixProductGaussianClippedOverAperture(self):
        m = Matrix(A=1, B=2, C=3, D=4, physicalLength=1.2, apertureDiameter=2)
        beamIn = GaussianBeam(w=1.1, wavelength=1, z=1)
        beamOut = m * beamIn
        self.assertTrue(beamOut.isClipped)

    def testMatrixProductGaussianInitiallyClipped(self):
        m = Matrix(A=1, B=2, C=3, D=4, physicalLength=1.2, apertureDiameter=2)
        beamIn = GaussianBeam(w=0.5, wavelength=1, z=1)
        beamIn.isClipped = True
        beamOut = m * beamIn
        self.assertTrue(beamOut.isClipped)

    def testMatrixProductGaussianNotClipped(self):
        m = Matrix(A=1, B=2, C=3, D=4, physicalLength=1.2)
        beamIn = GaussianBeam(w=1.1, wavelength=1, z=1)
        beamOut = m * beamIn
        self.assertFalse(beamOut.isClipped)

    def testMatrixProductUnknownRightSide(self):
        m = Matrix()
        other = TypeError
        with self.assertRaises(TypeError):
            m * other

    def testApertureDiameter(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, apertureDiameter=2)
        self.assertTrue(m1.hasFiniteApertureDiameter())
        self.assertEqual(m1.largestDiameter, 2.0)
        m2 = Matrix(A=1, B=2, C=3, D=4)
        self.assertFalse(m2.hasFiniteApertureDiameter())
        self.assertEqual(m2.largestDiameter, float("+inf"))

    def testTransferMatrix(self):
        m1 = Matrix(A=1, B=2, C=3, D=4)
        # Null length returns self
        self.assertEqual(m1.transferMatrix(), m1)

        # Length == 1 returns self if upTo >= 1
        m2 = Matrix(A=1, B=2, C=3, D=4, physicalLength=1)
        self.assertEqual(m2.transferMatrix(upTo=1), m2)
        self.assertEqual(m2.transferMatrix(upTo=2), m2)

        # Length == 1 raises exception if upTo<1: can't do partial
        # Subclasses Space() and DielectricSlab() can handle this
        # (not the generic matrix).
        with self.assertRaises(Exception) as context:
            m2.transferMatrix(upTo=0.5)

    def testTransferMatrices(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, frontIndex=2)
        self.assertEqual(m1.transferMatrices(), [m1])
        m1 * GaussianBeam(w=1, n=2)

    def testTrace(self):
        ray = Ray(y=1, theta=1)
        m = Matrix(A=1, B=2, C=3, D=4, physicalLength=1)
        trace = [ray, m * ray]
        self.assertListEqual(m.trace(ray), trace)

    def testTraceNullLength(self):
        ray = Ray(y=1, theta=1)
        m = Matrix(A=1, B=2, C=3, D=4)
        trace = [m * ray]
        self.assertListEqual(m.trace(ray), trace)

    def testTraceBlocked(self):
        ray = Ray(y=10, theta=1)
        m = Matrix(A=1, B=2, C=3, D=4, apertureDiameter=10, physicalLength=1)
        trace = m.trace(ray)
        self.assertTrue(all(x.isBlocked for x in trace))

    def testTraceGaussianBeam(self):
        beam = GaussianBeam(w=1)
        m = Matrix(A=1, B=2, C=3, D=4, apertureDiameter=10)
        outputBeam = m * beam
        tracedBeam = m.trace(beam)[-1]
        self.assertEqual(tracedBeam.w, outputBeam.w)
        self.assertEqual(tracedBeam.q, outputBeam.q)
        self.assertEqual(tracedBeam.z, outputBeam.z)
        self.assertEqual(tracedBeam.n, outputBeam.n)
        self.assertEqual(tracedBeam.isClipped, outputBeam.isClipped)

    def testTraceThrough(self):
        ray = Ray()
        m = Matrix(A=1, B=2, C=3, D=4, apertureDiameter=10)
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
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            rays = [Ray(y, y) for y in range(10_000)]
            m = Matrix(physicalLength=1)
            m.traceManyThrough(rays, True)
        out = f.getvalue()
        self.assertEqual(out.strip(), "Progress 10000/10000 (100%)")

    def testTraceManyThroughNoOutput(self):
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            rays = [Ray(y, y) for y in range(10_000)]
            m = Matrix(physicalLength=1)
            m.traceManyThrough(rays, False)
        out = f.getvalue()
        self.assertEqual(out.strip(), "")

    def testTraceManyThroughLastRayBlocked(self):
        m = Matrix()
        rays = Rays([Ray(), Ray(-1, -1)])
        rays[-1].isBlocked = True
        traceManyThrough = m.traceManyThrough(rays)
        # One less ray, because last is blocked
        self.assertEqual(len(traceManyThrough), len(rays) - 1)

    def testTraceManyThroughInParallel(self):
        rays = [Ray(y, y) for y in range(5)]
        m = Matrix(physicalLength=1)
        trace = m.traceManyThroughInParallel(rays)
        traceWithNumberProcesses = m.traceManyThroughInParallel(rays, processes=2)
        for i in range(len(rays)):
            # Order is not kept, we have to check if the ray traced is in the original list
            self.assertTrue(trace[i] in rays)
            self.assertTrue(traceWithNumberProcesses[i] in rays)

    def testPointsOfInterest(self):
        m = Matrix()
        self.assertListEqual(m.pointsOfInterest(1), [])

    def testIsImaging(self):
        m1 = Matrix(A=1, B=0, C=3, D=4)
        self.assertTrue(m1.isImaging)
        m2 = Matrix(A=1, B=1, C=3, D=4)
        self.assertFalse(m2.isImaging)

    def testEffectiveFocalLengthsHasPower(self):
        m = Matrix(1, 2, 3, 4)
        focalLengths = (-1 / 3, -1 / 3)
        self.assertTupleEqual(m.effectiveFocalLengths(), focalLengths)

    def testEffectiveFocalLengthsNoPower(self):
        m = Matrix()
        focalLengths = (inf, inf)
        self.assertTupleEqual(m.effectiveFocalLengths(), focalLengths)

    def testMatrixBackFocalLength(self):
        m = Matrix(1, 2, 3, 4, backVertex=1, physicalLength=1)
        f2 = -1 / 3
        p2 = 0 + 1 + (1 - 1) / 3
        self.assertEqual(m.backFocalLength(), p2 + f2 - 1)

    def testBackFocalLengthSupposedNone(self):
        m = Matrix()
        self.assertIsNone(m.backFocalLength())

    def testMatrixFrontFocalLength(self):
        m = Matrix(1, 2, 3, 4, frontVertex=1, physicalLength=1)
        f1 = -1 / 3
        p1 = 0 - (1 - 4) / 3
        self.assertEqual(m.frontFocalLength(), -(p1 - f1 - 1))

    def testFrontFocalLengthSupposedNone(self):
        m = Matrix()
        self.assertIsNone(m.frontFocalLength())

    def testPrincipalPlanePositions(self):
        m = Matrix(1, 2, 3, 4, physicalLength=1)
        p1 = 0 - (1 - 4) / 3
        p2 = 0 + 1 + (1 - 1) / 3
        self.assertTupleEqual(m.principalPlanePositions(0), (p1, p2))

    def testPrincipalPlanePositionsNoPower(self):
        m = Matrix()
        self.assertTupleEqual(m.principalPlanePositions(0), (None, None))

    def testFocusPositions(self):
        m = Matrix(1, 2, 3, 4, physicalLength=1)
        f1 = -1 / 3
        p1 = 1
        f2 = -1 / 3
        p2 = 1
        self.assertTupleEqual(m.focusPositions(0), (p1 - f1, p2 + f2))

    def testFocusPositionsNoPower(self):
        m = Matrix()
        self.assertTupleEqual(m.focusPositions(0), (None, None))

    def testFiniteForwardConjugate(self):
        m1 = Lens(f=5) * Space(d=10)
        (d, m2) = m1.forwardConjugate()
        self.assertTrue(m2.isImaging)
        self.assertEqual(d, 10)
        self.assertEqual(m1.determinant, 1)
        self.assertEqual(m2.determinant, 1)

        m1 = Space(d=5) * Lens(f=5) * Space(d=10)
        (d, m2) = m1.forwardConjugate()
        self.assertTrue(m2.isImaging)
        self.assertEqual(d, 5)
        self.assertEqual(m2.determinant, 1)

    def testInfiniteForwardConjugate(self):
        m1 = Lens(f=5) * Space(d=5)
        (d, m2) = m1.forwardConjugate()
        self.assertIsNone(m2)
        self.assertEqual(d, float("+inf"))
        self.assertEqual(m1.determinant, 1)

    def testInfiniteBackConjugate(self):
        m = Matrix(A=0)
        self.assertTupleEqual(m.backwardConjugate(), (float("+inf"), None))

    def testFiniteBackConjugate(self):
        m1 = Space(d=10) * Lens(f=5)
        (d, m2) = m1.backwardConjugate()
        self.assertTrue(m2.isImaging)
        self.assertEqual(d, 10)
        self.assertEqual(m1.determinant, 1)
        self.assertEqual(m2.determinant, 1)

        m1 = Space(d=10) * Lens(f=5) * Space(d=5)
        (d, m2) = m1.backwardConjugate()
        self.assertTrue(m2.isImaging)
        self.assertEqual(d, 5)
        self.assertEqual(m1.determinant, 1)
        self.assertEqual(m2.determinant, 1)

    def testMagnificationImaging(self):
        m = Matrix()
        self.assertTupleEqual(m.magnification(), (1, 1))

    def testMagnificationNotImaging(self):
        m = Matrix(B=1)
        self.assertTupleEqual(m.magnification(), (None, None))

    def testMatrixFlipOrientation(self):
        frontVertexInit = 10
        backVertexInit = 20
        frontIndexInit = 1
        backIndexInit = 2
        m = Matrix(frontVertex=frontVertexInit, backVertex=backVertexInit, frontIndex=frontIndexInit,
                   backIndex=backIndexInit)
        m.flipOrientation()
        self.assertTrue(m.isFlipped)
        self.assertEqual(m.backIndex, frontIndexInit)
        self.assertEqual(m.frontIndex, backIndexInit)
        self.assertEqual(m.frontVertex, backVertexInit)
        self.assertEqual(m.backVertex, frontVertexInit)

    def testStrRepresentation(self):
        m = Matrix(C=1)
        strRepresentation = r""" /             \ 
| {0:6.3f}   {1:6.3f} |
|               |
| {2:6.3f}   {3:6.3f} |
 \             /
""".format(1, 0, 1, 1)
        strRepresentation += "\nf={:0.3f}\n".format(-1.0)
        self.assertEqual(str(m).strip(), strRepresentation.strip())

    def testStrRepresentationAfocal(self):
        m = Matrix()
        strRepresentation = r""" /             \ 
| {0:6.3f}   {1:6.3f} |
|               |
| {2:6.3f}   {3:6.3f} |
 \             /
""".format(1, 0, 0, 1)
        strRepresentation += "\nf = +inf (afocal)\n".format(-1.0)
        self.assertEqual(str(m).strip(), strRepresentation.strip())

    def testDisplayHalfHeight(self):
        m = Matrix(apertureDiameter=10)
        minSize = 2
        self.assertEqual(m.displayHalfHeight(minSize), m.apertureDiameter / 2)

        m.apertureDiameter = inf
        self.assertEqual(m.displayHalfHeight(), 4)

        self.assertEqual(m.displayHalfHeight(6), 6)

    def testAxesToDataScale(self):
        m = Matrix()
        min, max = -10, 10
        axes = plt.subplot()
        axes.set_ylim(min, max)
        axes.set_xlim(min, max)
        val = len(range(min, max))
        self.assertTupleEqual(m.axesToDataScale(axes), (val, val))


if __name__ == '__main__':
    unittest.main()
