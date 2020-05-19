import unittest
import envtest  # modifies path
from raytracing import *

inf = float("+inf")


class TestRays(unittest.TestCase):

    def testRays(self):
        r = Rays()
        self.assertIsNotNone(r)
        self.assertListEqual(r.rays, [])
        self.assertEqual(r.iteration, 0)
        self.assertEqual(r.progressLog, 10000)
        self.assertIsNone(r._yValues)
        self.assertIsNone(r._thetaValues)
        self.assertIsNone(r._yHistogram)
        self.assertIsNone(r._thetaHistogram)
        self.assertIsNone(r._directionBinEdges)

        r = Rays([])
        self.assertListEqual(r.rays, [])

        listOfRays = [Ray(), Ray(1, 1), Ray(1, -2), Ray(0, -1)]
        r = Rays(listOfRays)
        self.assertListEqual(r.rays, listOfRays)

    def testRaysLen(self):
        r = Rays()
        self.assertEqual(len(r), 0)

        r = Rays([])
        self.assertEqual(len(r), 0)

        listOfRays = [Ray(), Ray(1, 1), Ray(1, -2), Ray(0, -1)]
        r = Rays(listOfRays)
        self.assertEqual(len(r), len(listOfRays))

    def testCountRays(self):
        r = Rays()
        self.assertEqual(r.count, 0)

        r = Rays([])
        self.assertEqual(r.count, 0)

        listOfRays = [Ray(), Ray(1, 1), Ray(1, -2), Ray(0, -1)]
        r = Rays(listOfRays)
        self.assertEqual(r.count, 4)

    def testYValues(self):
        r = Rays()
        self.assertListEqual(r.yValues, [])

        r = Rays([])
        self.assertListEqual(r.yValues, [])

        listOfRays = [Ray(), Ray(1, 1), Ray(1, -2), Ray(0, -1)]
        r = Rays(listOfRays)
        self.assertListEqual(r.yValues, [0, 1, 1, 0])

    def testThetaValues(self):
        r = Rays()
        self.assertListEqual(r.thetaValues, [])

        r = Rays([])
        self.assertListEqual(r.thetaValues, [])

        listOfRays = [Ray(), Ray(1, 1), Ray(1, -2), Ray(0, -1)]
        r = Rays(listOfRays)
        self.assertListEqual(r.thetaValues, [0, 1, -2, -1])

    def testRayCountHistogram(self):
        r = Rays()
        self.assertTupleEqual(r.rayCountHistogram(3, 0, 3), ([0.5, 1.5, 2.5], [0, 0, 0]))

        r = [Ray(a, a) for a in range(6)]
        r = Rays(r)
        tRes = ([x * 0.5 + 0.25 for x in range(10)], [1, 0, 1, 0, 1, 0, 1, 0, 1, 1])
        self.assertTupleEqual(r.rayCountHistogram(10), tRes)

        r = [Ray(a, a) for a in range(50)]
        r = Rays(r)
        self.assertTupleEqual(r.rayCountHistogram(minValue=0), ([a * 1.25 - 0.625 for a in range(2, 50)], []))
