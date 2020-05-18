import unittest
import envtest # modifies path
from raytracing import *
import warnings

inf = float("+inf")


class TestThickLens(unittest.TestCase):
    def testMatrix(self):
        m = ThickLens(R1=-10, R2 = 20, n=1.5, thickness=1)
        self.assertIsNotNone(m)

    def testRayConvergingThickLens(self):
        m1 = ThickLens(R1=-10, R2 = 20, n=1.5, thickness=1)
        outRay1 = m1*Ray(y=1,theta=0)
        self.assertTrue(outRay1.theta < 0)

    def testRayDivergingThickLens(self):
        m2 = ThickLens(R1=10, R2 = -20, n=1.5, thickness=1)
        outRay2 = m2*Ray(y=1,theta=0)
        self.assertTrue(outRay2.theta >  0)

    def testRayInFlippedThickLens(self):
        m1 = CurvedMirror(R=-10)
        outRay1 = m1*Ray(y=1,theta=0)
        m2 = CurvedMirror(R=10)
        outRay2 = m2*Ray(y=1,theta=0)

        m3 = m2.flipOrientation()
        outRay3 = m3*Ray(y=1,theta=0)

        self.assertEqual(outRay3.theta, outRay1.theta)
        self.assertEqual(outRay3.theta, -outRay2.theta)



if __name__ == '__main__':
    unittest.main()