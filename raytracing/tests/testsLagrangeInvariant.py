import unittest
import envtest # modifies path
from raytracing import *

inf = float("+inf")


class TestLagrange(unittest.TestCase):
    def testLagrangeInvariantSpace(self):
        m = Space(d=10)
        self.assertIsNotNone(m)
        before = m.lagrangeInvariant(z=0, ray1=Ray(1,2),ray2=Ray(2,1))
        after = m.lagrangeInvariant(z=10, ray1=Ray(1,2),ray2=Ray(2,1))
        self.assertAlmostEqual(before, after)

    def testLagrangeInvariantOpticalPath(self):
        path = OpticalPath()
        path.append(Space(d=50))
        path.append(Lens(f=50))
        path.append(Space(d=50))
        before = path.lagrangeInvariant(z=0, ray1=Ray(1,2),ray2=Ray(2,1))
        after = path.lagrangeInvariant(z=150, ray1=Ray(1,2),ray2=Ray(2,1))
        self.assertAlmostEqual(before, after)



if __name__ == '__main__':
    unittest.main()