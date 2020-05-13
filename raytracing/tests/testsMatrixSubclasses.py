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

        s = Space(d=inf)
        self.assertEqual(s.B, inf)
        self.assertEqual(s.L, inf)

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

    def testTransferMatrix(self):
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

        s = Space(2)
        s = s.transferMatrix()
        self.assertEqual(s.A, 1)
        self.assertEqual(s.B, 2)
        self.assertEqual(s.C, 0)
        self.assertEqual(s.D, 1)
        self.assertIsNone(s.frontVertex)
        self.assertIsNone(s.backVertex)
        self.assertEqual(s.L, 2)


class TestDielectricInterface(unittest.TestCase):

    def testDielectricInterface(self):
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


class TestThickLens(unittest.TestCase):

    def testThickLens(self):
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


class TestDielectricSlab(unittest.TestCase):

    def testDielectricSlab(self):
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


class TestAperture(unittest.TestCase):

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
    unittest.main()
