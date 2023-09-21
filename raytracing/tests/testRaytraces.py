import envtest  # modifies path
import subprocess

from raytracing import *
inf = float("+inf")


class TestMatrix(envtest.RaytracingTestCase):

    def testCompactRaytrace(self):
        rays = CompactRays(maxCount=10)
        self.assertIsNotNone(rays)
        self.assertEqual(len(rays), 10)
        raytrace = CompactRaytrace(rays, firstIndex=0, traceLength=10)

        self.assertEqual(len(raytrace), 10)

        for i in range(10):
            print(raytrace[i])

    def testCompactRaytraceIterator(self):
        rays = CompactRays(maxCount=10)
        self.assertIsNotNone(rays)
        self.assertEqual(len(rays), 10)
        raytrace = CompactRaytrace(rays, firstIndex=0, traceLength=10)

        self.assertEqual(len(raytrace), 10)

        for ray in raytrace:
            print(ray)

    def testCompactRaytraces(self):
        rays = CompactRays(maxCount=10)
        self.assertIsNotNone(rays)
        self.assertEqual(len(rays), 10)
        raytraces = CompactRaytraces(rays, traceLength=5)

        self.assertEqual(len(raytraces), 2)

        self.assertEqual(raytraces[0], 5)
        self.assertEqual(raytraces[1], 5)

    def testCompactRaytraces(self):
        rays = CompactRays(maxCount=10)
        self.assertIsNotNone(rays)
        self.assertEqual(len(rays), 10)
        raytraces = CompactRaytraces(rays, traceLength=5)

        for raytrace in raytraces:
            self.assertEqual(len(raytrace), 5)

