import envtest  # modifies path
import subprocess

from raytracing import *
inf = float("+inf")

class TestCompactRays(envtest.RaytracingTestCase):
    def testCompactRaysInitNotNone(self):
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

    def testFillWithRandomUniformActuallyModifiesRays(self):
        rays = CompactRays(maxCount=100)
        rays.fillWithRandomUniform(yMax=1.0, thetaMax=0.5)
        hasNonZeroY = any(rays[i].y != 0 for i in range(len(rays)))
        hasNonZeroTheta = any(rays[i].theta != 0 for i in range(len(rays)))
        self.assertTrue(hasNonZeroY, "fillWithRandomUniform did not modify y values")
        self.assertTrue(hasNonZeroTheta, "fillWithRandomUniform did not modify theta values")

    def testFillWithRandomUniformValuesWithinRange(self):
        rays = CompactRays(maxCount=1000)
        rays.fillWithRandomUniform(yMax=2.0, thetaMax=0.3)
        for i in range(len(rays)):
            ray = rays[i]
            self.assertGreaterEqual(ray.y, -2.0)
            self.assertLessEqual(ray.y, 2.0)
            self.assertGreaterEqual(ray.theta, -0.3)
            self.assertLessEqual(ray.theta, 0.3)

    def testFillWithRandomUniformExplicitMin(self):
        rays = CompactRays(maxCount=1000)
        rays.fillWithRandomUniform(yMax=5.0, yMin=1.0, thetaMax=0.5, thetaMin=0.1)
        for i in range(len(rays)):
            ray = rays[i]
            self.assertGreaterEqual(ray.y, 1.0)
            self.assertLessEqual(ray.y, 5.0)
            self.assertGreaterEqual(ray.theta, 0.1)
            self.assertLessEqual(ray.theta, 0.5)

    def testCompactRayIsBlockedSetter(self):
        rays = CompactRays(maxCount=1)
        ray = rays[0]
        self.assertFalse(ray.isBlocked)
        ray.isBlocked = True
        self.assertTrue(ray.isBlocked)
        ray.isBlocked = False
        self.assertFalse(ray.isBlocked)

    def testCompactRayApertureDiameter(self):
        rays = CompactRays(maxCount=1)
        ray = rays[0]
        ray.apertureDiameter = 25.4
        self.assertAlmostEqual(ray.apertureDiameter, 25.4, places=3)

    def testCompactRayWavelength(self):
        rays = CompactRays(maxCount=1)
        ray = rays[0]
        ray.wavelength = 0.532
        self.assertAlmostEqual(ray.wavelength, 0.532, places=3)

    def testCompactRayAssignRoundTrip(self):
        rays = CompactRays(maxCount=1)
        original = Ray(y=1.5, theta=-0.3, z=10.0, isBlocked=True)
        original.apertureDiameter = 25.0
        original.wavelength = 0.633
        rays[0].assign(original)
        ray = rays[0]
        self.assertAlmostEqual(ray.y, 1.5, places=3)
        self.assertAlmostEqual(ray.theta, -0.3, places=3)
        self.assertAlmostEqual(ray.z, 10.0, places=3)
        self.assertTrue(ray.isBlocked)
        self.assertAlmostEqual(ray.apertureDiameter, 25.0, places=3)
        self.assertAlmostEqual(ray.wavelength, 0.633, places=3)

    def testCompactRaysFromRayList(self):
        originals = [Ray(y=1, theta=0.1), Ray(y=-2, theta=0.5), Ray(y=0, theta=-0.3)]
        rays = CompactRays(rays=originals)
        self.assertEqual(len(rays), 3)
        for i, original in enumerate(originals):
            self.assertAlmostEqual(rays[i].y, original.y, places=3)
            self.assertAlmostEqual(rays[i].theta, original.theta, places=3)

    def testCompactRaysNoArgsRaises(self):
        with self.assertRaises(ValueError):
            CompactRays()


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

    def testCompactRaytracesMultiple(self):
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

    def testCompactRaytraceNegativeIndex(self):
        rays = CompactRays(maxCount=5)
        for i in range(5):
            rays[i].y = i * 10

        raytrace = CompactRaytrace(rays, firstIndex=0, traceLength=5)
        self.assertAlmostEqual(raytrace[-1].y, 40, places=3)
        self.assertAlmostEqual(raytrace[-2].y, 30, places=3)
        self.assertAlmostEqual(raytrace[-5].y, 0, places=3)

    def testCompactRaytracesNegativeIndex(self):
        rays = CompactRays(maxCount=10)
        for i in range(10):
            rays[i].y = i

        raytraces = CompactRaytraces(rays, traceLength=5)
        # raytraces[0] covers indices 0-4, raytraces[1] covers 5-9
        # raytraces[-1] should be the same as raytraces[1]
        self.assertAlmostEqual(raytraces[-1][0].y, 5, places=3)
        self.assertAlmostEqual(raytraces[-1][-1].y, 9, places=3)

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
