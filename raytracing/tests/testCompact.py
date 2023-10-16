import envtest  # modifies path
import subprocess

from raytracing import *
inf = float("+inf")

class TestCompactRays(envtest.RaytracingTestCase):
    def testCompactRaysInit(self):
        self.assertIsNotNone(CompactRays(maxCount=100))

    def testCompactRaysInit(self):
        rays=CompactRays(maxCount=100)
        self.assertIsNotNone(rays)
        self.assertEqual(len(rays), 100)

    def testCompactRaysGetItem(self):
        rays=CompactRays(maxCount=100)
        self.assertIsNotNone(rays)
        for ray in rays:
            self.assertIsNotNone(ray)
            self.assertEqual(ray.y, 0)
            self.assertEqual(ray.theta, 0)
            self.assertEqual(ray.z, 0)
        self.assertEqual(len(rays), 100)

    def testCompactRaysSetItem(self):
        rays=CompactRays(maxCount=100)
        ray = Ray(y=1, theta=0.5)
        rays[0] = ray
        self.assertEqual(rays[0].y, ray.y)
        self.assertEqual(rays[0].theta, ray.theta)

    def testRaysListRaysAndCompactEquivalence(self):
        inputRays1 = []
        for y in [-1, 0, 1]:
            for t in [-1, -0.5, 0, 0.5, 1.0]:
                inputRays1.append(Ray(y, t))
                inputRays1.append(Ray(-y, -t))

        inputRays2 = CompactRays(maxCount=len(inputRays1))

        for i, otherRay in enumerate(inputRays1):
            inputRays2[i] = otherRay

        for r1, r2 in zip(inputRays1, inputRays2):
            self.assertEqual(r1, r2)

    def testCompactRaysPreallocated(self):
        rays = CompactRays(maxCount=10)
        self.assertIsNotNone(rays)
        self.assertEqual(len(rays), 10)

    def testCompactRaysFromBuffer(self):
        rays = CompactRays(compactRaysStructuredBuffer=bytearray(b'\x00'*CompactRay.Struct.itemsize))
        self.assertEqual(len(rays), 1)

    def testCompactRaysFromBufferElementRightType(self):
        rays = CompactRays(compactRaysStructuredBuffer=bytearray(b'\x00' * CompactRay.Struct.itemsize))
        self.assertTrue(isinstance(rays[0], CompactRay))

    def testCompactRayElementHasRightValues(self):
        value = 1.0
        floatBytes = pack('<f', value) # should use dtype formats? Don't know how to read alignment
        rays = CompactRays(compactRaysStructuredBuffer=bytearray(floatBytes + b'\x00' * (CompactRay.Struct.itemsize-4)))
        ray = rays[0]
        self.assertEqual(ray.y, value)
        self.assertEqual(ray.isBlocked, False)

    def testCompactRayElementCanChangeValue(self):
        value = 1.0
        floatBytes = pack('<f', value) # should use dtype formats? Don't know how to read alignment
        rays = CompactRays(compactRaysStructuredBuffer=bytearray(floatBytes + b'\x00' * (CompactRay.Struct.itemsize-4)))
        ray = rays[0]
        self.assertEqual(ray.y, value)
        self.assertEqual(ray.isBlocked, False)
        ray.y = 2.0*value+1
        self.assertEqual(ray.y, 2*value+1)

    def testAppendElementToBufferFails(self):
        rays = CompactRays(compactRaysStructuredBuffer=bytearray(b'\x00' * (CompactRay.Struct.itemsize)))
        with self.assertRaises(Exception):
            rays.append((1,2,3,4,5,6))

        rays = CompactRays(maxCount=10)
        with self.assertRaises(Exception):
            rays.append((1,2,3,4,5,6))

    def testReplaceValue(self):
        rays = CompactRays(maxCount=10)
        rays[0].y = 1
        rays[2].theta = 2
        self.assertEqual(rays[0].y, 1)
        self.assertEqual(rays[2].theta, 2)




    # def testDefaultCompactRay(self):
    #     ray = CompactRay()
    #     self.assertIsNotNone(ray)
    #
    # def testCompactRayNoInitPossibleFromComponent(self):
    #     with self.assertRaises(Exception):
    #         ray = CompactRay(y=1, theta=2)
    #
    # def testCompactRayNoInitPossibleFromComponent(self):
    #     ray = CompactRay()
    #     self.assertIsNotNone(ray)
    #     with self.assertRaises(Exception):
    #         ray = CompactRay(y=1, theta=2)

    # def testCompactRayFromRay(self):
    #     someRay = Ray(y=1, theta=2)
    #     ray = CompactRay(someRay)
    #     self.assertIsNotNone(ray)
    #     self.assertEqual(ray, someRay)

    # def testAsStructuredArray(self):
    #     rays = RandomUniformRays()
    #     structArray = np.array([ r.struct for r in rays ], dtype=CompactRay.Struct)
    #     print(structArray)


class TestCompactRaytraces(envtest.RaytracingTestCase):

    def testCompactRaytraceInit(self):
        rays = CompactRays(maxCount=10)
        self.assertIsNotNone(rays)
        self.assertEqual(len(rays), 10)
        raytrace = CompactRaytrace(rays, firstIndex=0, traceLength=10)
        self.assertEqual(len(raytrace), 10)

    def testCompactRaytraceAssignment(self):
        rays = CompactRays(maxCount=10)
        self.assertIsNotNone(rays)
        self.assertEqual(len(rays), 10)

        for i, ray in enumerate(rays):
            ray.y = i
            ray.theta = i
            ray.z = i

        raytrace = CompactRaytrace(rays, firstIndex=0, traceLength=10)

        self.assertEqual(len(raytrace), 10)

        for i in range(10):
            self.assertEqual(raytrace[i].y, i)
            self.assertEqual(raytrace[i].theta, i)
            self.assertEqual(raytrace[i].z, i)

    def testCompactRaytraceIterator(self):
        rays = CompactRays(maxCount=10)
        self.assertIsNotNone(rays)
        self.assertEqual(len(rays), 10)

        for i, ray in enumerate(rays):
            ray.y = i
            ray.theta = i
            ray.z = i

        raytrace = CompactRaytrace(rays, firstIndex=0, traceLength=10)

        self.assertEqual(len(raytrace), 10)

        for i,ray in enumerate(raytrace):
            self.assertEqual(ray.y, i)
            self.assertEqual(ray.theta, i)
            self.assertEqual(ray.z, i)

    def testCompactRaytraces(self):
        rays = CompactRays(maxCount=10)
        self.assertIsNotNone(rays)
        self.assertEqual(len(rays), 10)
        raytraces = CompactRaytraces(rays, traceLength=5)

        self.assertEqual(len(raytraces), 2)

        self.assertEqual(len(raytraces[0]), 5)
        self.assertEqual(len(raytraces[1]), 5)

    def testCompactRaytracesValidated(self):
        rays = CompactRays(maxCount=10)
        self.assertIsNotNone(rays)
        self.assertEqual(len(rays), 10)
        raytraces = CompactRaytraces(rays, traceLength=5)

        for raytrace in raytraces:
            self.assertEqual(len(raytrace), 5)

    def testCompactRaytraces(self):
        inputRays1 = []
        for y in [-1, 0, 1]:
            for t in [-1, -0.5, 0, 0.5, 1.0]:
                inputRays1.append(Ray(y, t))

        inputRays2 = CompactRays(maxCount=len(inputRays1))
        inputRays3 = Rays()
        for i, otherRay in enumerate(inputRays1):
            compactRay = inputRays2[i]
            compactRay.y = otherRay.y
            compactRay.theta = otherRay.theta
            inputRays3.append(otherRay, copy=True)

        for r1, r2, r3 in zip(inputRays1, inputRays2, inputRays3):
            self.assertEqual(r1, r2)
            self.assertEqual(r1, r3)
