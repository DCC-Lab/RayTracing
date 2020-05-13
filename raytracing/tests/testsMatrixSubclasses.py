import unittest
import env  # modifies path

from raytracing import *

inf = float("+inf")


class TestLens(unittest.TestCase):

    def testLensMatrix(self):
        s = Lens(f=10)
        self.assertEqual(s.C, -1 / 10)
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
        f = 1
        l = Lens(f=f)
        l.C = 0
        self.assertListEqual(l.pointsOfInterest(0), [])


class TestCurvedMirror(unittest.TestCase):

    def testCurvedMirror(self):
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

        cm = CurvedMirror(0.2, label="Test")
        self.assertEqual(cm.A, 1)
        self.assertEqual(cm.B, 0)
        self.assertEqual(cm.C, -10)
        self.assertEqual(cm.D, 1)
        self.assertEqual(cm.label, "Test")

        cm = CurvedMirror(-0.2, 9)
        self.assertEqual(cm.A, 1)
        self.assertEqual(cm.B, 0)
        self.assertEqual(cm.C, 10)
        self.assertEqual(cm.D, 1)
        self.assertEqual(cm.apertureDiameter, 9)

    def testCurvedMirrorPointsOfInterest(self):
        R = -4
        cm = CurvedMirror(R)
        z = 20
        pointsInterest = [{'z': z - R / 2, 'label': "$F_f$"}, {'z': z + R / 2, 'label': "$F_b$"}]
        self.assertListEqual(cm.pointsOfInterest(z), pointsInterest)

        cm.C = 0
        self.assertListEqual(cm.pointsOfInterest(z), [])


class TestSpaceMatrix(unittest.TestCase):

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
        # 0 * inifinity = nan in python
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

        # 0 * inifinity = nan in python
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
