import unittest
import envtest # modifies path
from raytracing import *
import warnings

inf = float("+inf")


class TestCurvedMirror(unittest.TestCase):
    def testMatrix(self):
        m = CurvedMirror(R=-10)
        self.assertIsNotNone(m)

    def testRayInMirror(self):
        # Convex mirror is positive radius, concave is negative
        m1 = CurvedMirror(R=-10)
        outRay1 = m1*Ray(y=1,theta=0)
        self.assertTrue(outRay1.theta < 0)

        m2 = CurvedMirror(R=10)
        outRay2 = m2*Ray(y=1,theta=0)
        self.assertTrue(outRay2.theta >  0)

    def testRayInFlippedMirror(self):
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