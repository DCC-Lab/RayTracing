import unittest
import envtest  # modifies path

from raytracing import *

inf = float("+inf")


class TestThickLens(unittest.TestCase):

    def testTransferMatrix(self):
        tl = ThickLens(1, 10, -10, 2)
        transMat = tl.transferMatrix()
        self.assertEqual(tl.n, transMat.n)
        self.assertEqual(tl.L, transMat.L)
        self.assertEqual(tl.apertureDiameter, transMat.apertureDiameter)
        self.assertEqual(tl.label, transMat.label)
        self.assertEqual(tl.A, transMat.A)
        self.assertEqual(tl.B, transMat.B)
        self.assertEqual(tl.C, transMat.C)
        self.assertEqual(tl.D, transMat.D)

        originalTl = ThickLens(1.33, 10, -10, 2)
        transMat = originalTl.transferMatrix(1)
        finalTl = Space(1, 1.33, 2) * DielectricInterface(1, 1.33, 10, 2)
        self.assertEqual(finalTl.backIndex, transMat.backIndex)
        self.assertEqual(finalTl.frontIndex, transMat.frontIndex)
        self.assertEqual(finalTl.L, transMat.L)
        self.assertEqual(finalTl.apertureDiameter, transMat.apertureDiameter)
        self.assertEqual(finalTl.A, transMat.A)
        self.assertEqual(finalTl.B, transMat.B)
        self.assertEqual(finalTl.C, transMat.C)
        self.assertEqual(finalTl.D, transMat.D)
