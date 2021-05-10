import envtest # modifies path
from raytracing import *

inf = float("+inf")


class TestRay(envtest.RaytracingTestCase):

    def testRay(self):
        ray = Ray()
        
        self.assertIsNotNone(ray)
        self.assertEqual(ray.y, 0)
        self.assertEqual(ray.theta, 0)
        self.assertEqual(ray.z, 0)
        self.assertEqual(ray.apertureDiameter, inf)
        self.assertFalse(ray.isBlocked)
        self.assertTrue(ray.isNotBlocked)

    def testFan(self):
        fan = Ray.fan(y=0, radianMin=-0.1, radianMax=0.1, N=5)
        self.assertIsNotNone(fan)
        self.assertEqual(len(fan), 5)
        self.assertEqual(min(map(lambda r: r.theta, fan)), -0.1)
        self.assertEqual(max(map(lambda r: r.theta, fan)), 0.1)
        self.assertEqual(min(map(lambda r: r.y, fan)), 0)
        self.assertEqual(max(map(lambda r: r.y, fan)), 0)

    def testUnitFan(self):
        fan = Ray.fan(y=0, radianMin=-0.1, radianMax=0.1, N=1)
        self.assertIsNotNone(fan)
        self.assertEqual(len(fan), 1)
        self.assertEqual(min(map(lambda r: r.theta, fan)), -0.1)
        self.assertEqual(max(map(lambda r: r.theta, fan)), -0.1)
        self.assertEqual(min(map(lambda r: r.y, fan)), 0)
        self.assertEqual(max(map(lambda r: r.y, fan)), 0)

    def testFanGroup(self):
        fanGroup = Ray.fanGroup(yMin=0, yMax=1, M=10, radianMin=-0.1, radianMax=0.1, N=5)
        self.assertIsNotNone(fanGroup)
        self.assertEqual(len(fanGroup), 10 * 5)
        self.assertEqual(min(map(lambda r: r.theta, fanGroup)), -0.1)
        self.assertEqual(max(map(lambda r: r.theta, fanGroup)), 0.1)
        self.assertEqual(min(map(lambda r: r.y, fanGroup)), 0)
        self.assertEqual(max(map(lambda r: r.y, fanGroup)), 1)

    def testUnitFanGroup(self):
        fanGroup = Ray.fanGroup(yMin=0, yMax=1, M=1, radianMin=-0.1, radianMax=0.1, N=1)
        self.assertIsNotNone(fanGroup)
        self.assertEqual(len(fanGroup), 1)
        self.assertEqual(min(map(lambda r: r.theta, fanGroup)), -0.1)
        self.assertEqual(max(map(lambda r: r.theta, fanGroup)), -0.1)
        self.assertEqual(min(map(lambda r: r.y, fanGroup)), 0)
        self.assertEqual(max(map(lambda r: r.y, fanGroup)), 0)

    def testNullFan(self):
        with self.assertRaises(Exception) as context:
            fan = Ray.fan(y=0, radianMin=-0.1, radianMax=0.1, N=0)

    def testNullFanGroup(self):
        with self.assertRaises(Exception) as context:
            fanGroup = Ray.fanGroup(yMin=0, yMax=1, M=0, radianMin=-0.1, radianMax=0.1, N=5)

        with self.assertRaises(Exception) as context:
            fanGroup = Ray.fanGroup(yMin=0, yMax=1, M=1, radianMin=-0.1, radianMax=0.1, N=0)

    def testPrintString(self):
        ray = Ray()
        ray_desc = "{0}".format(ray)
        ray.isBlocked = True
        blockedray_desc = "{0}".format(ray)
        self.assertIsNotNone(ray_desc)
        self.assertIsNotNone(blockedray_desc)
        self.assertNotEqual(ray_desc, blockedray_desc)

    def testEqualWithStr(self):
        ray = Ray(10, 10)
        other = "this is a ray"
        self.assertNotEqual(ray, other)

    def testEqualWithNone(self):
        ray = Ray(10, 10)
        other = None
        self.assertNotEqual(ray, other)

    def testEqualWithMatrix(self):
        ray = Ray(10, 10)
        other = Matrix()
        self.assertNotEqual(ray, other)

    def testEqualWithDifferentRay(self):
        ray = Ray(10, 10)
        other = Ray(0, 10)
        self.assertNotEqual(ray, other)

    def testEqualWithDifferentRay2(self):
        ray = Ray(10, 10)
        other = Ray(10, 0)
        self.assertNotEqual(ray, other)

    def testEqualWithSameRay(self):
        ray = Ray(10, 10)
        other = Ray(10, 10)
        self.assertEqual(ray, other)

    def testRayParallelToAnotherRay(self):
        ray = Ray(0,0).at(z=1)
        self.assertEqual(ray, Ray(0,0))

        ray = Ray(0,0.1).at(z=1)
        self.assertEqual(ray, Ray(0.1, 0.1))

        ray = Ray(0,0.1).at(z=-1)
        self.assertEqual(ray, Ray(-0.1, 0.1))

        ray = Ray(1,0.1).at(z=1)
        self.assertEqual(ray, Ray(1.1,0.1))

        ray = Ray(-1,0.1).at(z=1)
        self.assertEqual(ray, Ray(-0.9, 0.1))

        ray = Ray(-1,0.1).at(z=-1)
        self.assertEqual(ray, Ray(-1.1, 0.1))

        ray = Ray(-1,0.1,z=1).at(z=1)
        self.assertEqual(ray, Ray(-1.0, 0.1))

    def testRayTrace(self):
        rayTrace = [Ray(0,0.1), Ray(0.1,0.2,z=1), Ray(0.3,0,z=2)]

        self.assertEqual(Ray.along(rayTrace, z=0), Ray(0,0.1))
        self.assertEqual(Ray.along(rayTrace, z=0.5), Ray(0.05,0.1))
        self.assertEqual(Ray.along(rayTrace, z=1.0).y, 0.1)
        self.assertEqual(Ray.along(rayTrace, z=1.0), Ray(0.1,0.2))
        self.assertEqual(Ray.along(rayTrace, z=1.5), Ray(0.2,0.2))
        self.assertEqual(Ray.along(rayTrace, z=2.0), Ray(0.3,0))


if __name__ == '__main__':
    envtest.main()
