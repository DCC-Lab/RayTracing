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

    def testMatrixProductVerticesAllNone(self):
        m1 = Matrix(A=1, B=2, C=3, D=4)
        m2 = Matrix(A=5, B=6, C=7, D=8)
        m3 = m2 * m1        
        self.assertEqual(m3.L, m1.L + m2.L)
        self.assertIsNone(m3.frontVertex)
        self.assertIsNone(m3.backVertex)

    def testMatrixProductVerticesSecondNone(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, physicalLength=10)
        m2 = Matrix(A=5, B=6, C=7, D=8)
        m3 = m2 * m1        
        self.assertEqual(m3.L, m1.L + m2.L)
        self.assertEqual(m3.frontVertex, 0)
        self.assertEqual(m3.backVertex, 10)

    def testMatrixProductVerticesFirstNone(self):
        m1 = Matrix(A=1, B=2, C=3, D=4)
        m2 = Matrix(A=5, B=6, C=7, D=8, physicalLength=10)
        m3 = m2 * m1        
        self.assertEqual(m3.L, m1.L + m2.L)
        self.assertEqual(m3.frontVertex, 0)
        self.assertEqual(m3.backVertex, 10)

    def testMatrixProductVerticesTwoElements(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, physicalLength=5)
        m2 = Matrix(A=5, B=6, C=7, D=8, physicalLength=10)
        m3 = m2 * m1        
        self.assertEqual(m3.L, m1.L + m2.L)
        self.assertEqual(m3.frontVertex, 0)
        self.assertEqual(m3.backVertex, 15)

if __name__ == '__main__':
    unittest.main()