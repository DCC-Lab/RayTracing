import envtest  # modifies path
from raytracing import *
import itertools

inf = float("+inf")


def multiplyBy2(value) -> float:
    return 2 * value


def mul(value1, value2) -> float:
    return value1 * value2


class TestMultiProcessorSupport(envtest.RaytracingTestCase):
    @envtest.skipIf(sys.platform == 'darwin' and sys.version_info.major == 3 and sys.version_info.minor <= 7,
                    "Endless loop on macOS")
    # Some information here: https://github.com/gammapy/gammapy/issues/2453
    def testMultiPool(self):
        processes = 8
        inputValues = [1, 2, 3, 4]
        with multiprocessing.Pool(processes=processes) as pool:
            outputValues = pool.map(multiplyBy2, inputValues)
        self.assertEqual(outputValues, list(map(multiplyBy2, inputValues)))

    @envtest.skipIf(sys.platform == 'darwin' and sys.version_info.major == 3 and sys.version_info.minor <= 7,
                    "Endless loop on macOS")
    # Some information here: https://github.com/gammapy/gammapy/issues/2453
    def testMultiPoolWith2Args(self):
        processes = 4
        inputValues = [1, 2, 3, 4]
        with multiprocessing.Pool(processes=processes) as pool:
            outputValues = pool.starmap(mul, itertools.product(inputValues, [2]))
        func = lambda val1: mul(val1, 2)
        self.assertEqual(outputValues, list(map(func, inputValues)))


if __name__ == '__main__':
    envtest.main()
