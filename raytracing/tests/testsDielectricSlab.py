import unittest
import envtest # modifies path

from raytracing import *

inf = float("+inf")

class TestDielectricSlab(unittest.TestCase):

    def testTransferMatrix(self):
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