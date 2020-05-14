import unittest
import envtest # modifies path

from raytracing import *

inf = float("+inf")


class TestMatrix(unittest.TestCase):
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

    def testApertureDiameter(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, apertureDiameter=2)
        self.assertTrue(m1.hasFiniteApertureDiameter())
        self.assertEqual(m1.largestDiameter(), 2.0)
        m2 = Matrix(A=1, B=2, C=3, D=4)
        self.assertFalse(m2.hasFiniteApertureDiameter())
        self.assertEqual(m2.largestDiameter(), float("+inf"))

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
        m1 = Matrix(A=1, B=2, C=3, D=4)
        self.assertEqual(m1.transferMatrices(), [m1])
        m1 * GaussianBeam(w=1, n=2)

    def testIsImaging(self):
        m1 = Matrix(A=1, B=0, C=3, D=4)
        self.assertTrue(m1.isImaging)
        m2 = Matrix(A=1, B=1, C=3, D=4)
        self.assertFalse(m2.isImaging)

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

    def deactivated_testInfiniteForwardConjugate(self):
        m1 = Lens(f=5) * Space(d=5)
        (d, m2) = m1.forwardConjugate()
        self.assertTrue(m2.isImaging)
        self.assertEqual(d, float("+inf"))
        self.assertEqual(m1.determinant, 1)
        self.assertEqual(m2.determinant, 1)

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

    def testSpaceMatrix(self):
        s = Space(d=10)
        self.assertEqual(s.B, 10)
        self.assertEqual(s.L, 10)
        self.assertEqual(s.determinant, 1)
        self.assertIsNone(s.frontVertex)
        self.assertIsNone(s.backVertex)

        s = Space(d=-10)
        self.assertEqual(s.B, -10)
        self.assertEqual(s.L, -10)
        self.assertEqual(s.determinant, 1)
        self.assertIsNone(s.frontVertex)
        self.assertIsNone(s.backVertex)

        s = Space(d=10) * Space(d=5)
        self.assertEqual(s.B, 15)
        self.assertEqual(s.L, 15)
        self.assertEqual(s.determinant, 1)
        self.assertIsNone(s.frontVertex)
        self.assertIsNone(s.backVertex)

    def deactivated_testInfiniteSpaceMatrix(self):
        s = Space(d=inf)
        self.assertEqual(s.A, 1)
        self.assertEqual(s.B, inf)
        self.assertEqual(s.C, 0)
        self.assertEqual(s.D, 1)
        self.assertEqual(s.determinant, 1)
        self.assertIsNone(s.frontVertex)
        self.assertIsNone(s.backVertex)

    def deactivated_testInfiniteSpaceMatrixMultiplication(self):
        # This should work, not sure how to deal
        # with this failed test: C is identically
        # zero and 0 * d->inf == 0 (I think).
        s = Space(d=1) * Space(d=inf)
        self.assertEqual(s.A, 1)
        self.assertEqual(s.B, inf)
        self.assertEqual(s.C, 0)
        self.assertEqual(s.D, 1)
        self.assertEqual(s.determinant, 1)
        self.assertIsNone(s.frontVertex)
        self.assertIsNone(s.backVertex)

        s = Space(d=inf) * Space(d=1)
        self.assertEqual(s.A, 1)
        self.assertEqual(s.B, inf)
        self.assertEqual(s.C, 0)
        self.assertEqual(s.D, 1)
        self.assertEqual(s.determinant, 1)
        self.assertIsNone(s.frontVertex)
        self.assertIsNone(s.backVertex)

        s = Space(d=inf) * Space(d=inf)
        self.assertEqual(s.A, 1)
        self.assertEqual(s.B, inf)
        self.assertEqual(s.C, 0)
        self.assertEqual(s.D, 1)
        self.assertEqual(s.determinant, 1)
        self.assertIsNone(s.frontVertex)
        self.assertIsNone(s.backVertex)

    def testLensMatrix(self):
        s = Lens(f=10)
        self.assertEqual(s.C, -1 / 10)
        self.assertEqual(s.determinant, 1)
        self.assertEqual(s.frontVertex, 0)
        self.assertEqual(s.backVertex, 0)

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

    def testDielectricInterface(self):
        m = DielectricInterface(n1=1, n2=1.5, R=10)
        self.assertEqual(m.determinant, 1 / 1.5)
        self.assertEqual(m.frontVertex, 0)
        self.assertEqual(m.backVertex, 0)

    def testDielectricInterfaceConvergingSign(self):
        # Positive R is convex for ray
        m = DielectricInterface(n1=1, n2=1.5, R=10)
        outRayDown = m*Ray(y=1,theta=0)
        outRayUp = m*Ray(y=-1,theta=0)

        # Ray is focussed to focal spot
        self.assertTrue(outRayDown.theta < 0)
        self.assertTrue(outRayUp.theta > 0)

    def testDielectricInterfaceDivergingSign(self):
        # Negative R is concave for ray
        m = DielectricInterface(n1=1, n2=1.5, R=-10)
        outRayUp = m*Ray(y=1,theta=0)
        outRayDown = m*Ray(y=-1,theta=0)

        # Ray is diverging
        self.assertTrue(outRayDown.theta < 0)
        self.assertTrue(outRayUp.theta > 0)

    def testThickConvergingLens(self):
        # Biconvex
        m = ThickLens(n=1.55, R1=100, R2=-100, thickness=3)
        outRayDown = m*Ray(y=1,theta=0)
        outRayUp = m*Ray(y=-1,theta=0)

        # Ray is focussed to focal spot
        self.assertTrue(m.C < 0)
        self.assertTrue(outRayDown.theta < 0)
        self.assertTrue(outRayUp.theta > 0)

    def testThickDivergingLens(self):
        # Biconcave
        m = ThickLens(n=1.55, R1=-100, R2=100, thickness=3)
        outRayUp = m*Ray(y=1,theta=0)
        outRayDown = m*Ray(y=-1,theta=0)

        # Ray is diverging
        self.assertTrue(m.C > 0)
        self.assertTrue(outRayDown.theta < 0)
        self.assertTrue(outRayUp.theta > 0)

    def testThickConvergingLensEquivalence(self):
        # Biconvex
        m = ThickLens(n=1.55, R1=100, R2=-100, thickness=3)

        mEquivalent = MatrixGroup()
        mEquivalent.append(DielectricInterface(n1=1, n2=1.55, R=100))
        mEquivalent.append(Space(d=3))
        mEquivalent.append(DielectricInterface(n1=1.55, n2=1.0, R=-100))

        self.assertAlmostEqual(m.A, mEquivalent.A,3)
        self.assertAlmostEqual(m.B, mEquivalent.B,3)
        self.assertAlmostEqual(m.C, mEquivalent.C,3)
        self.assertAlmostEqual(m.D, mEquivalent.D,3)

    def testThickConvergingLensFlip(self):
        # Biconvex
        m1 = ThickLens(n=1.55, R1=200, R2=-100, thickness=3)
        m2 = ThickLens(n=1.55, R1=100, R2=-200, thickness=3)
        m2.flipOrientation()

        self.assertAlmostEqual(m1.determinant, 1,4)
        self.assertAlmostEqual(m2.determinant, 1,4)
        self.assertAlmostEqual(m1.A, m2.A,4)
        self.assertAlmostEqual(m1.B, m2.B,4)
        self.assertAlmostEqual(m1.C, m2.C,4)
        self.assertAlmostEqual(m1.D, m2.D,4)

    def testConvergingCurvedMirror(self):
        # Concave should be positive?
        m = CurvedMirror(R=-100)
        outRayDown = m*Ray(y=1,theta=0)
        outRayUp = m*Ray(y=-1,theta=0)

        # Ray is focussed to focal spot
        self.assertTrue(m.C < 0)
        self.assertTrue(outRayDown.theta < 0)
        self.assertTrue(outRayUp.theta > 0)

    def testDivergingCurvedMirror(self):
        m = CurvedMirror(R=100)
        outRayUp = m*Ray(y=1,theta=0)
        outRayDown = m*Ray(y=-1,theta=0)

        # Ray is diverging
        self.assertTrue(m.C > 0)
        self.assertTrue(outRayDown.theta < 0)
        self.assertTrue(outRayUp.theta > 0)

    def testCurvedMirrorFlip(self):
        # Biconvex
        m1 = CurvedMirror(R=100)
        m2 = CurvedMirror(R=-100)
        m2.flipOrientation()

        self.assertAlmostEqual(m1.determinant, 1,4)
        self.assertAlmostEqual(m2.determinant, 1,4)
        self.assertAlmostEqual(m1.A, m2.A,4)
        self.assertAlmostEqual(m1.B, m2.B,4)
        self.assertAlmostEqual(m1.C, m2.C,4)
        self.assertAlmostEqual(m1.D, m2.D,4)

    def testLensFocalLengths(self):
        m = Lens(f=5)
        self.assertEqual(m.effectiveFocalLengths(), (5, 5))
        self.assertEqual(m.backFocalLength(), 5)
        self.assertEqual(m.frontFocalLength(), 5)

    def deactivated_testThickLensFocalLengths(self):
        m = ThickLens(n=1.55, R1=100, R2=-100, thickness=3)

        self.assertEqual(m.backFocalLength(), 5)
        self.assertEqual(m.frontFocalLength(), 5)

    def testOlympusLens(self):
        self.assertIsNotNone(olympus.LUMPlanFL40X())
        self.assertIsNotNone(olympus.XLUMPlanFLN20X())
        self.assertIsNotNone(olympus.MVPlapo2XC())
        self.assertIsNotNone(olympus.UMPLFN20XW())

    def testThorlabsLenses(self):
        l = thorlabs.ACN254_100_A()
        l = thorlabs.ACN254_075_A()
        l = thorlabs.ACN254_050_A()
        l = thorlabs.ACN254_040_A()
        l = thorlabs.AC254_030_A()
        l = thorlabs.AC254_035_A()
        l = thorlabs.AC254_045_A()
        l = thorlabs.AC254_050_A()
        l = thorlabs.AC254_060_A()
        l = thorlabs.AC254_075_A()
        l = thorlabs.AC254_080_A()
        l = thorlabs.AC254_100_A()
        l = thorlabs.AC254_125_A()
        l = thorlabs.AC254_200_A()
        l = thorlabs.AC254_250_A()
        l = thorlabs.AC254_300_A()
        l = thorlabs.AC254_400_A()
        l = thorlabs.AC254_500_A()

        l = thorlabs.AC508_075_B()
        l = thorlabs.AC508_080_B()
        l = thorlabs.AC508_100_B()
        l = thorlabs.AC508_150_B()
        l = thorlabs.AC508_200_B()
        l = thorlabs.AC508_250_B()
        l = thorlabs.AC508_300_B()
        l = thorlabs.AC508_400_B()
        l = thorlabs.AC508_500_B()
        l = thorlabs.AC508_750_B()
        l = thorlabs.AC508_1000_B()

    def testEdmundLens(self):
        l = eo.PN_33_921()


if __name__ == '__main__':
    unittest.main()
