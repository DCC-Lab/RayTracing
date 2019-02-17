import unittest
import env # modifies path
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
        self.assertEqual(m3.A, 1*5 + 3*6)
        self.assertEqual(m3.B, 2*5 + 4*6)
        self.assertEqual(m3.C, 1*7 + 3*8)
        self.assertEqual(m3.D, 2*7 + 4*8)

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
        m1 = Matrix(A=1, B=2, C=3, D=4, physicalLength=10,frontVertex=0, backVertex=10)
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

    def testIsImaging(self):
        m1 = Matrix(A=1, B=0, C=3, D=4)
        self.assertTrue(m1.isImaging)
        m2 = Matrix(A=1, B=1, C=3, D=4)
        self.assertFalse(m2.isImaging)

    def testFiniteForwardConjugate(self):
        m1 = Lens(f=5)*Space(d=10)
        (d,m2) = m1.forwardConjugate()
        self.assertTrue(m2.isImaging)
        self.assertEqual(d, 10)

        m1 = Space(d=5)*Lens(f=5)*Space(d=10)
        (d,m2) = m1.forwardConjugate()
        self.assertTrue(m2.isImaging)
        self.assertEqual(d, 5)

    def testInfiniteForwardConjugate(self):
        m1 = Lens(f=5)*Space(d=5)
        (d,m2) = m1.forwardConjugate()
        self.assertTrue(m2.isImaging)
        self.assertEqual(d, float("+inf"))

    def testFiniteBackConjugate(self):
        m1 = Space(d=10)*Lens(f=5)
        (d,m2) = m1.backwardConjugate()
        self.assertTrue(m2.isImaging)
        self.assertEqual(d, 10)

        m1 = Space(d=10)*Lens(f=5)*Space(d=5)
        (d,m2) = m1.backwardConjugate()
        self.assertTrue(m2.isImaging)
        self.assertEqual(d, 5)

    def testSpaceMatrix(self):
        s = Space(d=10)
        self.assertEqual(s.B, 10)
        self.assertEqual(s.L, 10)
        s = Space(d=-10)
        self.assertEqual(s.B, -10)
        self.assertEqual(s.L, -10)
        s = Space(d=10)*Space(d=5)
        self.assertEqual(s.B, 15)
        self.assertEqual(s.L, 15)

    def testInfiniteSpaceMatrix(self):
        s = Space(d=inf)
        self.assertEqual(s.A, 1)
        self.assertEqual(s.B, inf)
        self.assertEqual(s.C, 0)
        self.assertEqual(s.D, 1)

    def testInfiniteSpaceMatrixMultiplication(self):
        # This should work, not sure how to deal
        # with this failed test: C is identically
        # zero and 0 * d->inf == 0 (I think).
        s = Space(d=1)*Space(d=inf)
        self.assertEqual(s.A, 1)
        self.assertEqual(s.B, inf)
        self.assertEqual(s.C, 0)
        self.assertEqual(s.D, 1)

        s = Space(d=inf)*Space(d=1)
        self.assertEqual(s.A, 1)
        self.assertEqual(s.B, inf)
        self.assertEqual(s.C, 0)
        self.assertEqual(s.D, 1)

        s = Space(d=inf)*Space(d=inf)
        self.assertEqual(s.A, 1)
        self.assertEqual(s.B, inf)
        self.assertEqual(s.C, 0)
        self.assertEqual(s.D, 1)



if __name__ == '__main__':
    unittest.main()