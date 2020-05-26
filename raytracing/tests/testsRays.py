import unittest
import envtest  # modifies path
from raytracing import *

inf = float("+inf")

# Set to False if you don't want to test saving and/or loading a lot or rays
# These tests can take a few seconds
testSaveHugeFile = True


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

    def testRaysInitDifferentInputs(self):
        listOfRays = [Ray(), Ray(1, 1), Ray(1, -2), Ray(0, -1)]
        tupleOfRays = tuple(listOfRays)
        npArrayOfRays = array(listOfRays)
        raysFromList = Rays(listOfRays)
        raysFromTuple = Rays(tupleOfRays)
        raysFromArray = Rays(npArrayOfRays)

        self.assertListEqual(raysFromList.rays, listOfRays)
        self.assertListEqual(raysFromTuple.rays, list(tupleOfRays))
        self.assertListEqual(raysFromArray.rays, list(npArrayOfRays))

        with self.assertRaises(TypeError):
            # This should raise an TypeError exception
            Rays("Ray(), Ray(1), Ray(1,1)")

        with self.assertRaises(TypeError):
            # This should raise an TypeError exception
            Rays([Ray(), [1, 2], Ray()])

        with self.assertRaises(TypeError):
            # This should raise an TypeError exception
            Rays(Matrix())

    def testRaysIterations(self):
        raysList = [Ray(), Ray(2), Ray(1)]
        rays = Rays(raysList)
        index = 0
        for ray in rays:
            self.assertEqual(ray, raysList[index])
            index += 1

    def testRaysLen(self):
        r = Rays()
        self.assertEqual(len(r), 0)

        r = Rays([])
        self.assertEqual(len(r), 0)

        listOfRays = [Ray(), Ray(1, 1), Ray(1, -2), Ray(0, -1)]
        r = Rays(listOfRays)
        self.assertEqual(len(r), len(listOfRays))

    def testRaysGetRay(self):
        raysList = [Ray(), Ray(1), Ray(-1)]
        rays = Rays(raysList)
        for i in range(len(raysList)):
            self.assertEqual(rays[i], raysList[i])

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

    def testYValuesNotNone(self):
        r = Rays([Ray()])
        # Don't do this, only for test purpose
        yvalues = [0]
        r._yValues = yvalues
        self.assertListEqual(r.yValues, yvalues)

    def testThetaValues(self):
        r = Rays()
        self.assertListEqual(r.thetaValues, [])

        r = Rays([])
        self.assertListEqual(r.thetaValues, [])

        listOfRays = [Ray(), Ray(1, 1), Ray(1, -2), Ray(0, -1)]
        r = Rays(listOfRays)
        self.assertListEqual(r.thetaValues, [0, 1, -2, -1])

    def testRayCountHist(self):
        r = Rays([Ray()])
        # Don't do this, only for test purpose
        thetaValues = [0]
        r._thetaValues = thetaValues
        self.assertListEqual(r.thetaValues, thetaValues)

    def testDisplayProgress(self):
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            rays = [Ray(0, 0)]
            rays = Rays(rays)
            rays.progressLog = 1
            rays.displayProgress()
        out = f.getvalue()
        self.assertEqual(out.strip(), "Progress 0/1 (0%)")

    def testDisplayProgressSmallerProgressLog(self):
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            rays = [Ray(), Ray(2, 0), Ray(1, 0), Ray(-1, 0)]
            rays = Rays(rays)
            rays.progressLog = 1
            rays.displayProgress()
        out = f.getvalue()
        self.assertEqual(out.strip(), "Progress 0/4 (0%)")

    def testDisplayProgressNothing(self):
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            rays = [Ray(0, 0)]
            rays = Rays(rays)
            rays.iteration = 1
            rays.displayProgress()
        out = f.getvalue()
        self.assertEqual(out.strip(), "")

    def testRayCountHistogram(self):
        r = [Ray(a, a) for a in range(6)]
        r = Rays(r)
        tRes = ([x * 0.5 + 0.25 for x in range(10)], [1, 0, 1, 0, 1, 0, 1, 0, 1, 1])
        self.assertTupleEqual(r.rayCountHistogram(10), tRes)

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

    def testRayAnglesHistogram(self):
        r = [Ray(a, a / 6) for a in range(6)]
        r = Rays(r)
        tRes = ([(x * 1 / 12 + 1 / 24) for x in range(10)], [1, 1, 0, 1, 0, 0, 1, 1, 0, 1])
        rayAngleHist = r.rayAnglesHistogram(10)
        self.assertEqual(len(rayAngleHist[0]), len(tRes[0]))
        self.assertEqual(len(rayAngleHist[1]), len(tRes[1]))
        for i in range(len(rayAngleHist[0])):
            self.assertAlmostEqual(rayAngleHist[0][i], tRes[0][i])
        self.assertListEqual(rayAngleHist[1], tRes[1])

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

    def testRayCountHistAlreadyComputed(self):
        r = Rays([Ray(2), Ray()])
        init = r.rayCountHistogram()
        self.assertIsNotNone(init)  # First time compute
        final = r.rayCountHistogram()
        self.assertIsNotNone(final)  # Second time compute, now works

        self.assertTupleEqual(init, final)
        final = r.rayCountHistogram(maxValue=1)
        self.assertNotEqual(init, final)

    def testRayAnglesHistAlreadyComputed(self):
        r = Rays([Ray(0, 2), Ray()])
        init = r.rayAnglesHistogram()
        self.assertIsNotNone(init)  # First time compute
        final = r.rayAnglesHistogram()
        self.assertIsNotNone(final)  # Second time compute, now works

        self.assertTupleEqual(init, final)
        final = r.rayAnglesHistogram(maxValue=1)
        self.assertNotEqual(init, final)

    def testAppend(self):
        r = Rays([Ray(1, 1)])
        self.assertListEqual(r.rays, [Ray(1, 1)])
        r.append(Ray())
        self.assertListEqual(r.rays, [Ray(1, 1), Ray()])

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


class TestRaysSaveAndLoad(unittest.TestCase):

    def setUp(self) -> None:
        self.testRays = Rays([Ray(), Ray(1, 1), Ray(-1, 1), Ray(-1, -1)])
        self.fileName = 'testFile.pkl'
        with open(self.fileName, 'wb') as file:
            pickle.Pickler(file).dump(self.testRays.rays)
        time.sleep(0.5)  # Make sure everything is ok

    def tearDown(self) -> None:
        if os.path.exists(self.fileName):
            os.remove(self.fileName)  # We remove the test file

    def testLoadFileDoesntExists(self):
        file = r"this file\doesn't\exists"
        rays = Rays()
        with self.assertRaises(FileNotFoundError):
            rays.load(file)

    def assertLoadNotFailed(self, rays: Rays, name: str = None, append: bool = False):
        if name is None:
            name = self.fileName
        try:
            rays.load(name, append)
        except Exception as exception:
            self.fail(f"An exception was raised:\n{exception}")

    def testLoad(self):
        rays = Rays()
        self.assertLoadNotFailed(rays)
        self.assertListEqual(rays.rays, self.testRays.rays)
        rays._rays = []
        self.assertLoadNotFailed(rays)
        self.assertListEqual(rays.rays, self.testRays.rays)

        finalRays = self.testRays.rays[:]  # We copy with [:]
        finalRays.extend(self.testRays.rays[:])
        self.assertLoadNotFailed(rays, append=True)  # We append
        self.assertListEqual(rays.rays, finalRays)

        self.assertLoadNotFailed(rays)  # We don't append, we override
        self.assertListEqual(rays.rays, self.testRays.rays)

    def testLoadWrongFileContent(self):
        wrongObj = 7734
        fileName = 'wrongObj.pkl'
        with open(fileName, 'wb') as file:
            pickle.Pickler(file).dump(wrongObj)
        time.sleep(0.5)  # Make sure everything is ok

        try:
            with self.assertRaises(IOError):
                Rays().load(fileName)
        except AssertionError as exception:
            self.fail(str(exception))
        finally:
            os.remove(fileName)

        wrongIterType = [Ray(), Ray(1), [1, 1]]
        with open(fileName, 'wb') as file:
            pickle.Pickler(file).dump(wrongIterType)
        time.sleep(0.5)
        try:
            with self.assertRaises(IOError):
                Rays().load(fileName)
        except AssertionError as exception:
            self.fail(str(exception))
        finally:
            os.remove(fileName)

    def assertSaveNotFailed(self, rays: Rays, name: str, deleteNow: bool = True):
        try:
            rays.save(name)
        except Exception as exception:
            self.fail(f"An exception was raised:\n{exception}")
        finally:
            if os.path.exists(name) and deleteNow:
                os.remove(name)  # We delete the temp file

    def testSaveInEmptyFile(self):
        rays = Rays([Ray(), Ray(1, 1), Ray(-1, 1)])
        name = "emptyFile.pkl"
        self.assertSaveNotFailed(rays, name)

    def testSaveInFileNotEmpty(self):
        rays = Rays([Ray(), Ray(1, 1), Ray(-1, 1)])
        self.assertSaveNotFailed(rays, self.fileName)

    @unittest.skipIf(not testSaveHugeFile, "Don't test saving a lot of rays")
    def testSaveHugeFile(self):
        nbRays = 100_000
        raysList = [Ray(y, y / nbRays) for y in range(nbRays)]
        rays = Rays(raysList)
        self.assertSaveNotFailed(rays, "hugeFile.pkl")

    def testSaveThenLoad(self):
        raysList = [Ray(), Ray(-1), Ray(2), Ray(3)]
        rays = Rays(raysList)
        name = "testSaveAndLoad.pkl"
        self.assertSaveNotFailed(rays, name, False)
        raysLoad = Rays()
        self.assertLoadNotFailed(raysLoad, name)
        self.assertListEqual(raysLoad.rays, rays.rays)
        os.remove(name)

    @unittest.skipIf(not testSaveHugeFile, "Don't test saving then loading a lot of rays")
    def testSaveThenLoadHugeFile(self):
        nbRays = 100_000
        raysList = [Ray(y, y / nbRays) for y in range(nbRays)]
        rays = Rays(raysList)
        name = "hugeFile.pkl"
        self.assertSaveNotFailed(rays, name, False)
        raysLoad = Rays()
        self.assertLoadNotFailed(raysLoad, name)
        self.assertListEqual(raysLoad.rays, rays.rays)
        os.remove(name)


if __name__ == '__main__':
    unittest.main()
