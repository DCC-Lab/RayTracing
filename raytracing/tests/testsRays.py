import envtest  # modifies path
from raytracing import *

inf = float("+inf")

# Set to False if you don't want to test saving and/or loading a lot or rays
# These tests can take a few seconds
testSaveHugeFile = True


class TestRays(envtest.RaytracingTestCase):

    def testRaysNoArgs(self):
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

    def testRaysEmptyListArg(self):
        r = Rays([])
        self.assertListEqual(r.rays, [])

    def testRaysInitDifferentIterInputs(self):
        listOfRays = [Ray(), Ray(1, 1), Ray(1, -2), Ray(0, -1)]
        tupleOfRays = tuple(listOfRays)
        npArrayOfRays = np.array(listOfRays)
        raysFromList = Rays(listOfRays)
        raysFromTuple = Rays(tupleOfRays)
        raysFromArray = Rays(npArrayOfRays)

        self.assertListEqual(raysFromList.rays, listOfRays)
        self.assertListEqual(raysFromTuple.rays, list(tupleOfRays))
        self.assertListEqual(raysFromArray.rays, list(npArrayOfRays))

    def testRaysInitNoRightIterInput(self):
        with self.assertRaises(TypeError):
            Rays("Ray(), Ray(1), Ray(1,1)")

    def testRaysInitNotAllRayInstances(self):
        with self.assertRaises(TypeError):
            Rays([Ray(), [1, 2], Ray()])

    def testRaysInitWrongObj(self):
        with self.assertRaises(TypeError):
            Rays(Matrix())

    def testRaysIterations(self):
        raysList = [Ray(), Ray(2), Ray(1)]
        rays = Rays(raysList)
        index = 0
        for ray in rays:
            self.assertEqual(ray, raysList[index])
            index += 1

    def testRaysLenDefaultArgs(self):
        r = Rays()
        self.assertEqual(len(r), 0)

    def testRaysLenEmptyList(self):
        r = Rays([])
        self.assertEqual(len(r), 0)

    def testRaysLen(self):
        listOfRays = [Ray(), Ray(1, 1), Ray(1, -2), Ray(0, -1)]
        r = Rays(listOfRays)
        self.assertEqual(len(r), len(listOfRays))

    def testRaysGetRay(self):
        raysList = [Ray(), Ray(1), Ray(-1)]
        rays = Rays(raysList)
        for i in range(len(raysList)):
            self.assertEqual(rays[i], raysList[i])

    def testCountRaysDefaultArgs(self):
        r = Rays()
        self.assertEqual(r.count, 0)

    def testCountRaysEmptyList(self):
        r = Rays([])
        self.assertEqual(r.count, 0)

    def testCountRays(self):
        listOfRays = [Ray(), Ray(1, 1), Ray(1, -2), Ray(0, -1)]
        r = Rays(listOfRays)
        self.assertEqual(r.count, len(listOfRays))

    def testYValuesDefaultArgs(self):
        r = Rays()
        self.assertListEqual(r.yValues, [])

    def testYValuesEmptyList(self):
        r = Rays([])
        self.assertListEqual(r.yValues, [])

    def testYValues(self):
        yvalues = list(range(10))
        listOfRays = [Ray(y) for y in yvalues]
        r = Rays(listOfRays)
        self.assertListEqual(r.yValues, yvalues)

    def testYValuesNotNone(self):
        r = Rays([Ray()])
        # Don't do this, only for test purpose
        yvalues = [0]
        r._yValues = yvalues
        self.assertListEqual(r.yValues, yvalues)

    def testThetaValuesDefaultArgs(self):
        r = Rays()
        self.assertListEqual(r.thetaValues, [])

    def testThetaValuesEmptyList(self):
        r = Rays([])
        self.assertListEqual(r.thetaValues, [])

    def testThetaValues(self):
        thetaValues = list(np.linspace(-pi / 2, pi / 2, 10))
        listOfRays = [Ray(theta=theta) for theta in thetaValues]
        r = Rays(listOfRays)
        self.assertListEqual(r.thetaValues, thetaValues)

    def testRayCountHist(self):
        r = Rays([Ray()])
        # Don't do this, only for test purpose
        thetaValues = [0]
        r._thetaValues = thetaValues
        self.assertListEqual(r.thetaValues, thetaValues)

    def testDisplayProgress(self):
        rays = [Ray(0, 0)]
        rays = Rays(rays)
        rays.progressLog = 1
        self.assertPrints(rays.displayProgress, "Progress 0/1 (0%)")

    def testDisplayProgressSmallerProgressLog(self):
        rays = [Ray(), Ray(2, 0), Ray(1, 0), Ray(-1, 0)]
        rays = Rays(rays)
        rays.progressLog = 1
        self.assertPrints(rays.displayProgress, "Progress 0/4 (0%)")

    def testDisplayProgressNothing(self):
        rays = [Ray(0, 0)]
        rays = Rays(rays)
        rays.iteration = 1
        self.assertPrints(rays.displayProgress, "")

    def testRayCountHistogramBinCountSpecified(self):
        r = [Ray(a, a) for a in range(6)]
        r = Rays(r)
        tRes = ([x * 0.5 + 0.25 for x in range(10)], [1, 0, 1, 0, 1, 0, 1, 0, 1, 1])
        self.assertTupleEqual(r.rayCountHistogram(10), tRes)

    def testRayCountHistogramMinValueSpecified(self):
        r = [Ray(a, a) for a in range(50)]
        r = Rays(r)
        rayCountHist = r.rayCountHistogram(minValue=2)
        comparison = ([(a - 1) * 1.175 + 1.4125 for a in range(2, 42)],
                      [2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1,
                       1, 1, 2, 1, 1, 1, 1, 2])
        self.assertEqual(len(rayCountHist[0]), len(comparison[0]))
        self.assertEqual(len(rayCountHist[1]), len(comparison[1]))
        for i in range(len(rayCountHist[0])):
            self.assertAlmostEqual(rayCountHist[0][i], comparison[0][i])
        self.assertListEqual(rayCountHist[1], comparison[1])

    def testRayAnglesHistogramBinCountSpecified(self):
        r = [Ray(a, a / 6) for a in range(6)]
        r = Rays(r)
        tRes = ([(x * 1 / 12 + 1 / 24) for x in range(10)], [1, 1, 0, 1, 0, 0, 1, 1, 0, 1])
        rayAngleHist = r.rayAnglesHistogram(10)
        self.assertEqual(len(rayAngleHist[0]), len(tRes[0]))
        self.assertEqual(len(rayAngleHist[1]), len(tRes[1]))
        for i in range(len(rayAngleHist[0])):
            self.assertAlmostEqual(rayAngleHist[0][i], tRes[0][i])
        self.assertListEqual(rayAngleHist[1], tRes[1])

    def testRayAnglesHistogramMinValueSpecified(self):
        r = [Ray(a, a / 50) for a in range(50)]
        r = Rays(r)
        rayAngleHist = r.rayAnglesHistogram(minValue=2 / 50)
        comparison = ([((a - 1) * 1.175 + 1.4125) / 50 for a in range(2, 42)],
                      [2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1,
                       1, 1, 2, 1, 1, 1, 1, 2])
        self.assertEqual(len(rayAngleHist[0]), len(comparison[0]))
        self.assertEqual(len(rayAngleHist[1]), len(comparison[1]))
        for i in range(len(rayAngleHist[0])):
            self.assertAlmostEqual(rayAngleHist[0][i], comparison[0][i])
        self.assertListEqual(rayAngleHist[1], comparison[1])

    def testRayCountHistAlreadyComputedSameParams(self):
        r = Rays([Ray(2), Ray()])
        init = r.rayCountHistogram()
        final = r.rayCountHistogram()
        self.assertIsNotNone(init)
        self.assertIsNotNone(final)
        self.assertTupleEqual(init, final)

    def testRayCountHistAlreadyComputedDifferentParams(self):
        r = Rays([Ray(2), Ray()])
        init = r.rayCountHistogram()
        final = r.rayCountHistogram(maxValue=1)
        self.assertNotEqual(init, final)

    def testRayAnglesHistAlreadyComputedSameParams(self):
        r = Rays([Ray(2), Ray()])
        init = r.rayAnglesHistogram()
        final = r.rayAnglesHistogram()
        self.assertIsNotNone(init)
        self.assertIsNotNone(final)
        self.assertTupleEqual(init, final)

    def testRayAnglesHistAlreadyComputedDifferentParams(self):
        r = Rays([Ray(0, 2), Ray()])
        init = r.rayAnglesHistogram()
        final = r.rayAnglesHistogram(maxValue=1)
        self.assertNotEqual(init, final)

    def testAppend(self):
        r = Rays([Ray(1, 1)])
        r.append(Ray())
        self.assertListEqual(r.rays, [Ray(1, 1), Ray()])

    def testAppendInvalidateCachedValues(self):
        r = Rays([Ray(1, 1)])
        r.append(Ray())
        r.rayAnglesHistogram()
        r.rayCountHistogram()
        r.append(Ray(2, 0))
        self.assertIsNone(r._yValues)
        self.assertIsNone(r._thetaValues)
        self.assertIsNone(r._yHistogram)
        self.assertIsNone(r._thetaHistogram)
        self.assertIsNone(r._directionBinEdges)
        self.assertIsNone(r._countHistogramParameters)
        self.assertIsNone(r._xValuesCountHistogram)
        self.assertIsNone(r._anglesHistogramParameters)
        self.assertIsNone(r._xValuesAnglesHistogram)

    def testAppendInvalidInput(self):
        rays = Rays()
        with self.assertRaises(TypeError):
            rays.append("This is a ray")


class TestRaysSaveAndLoad(envtest.RaytracingTestCase):

    def setUp(self) -> None:
        self.testRays = Rays([Ray(), Ray(1, 1), Ray(-1, 1), Ray(-1, -1)])
        self.fileName = self.tempFilePath('testFile.pkl')
        with open(self.fileName, 'wb') as file:
            pickle.Pickler(file).dump(self.testRays.rays)
        time.sleep(0.5)  # Make sure everything is ok
        super().setUp()

    def testLoadFileDoesntExists(self):
        file = r"this file\doesn't\exist"
        rays = Rays()
        with self.assertRaises(FileNotFoundError):
            rays.load(file)

    def assertLoadNotFailed(self, rays: Rays, name: str = None, append: bool = False):
        if name is None:
            name = self.fileName
        self.assertDoesNotRaise(rays.load, None, name, append)

    def testLoadNoInitialArgs(self):
        rays = Rays()
        self.assertLoadNotFailed(rays)
        self.assertListEqual(rays.rays, self.testRays.rays)

    def testLoadEmptyList(self):
        rays = Rays()
        self.assertLoadNotFailed(rays)
        self.assertListEqual(rays.rays, self.testRays.rays)

    def testLoadAppend(self):
        initialRays = [Ray(), Ray(1, 1), Ray(1), Ray(0, 1)]
        rays = Rays(initialRays)
        finalRays = initialRays[:]  # We copy with [:]
        finalRays.extend(self.testRays.rays[:])
        self.assertLoadNotFailed(rays, append=True)  # We append
        self.assertListEqual(rays.rays, finalRays)

    def testLoadOverride(self):
        initialRays = [Ray(), Ray(1, 1), Ray(1), Ray(0, 1)]
        rays = Rays(initialRays)
        self.assertLoadNotFailed(rays)  # We don't append, we override
        self.assertListEqual(rays.rays, self.testRays.rays)

    def testLoadWrongIterable(self):
        wrongObj = 7734
        fileName = self.tempFilePath('wrongObj.pkl')
        with open(fileName, 'wb') as file:
            pickle.Pickler(file).dump(wrongObj)
        time.sleep(0.5)  # Make sure everything is ok
        with self.assertRaises(IOError):
            Rays().load(fileName)

    def testLoadWrongTypeInIterable(self):
        fileName = self.tempFilePath('wrongObj.pkl')
        wrongIterType = [Ray(), Ray(1), [1, 1]]
        with open(fileName, 'wb') as file:
            pickle.Pickler(file).dump(wrongIterType)
        time.sleep(0.5)

        with self.assertRaises(IOError):
            Rays().load(fileName)

    def assertSaveNotFailed(self, rays: Rays, name: str):
        self.assertDoesNotRaise(rays.save, None, name)

    def testSaveInEmptyFile(self):
        rays = Rays([Ray(), Ray(1, 1), Ray(-1, 1)])
        fileName = self.tempFilePath('wrongObj.pkl')
        self.assertSaveNotFailed(rays, fileName)

    def testSaveInFileNotEmpty(self):
        rays = Rays([Ray(), Ray(1, 1), Ray(-1, 1)])
        self.assertSaveNotFailed(rays, self.fileName)

    @envtest.skipIf(not testSaveHugeFile, "Don't test saving a lot of rays")
    def testSaveHugeFile(self):
        fileName = self.tempFilePath('hugeFile.pkl')
        nbRays = 10_000
        raysList = [Ray(y, y / nbRays) for y in range(nbRays)]
        rays = Rays(raysList)
        self.assertSaveNotFailed(rays, fileName)

    def testSaveThenLoad(self):
        raysList = [Ray(), Ray(-1), Ray(2), Ray(3)]
        rays = Rays(raysList)
        fileName = self.tempFilePath('testSaveAndLoad.pkl')
        raysLoad = Rays()
        self.assertSaveNotFailed(rays, fileName)
        self.assertLoadNotFailed(raysLoad, fileName)
        self.assertListEqual(raysLoad.rays, rays.rays)

    @envtest.skipIf(not testSaveHugeFile, "Don't test saving then loading a lot of rays")
    def testSaveThenLoadHugeFile(self):
        nbRays = 10_000
        raysList = [Ray(y, y / nbRays) for y in range(nbRays)]
        rays = Rays(raysList)
        raysLoad = Rays()
        fileName = self.tempFilePath('hugeFile.pkl')
        self.assertSaveNotFailed(rays, fileName)
        self.assertLoadNotFailed(raysLoad, fileName)
        self.assertListEqual(raysLoad.rays, rays.rays)


if __name__ == '__main__':
    envtest.main()
