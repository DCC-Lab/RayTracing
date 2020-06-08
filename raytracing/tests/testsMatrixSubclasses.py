import envtest  # modifies path

from raytracing import *

inf = float("+inf")


class TestLens(envtest.RaytracingTestCase):

    def testLensMatrix(self):
        s = Lens(f=10)
        self.assertEqual(s.C, -1 / 10)
        self.assertEqual(s.apertureDiameter, inf)
        self.assertEqual(s.determinant, 1)
        self.assertEqual(s.frontVertex, 0)
        self.assertEqual(s.backVertex, 0)

    def testLensFocalLengths(self):
        m = Lens(f=5)
        self.assertEqual(m.effectiveFocalLengths(), (5, 5))
        self.assertEqual(m.backFocalLength(), 5)
        self.assertEqual(m.frontFocalLength(), 5)

    def testLensPointsOfInterestAllNotNone(self):
        f = 2
        l = Lens(f=f)
        pointsInterest = [{'z': -f, 'label': '$F_f$'}, {'z': f, 'label': '$F_b$'}]
        self.assertListEqual(l.pointsOfInterest(0), pointsInterest)

    def testLensPointsOfInterestNone(self):
        l = Lens(f=inf)
        self.assertListEqual(l.pointsOfInterest(0), [])


class TestCurvedMirror(envtest.RaytracingTestCase):

    def testCurvedMirrorInfiniteRadius(self):
        cm = CurvedMirror(inf)
        self.assertEqual(cm.A, 1)
        self.assertEqual(cm.B, 0)
        self.assertEqual(cm.C, 0)
        self.assertEqual(cm.D, 1)
        self.assertEqual(cm.apertureDiameter, inf)
        self.assertEqual(cm.label, "")
        self.assertEqual(cm.L, 0)
        self.assertEqual(cm.frontVertex, 0)
        self.assertEqual(cm.backVertex, 0)

    def testCurvedMirrorFiniteRadiusInfiniteDiameter(self):
        cm = CurvedMirror(0.2, label="Test")
        self.assertEqual(cm.A, 1)
        self.assertEqual(cm.B, 0)
        self.assertEqual(cm.C, 10)
        self.assertEqual(cm.D, 1)
        self.assertEqual(cm.label, "Test")

    def testCurvedMirrorFiniteRadiusFiniteDiameter(self):
        cm = CurvedMirror(-0.2, 9)
        self.assertEqual(cm.A, 1)
        self.assertEqual(cm.B, 0)
        self.assertEqual(cm.C, -10)
        self.assertEqual(cm.D, 1)
        self.assertEqual(cm.apertureDiameter, 9)

    def testCurvedMirrorPointsOfInterest(self):
        R = -4
        cm = CurvedMirror(R)
        z = 20
        pointsInterest = [{'z': z + R / 2, 'label': "$F_f$"}, {'z': z - R / 2, 'label': "$F_b$"}]
        self.assertListEqual(cm.pointsOfInterest(z), pointsInterest)

    def testCurvedMirrorNoPointsOfInterest(self):
        z = 20
        cm = CurvedMirror(inf)
        self.assertListEqual(cm.pointsOfInterest(z), [])

    def testConvergingCurvedMirror(self):
        m = CurvedMirror(R=-100)
        outRayDown = m * Ray(y=1, theta=0)
        outRayUp = m * Ray(y=-1, theta=0)
        # Ray is focussed to focal spot
        self.assertTrue(m.C < 0)
        self.assertTrue(outRayDown.theta < 0)
        self.assertTrue(outRayUp.theta > 0)

    def testDivergingCurvedMirror(self):
        m = CurvedMirror(R=100)
        outRayUp = m * Ray(y=1, theta=0)
        outRayDown = m * Ray(y=-1, theta=0)
        # Ray is diverging
        self.assertTrue(m.C > 0)
        self.assertTrue(outRayDown.theta < 0)
        self.assertTrue(outRayUp.theta > 0)

    def testCurvedMirrorFlip(self):
        # Biconvex
        m1 = CurvedMirror(R=100)
        m2 = CurvedMirror(R=-100)
        m2.flipOrientation()

        self.assertAlmostEqual(m1.determinant, 1, 4)
        self.assertAlmostEqual(m2.determinant, 1, 4)
        self.assertAlmostEqual(m1.A, m2.A, 4)
        self.assertAlmostEqual(m1.B, m2.B, 4)
        self.assertAlmostEqual(m1.C, m2.C, 4)
        self.assertAlmostEqual(m1.D, m2.D, 4)


class TestSpaceMatrix(envtest.RaytracingTestCase):

    def testSpaceMatrix(self):
        s = Space(d=10)
        self.assertEqual(s.B, 10)
        self.assertEqual(s.L, 10)
        self.assertEqual(s.determinant, 1)
        self.assertIsNone(s.frontVertex)
        self.assertIsNone(s.backVertex)

    def testSpaceMatrixNegativeDistance(self):
        s = Space(d=-10)
        self.assertEqual(s.B, -10)
        self.assertEqual(s.L, -10)
        self.assertEqual(s.determinant, 1)
        self.assertIsNone(s.frontVertex)
        self.assertIsNone(s.backVertex)

    def testSpaceMatrixMultiplicationAddsDistances(self):
        s = Space(d=10) * Space(d=5)
        self.assertEqual(s.B, 15)
        self.assertEqual(s.L, 15)
        self.assertEqual(s.determinant, 1)
        self.assertIsNone(s.frontVertex)
        self.assertIsNone(s.backVertex)

    def testSpaceMatrixInfiniteDistance(self):
        s = Space(d=inf)
        self.assertEqual(s.B, inf)
        self.assertEqual(s.L, inf)

    def testTransferMatrixInfiniteDistance(self):
        s = Space(inf)
        s = s.transferMatrix(2)
        self.assertEqual(s.A, 1)
        self.assertEqual(s.B, 2)
        self.assertEqual(s.C, 0)
        self.assertEqual(s.D, 1)
        self.assertEqual(s.determinant, 1)
        self.assertIsNone(s.frontVertex)
        self.assertIsNone(s.backVertex)
        self.assertEqual(s.L, 2)

    def testTransferMatrixFiniteDistance(self):
        s = Space(2)
        s = s.transferMatrix()
        self.assertEqual(s.A, 1)
        self.assertEqual(s.B, 2)
        self.assertEqual(s.C, 0)
        self.assertEqual(s.D, 1)
        self.assertIsNone(s.frontVertex)
        self.assertIsNone(s.backVertex)
        self.assertEqual(s.L, 2)


class TestDielectricInterface(envtest.RaytracingTestCase):

    def testDielectricInterfaceInfiniteRadiusInfiniteDiameter(self):
        di = DielectricInterface(1, 1.33)
        self.assertEqual(di.apertureDiameter, inf)
        self.assertEqual(di.n1, 1)
        self.assertEqual(di.n2, 1.33)
        self.assertEqual(di.A, 1)
        self.assertEqual(di.B, 0)
        self.assertEqual(di.C, 0)
        self.assertEqual(di.D, 1 / 1.33)
        self.assertEqual(di.L, 0)
        self.assertEqual(di.R, inf)
        self.assertEqual(di.frontVertex, 0)
        self.assertEqual(di.backVertex, 0)
        self.assertEqual(di.label, "")

    def testDielectricInterfaceFiniteRadiusFiniteDiameter(self):
        di = DielectricInterface(1, 1.33, 2, 2, "Test")
        self.assertEqual(di.apertureDiameter, 2)
        self.assertEqual(di.n1, 1)
        self.assertEqual(di.n2, 1.33)
        self.assertEqual(di.A, 1)
        self.assertEqual(di.B, 0)
        self.assertEqual(di.C, -(1.33 - 1) / (2 * 1.33))
        self.assertEqual(di.D, 1 / 1.33)
        self.assertEqual(di.L, 0)
        self.assertEqual(di.R, 2)
        self.assertEqual(di.frontVertex, 0)
        self.assertEqual(di.backVertex, 0)
        self.assertEqual(di.label, "Test")

    def testFlipOrientation(self):
        di = DielectricInterface(1, 1.33, 2, 2)
        di.flipOrientation()
        self.assertEqual(di.n1, 1.33)
        self.assertEqual(di.n2, 1)
        self.assertEqual(di.R, -2)
        self.assertEqual(di.C, -(1 - 1.33) / (-2 * 1))
        self.assertEqual(di.D, 1.33)

    def testDielectricInterfaceConvergingSign(self):
        # Positive R is convex for ray
        m = DielectricInterface(n1=1, n2=1.5, R=10)
        outRayDown = m * Ray(y=1, theta=0)
        outRayUp = m * Ray(y=-1, theta=0)

        # Ray is focussed to focal spot
        self.assertTrue(outRayDown.theta < 0)
        self.assertTrue(outRayUp.theta > 0)

    def testDielectricInterfaceDivergingSign(self):
        # Negative R is concave for ray
        m = DielectricInterface(n1=1, n2=1.5, R=-10)
        outRayUp = m * Ray(y=1, theta=0)
        outRayDown = m * Ray(y=-1, theta=0)

        # Ray is diverging
        self.assertTrue(outRayDown.theta < 0)
        self.assertTrue(outRayUp.theta > 0)


class TestThickLens(envtest.RaytracingTestCase):

    def testThickLensNullThicknessInfiniteDiameter(self):
        tl = ThickLens(1.33, 5, -5, 0)
        self.assertEqual(tl.R1, 5)
        self.assertEqual(tl.R2, -5)
        self.assertEqual(tl.n, 1.33)
        self.assertEqual(tl.A, 1)
        self.assertEqual(tl.B, 0)
        self.assertEqual(tl.C, -(1.33 - 1) * (1 / 5 + 1 / 5))
        self.assertEqual(tl.D, 1)
        self.assertEqual(tl.L, 0)
        self.assertEqual(tl.apertureDiameter, inf)
        self.assertEqual(tl.frontVertex, 0)
        self.assertEqual(tl.backVertex, 0)
        self.assertEqual(tl.label, "")

    def testThickLensFiniteThicknessFiniteDiameter(self):
        tl = ThickLens(1.33, 5, 10, 2, 10, "Test")
        self.assertEqual(tl.R1, 5)
        self.assertEqual(tl.R2, 10)
        self.assertEqual(tl.n, 1.33)
        self.assertEqual(tl.A, 2 * (1 - 1.33) / (1.33 * 5) + 1)
        self.assertEqual(tl.B, 2 / 1.33)
        self.assertEqual(tl.C, -(1.33 - 1) * (1 / 5 - 1 / 10 + 2 * (1.33 - 1) / (1.33 * 5 * 10)))
        self.assertEqual(tl.D, 2 * (1.33 - 1) / (1.33 * 10) + 1)
        self.assertEqual(tl.L, 2)
        self.assertEqual(tl.apertureDiameter, 10)
        self.assertEqual(tl.backVertex, 2)
        self.assertEqual(tl.label, "Test")

    def testThickLensPointsOfInterest(self):
        z = 10
        tl = ThickLens(1.33, 5, -8, 10, 100)
        f = - 1 / tl.C
        p1 = z - (1 - tl.D) / tl.C
        p2 = z + 10 + (1 - tl.A) / tl.C
        focusPos = p1 - f, p2 + f
        pointsInterest = [{'z': focusPos[0], 'label': "$F_f$"}, {'z': focusPos[1], 'label': "$F_b$"}]
        self.assertListEqual(tl.pointsOfInterest(z), pointsInterest)

    def testThickLensNoPointsOfInterest(self):
        tl = ThickLens(n=1, R1=100, R2=-100, thickness=2)
        self.assertListEqual(tl.pointsOfInterest(0), [])

    def testRayConvergingThickLens(self):
        m1 = ThickLens(R1=10, R2=20, n=1.5, thickness=1)
        outRay1 = m1 * Ray(y=1, theta=0)
        self.assertTrue(outRay1.theta < 0)

    def testRayDivergingThickLens(self):
        m2 = ThickLens(R1=-10, R2=-20, n=1.5, thickness=1)
        outRay2 = m2 * Ray(y=1, theta=0)
        self.assertTrue(outRay2.theta > 0)

    def testThickConvergingLens(self):
        # Biconvex
        m = ThickLens(n=1.55, R1=100, R2=-100, thickness=3)
        outRayDown = m * Ray(y=1, theta=0)
        outRayUp = m * Ray(y=-1, theta=0)

        # Ray is focussed to focal spot
        self.assertTrue(m.C < 0)
        self.assertTrue(outRayDown.theta < 0)
        self.assertTrue(outRayUp.theta > 0)

    def testThickDivergingLens(self):
        # Biconcave
        m = ThickLens(n=1.55, R1=-100, R2=100, thickness=3)
        outRayUp = m * Ray(y=1, theta=0)
        outRayDown = m * Ray(y=-1, theta=0)

        # Ray is diverging
        self.assertTrue(m.C > 0)
        self.assertTrue(outRayDown.theta < 0)
        self.assertTrue(outRayUp.theta > 0)

    def testThickConvergingLensFlip(self):
        # Biconvex
        m1 = ThickLens(n=1.55, R1=200, R2=-100, thickness=3)
        m2 = ThickLens(n=1.55, R1=100, R2=-200, thickness=3)
        m2.flipOrientation()

        self.assertAlmostEqual(m1.determinant, 1, 4)
        self.assertAlmostEqual(m2.determinant, 1, 4)
        self.assertAlmostEqual(m1.A, m2.A, 4)
        self.assertAlmostEqual(m1.B, m2.B, 4)
        self.assertAlmostEqual(m1.C, m2.C, 4)
        self.assertAlmostEqual(m1.D, m2.D, 4)
        self.assertEqual(m1.R1, m2.R1)
        self.assertEqual(m1.R2, m2.R2)

    def testTransferMatrixWholeThickLens(self):
        tl = ThickLens(1.33, 10, -6, 1, 20)
        transMat = tl.transferMatrix()
        self.assertEqual(tl.n, transMat.n)
        self.assertEqual(tl.L, transMat.L)
        self.assertEqual(tl.apertureDiameter, transMat.apertureDiameter)
        self.assertEqual(tl.label, transMat.label)
        self.assertEqual(tl.A, transMat.A)
        self.assertEqual(tl.B, transMat.B)
        self.assertEqual(tl.C, transMat.C)
        self.assertEqual(tl.D, transMat.D)

    def testTransferMatrixPartialThickLens(self):
        originalTl = ThickLens(1.33, -100, 100, 4, 120)
        transMat = originalTl.transferMatrix(2)
        finalTl = Space(2, 1.33) * DielectricInterface(1, 1.33, -100, 120)
        self.assertEqual(finalTl.backIndex, transMat.backIndex)
        self.assertEqual(finalTl.frontIndex, transMat.frontIndex)
        self.assertEqual(finalTl.L, transMat.L)
        self.assertEqual(finalTl.apertureDiameter, transMat.apertureDiameter)
        self.assertEqual(finalTl.label, transMat.label)
        self.assertEqual(finalTl.A, transMat.A)
        self.assertEqual(finalTl.B, transMat.B)
        self.assertEqual(finalTl.C, transMat.C)
        self.assertEqual(finalTl.D, transMat.D)


class TestDielectricSlab(envtest.RaytracingTestCase):

    def testDielectricSlabInfiniteDiameter(self):
        ds = DielectricSlab(1.33, 2)
        self.assertEqual(ds.A, 1)
        self.assertEqual(ds.B, 2 / 1.33)
        self.assertEqual(ds.C, 0)
        self.assertEqual(ds.D, 1)
        self.assertEqual(ds.n, 1.33)
        self.assertEqual(ds.R1, inf)
        self.assertEqual(ds.R2, inf)
        self.assertEqual(ds.L, 2)
        self.assertEqual(ds.apertureDiameter, inf)
        self.assertEqual(ds.label, "")

    def testDielectricSlabFiniteDiameter(self):
        ds = DielectricSlab(1.33, 2, 22, label="Test")
        self.assertEqual(ds.A, 1)
        self.assertEqual(ds.B, 2 / 1.33)
        self.assertEqual(ds.C, 0)
        self.assertEqual(ds.D, 1)
        self.assertEqual(ds.n, 1.33)
        self.assertEqual(ds.R1, inf)
        self.assertEqual(ds.R2, inf)
        self.assertEqual(ds.L, 2)
        self.assertEqual(ds.apertureDiameter, 22)
        self.assertEqual(ds.label, "Test")

    def testTransferMatrixWholeSlab(self):
        ds = DielectricSlab(1, 10)
        transMat = ds.transferMatrix()
        self.assertEqual(ds.n, transMat.n)
        self.assertEqual(ds.L, transMat.L)
        self.assertEqual(ds.apertureDiameter, transMat.apertureDiameter)
        self.assertEqual(ds.label, transMat.label)
        self.assertEqual(ds.A, transMat.A)
        self.assertEqual(ds.B, transMat.B)
        self.assertEqual(ds.C, transMat.C)
        self.assertEqual(ds.D, transMat.D)

    def testTransferMatrixPartialSlab(self):
        originalDs = DielectricSlab(1.33, 10)
        transMat = originalDs.transferMatrix(5)
        finalDs = Space(5, 1.33) * DielectricInterface(1, 1.33)
        self.assertEqual(finalDs.backIndex, transMat.backIndex)
        self.assertEqual(finalDs.frontIndex, transMat.frontIndex)
        self.assertEqual(finalDs.L, transMat.L)
        self.assertEqual(finalDs.apertureDiameter, transMat.apertureDiameter)
        self.assertEqual(finalDs.label, transMat.label)
        self.assertEqual(finalDs.A, transMat.A)
        self.assertEqual(finalDs.B, transMat.B)
        self.assertEqual(finalDs.C, transMat.C)
        self.assertEqual(finalDs.D, transMat.D)


class TestAperture(envtest.RaytracingTestCase):

    def testApertureMatrix(self):
        s = Aperture(diameter=25)
        self.assertEqual(s.apertureDiameter, 25)
        self.assertEqual(s.A, 1)
        self.assertEqual(s.B, 0)
        self.assertEqual(s.C, 0)
        self.assertEqual(s.D, 1)
        self.assertEqual(s.determinant, 1)
        self.assertIsNone(s.frontVertex)
        self.assertIsNone(s.backVertex)


if __name__ == '__main__':
    envtest.main()
